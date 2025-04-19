"""
Prompt refinement functionality for the AI Prompt Generator.

This module provides the core functionality for analyzing existing prompts
and generating targeted enhancements to improve their effectiveness.
"""

from typing import Dict, List, Tuple, Any, Optional
import re
import logging

# Setup logger
logger = logging.getLogger(__name__)


class PromptAnalyzer:
    """
    Analyzer class for existing prompts to identify structure and potential improvements.
    """
    
    def __init__(self):
        """Initialize the prompt analyzer."""
        # Patterns for identifying sections in prompts
        self.section_patterns = [
            # Common section headings (with variations in formatting)
            r'#+\s*(Context|Background|Introduction|Overview)',
            r'#+\s*(Instructions|Requirements|Specifications|Guidelines)',
            r'#+\s*(Format|Structure|Organization|Layout)',
            r'#+\s*(Constraints|Limitations|Restrictions)',
            r'#+\s*(Examples?|Samples?|Reference|Demo)',
            r'#+\s*(Output|Deliverables|Results|Expectations)',
            
            # Sections often found in programming prompts
            r'#+\s*(Code\s*Structure|Technical\s*Requirements|Architecture)',
            r'#+\s*(Testing|Validation|Quality\s*Assurance)',
            r'#+\s*(Best\s*Practices|Guidelines|Standards)',
            
            # Sections for content prompts
            r'#+\s*(Tone|Voice|Style|Audience)',
            r'#+\s*(Key\s*Points|Messages|Talking\s*Points)',
            
            # Other common patterns
            r'#+\s*[A-Z][A-Za-z\s]+:',  # Any capitalized heading with colon
            r'^[A-Z][A-Za-z\s]+:',      # Line starting with capitalized word and colon
        ]
        
        # Common issues in prompts
        self.issue_detectors = {
            "missing_context": lambda p: len(re.findall(r'context|background|overview', p, re.I)) == 0,
            "vague_instructions": lambda p: len(p.split()) < 50,  # Very simple heuristic
            "missing_examples": lambda p: len(re.findall(r'example|sample|for instance', p, re.I)) == 0,
            "missing_output_format": lambda p: len(re.findall(r'format|structure|organization|output', p, re.I)) == 0,
            "no_sections": lambda p: len(self._extract_sections(p)) <= 1,
        }
    
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze an existing prompt to identify its structure and potential improvements.
        
        Args:
            prompt: The existing prompt text
            
        Returns:
            Dictionary with analysis results
        """
        logger.info("Analyzing prompt structure and quality")
        
        results = {
            "sections": self._extract_sections(prompt),
            "issues": self._identify_issues(prompt),
            "quality_score": self._calculate_quality_score(prompt),
            "complexity": self._estimate_complexity(prompt),
            "word_count": len(prompt.split()),
            "domain": self._infer_domain(prompt),
        }
        
        return results
    
    def _extract_sections(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Extract section information from the prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            List of identified sections
        """
        sections = []
        lines = prompt.split('\n')
        
        current_section = None
        current_content = []
        
        for i, line in enumerate(lines):
            # Check if line is a section header
            is_header = False
            header_match = None
            
            for pattern in self.section_patterns:
                match = re.search(pattern, line)
                if match:
                    is_header = True
                    header_match = match
                    break
            
            if is_header:
                # If we were already processing a section, add it
                if current_section:
                    sections.append({
                        "name": current_section,
                        "content": '\n'.join(current_content).strip(),
                        "line_start": i - len(current_content),
                        "line_end": i - 1
                    })
                
                # Start new section
                # Extract section name - this is simplified and might need refinement
                section_name = header_match.group(1) if header_match and header_match.groups() else line.strip('# :')
                current_section = section_name
                current_content = []
            elif current_section:
                current_content.append(line)
            
        # Add the last section if there is one
        if current_section:
            sections.append({
                "name": current_section,
                "content": '\n'.join(current_content).strip(),
                "line_start": len(lines) - len(current_content),
                "line_end": len(lines) - 1
            })
        elif not sections:
            # If no sections were found, treat the whole prompt as one section
            sections.append({
                "name": "Unstructured Content",
                "content": prompt.strip(),
                "line_start": 0,
                "line_end": len(lines) - 1
            })
        
        return sections
    
    def _identify_issues(self, prompt: str) -> List[Dict[str, str]]:
        """
        Identify potential issues in the prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            List of identified issues
        """
        issues = []
        
        for issue_name, detector in self.issue_detectors.items():
            if detector(prompt):
                issue_description = self._get_issue_description(issue_name)
                issues.append({
                    "type": issue_name,
                    "description": issue_description
                })
        
        return issues
    
    def _get_issue_description(self, issue_name: str) -> str:
        """Get the human-readable description for an issue type."""
        descriptions = {
            "missing_context": "The prompt lacks context or background information",
            "vague_instructions": "Instructions may be too vague or brief",
            "missing_examples": "No examples are provided to guide the response",
            "missing_output_format": "Output format or structure is not specified",
            "no_sections": "The prompt lacks clear section organization"
        }
        return descriptions.get(issue_name, "Unspecified issue")
    
    def _calculate_quality_score(self, prompt: str) -> float:
        """
        Calculate a quality score for the prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            Quality score between 0 and 1
        """
        # Start with a perfect score
        score = 1.0
        
        # For each issue found, reduce the score
        issues = self._identify_issues(prompt)
        if issues:
            score -= len(issues) * 0.1  # Each issue reduces score by 0.1
        
        # Consider prompt length (very simple heuristic)
        word_count = len(prompt.split())
        if word_count < 50:
            score -= 0.2
        elif word_count < 100:
            score -= 0.1
        elif word_count > 500:
            score -= 0.1  # Too long can also be an issue
        
        # Consider section organization
        sections = self._extract_sections(prompt)
        if len(sections) == 1:
            score -= 0.2
        elif len(sections) < 3:
            score -= 0.1
        
        # Ensure score stays in valid range
        return max(0.0, min(1.0, score))
    
    def _estimate_complexity(self, prompt: str) -> int:
        """
        Estimate the complexity level of the prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            Complexity level between 1 and 5
        """
        word_count = len(prompt.split())
        section_count = len(self._extract_sections(prompt))
        
        # Very simple complexity calculation
        if word_count < 50 and section_count <= 1:
            return 1
        elif word_count < 100 and section_count <= 2:
            return 2
        elif word_count < 200 and section_count <= 3:
            return 3
        elif word_count < 350 and section_count <= 4:
            return 4
        else:
            return 5
    
    def _infer_domain(self, prompt: str) -> str:
        """
        Infer the domain of the prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            Inferred domain
        """
        # Simplified domain inference based on keyword presence
        # In a real implementation, we'd use the classifier from the classifier module
        keyword_patterns = {
            "software": r'\b(code|program|function|algorithm|software|development|api|database)\b',
            "content": r'\b(write|article|content|blog|story|marketing|creative)\b',
            "business": r'\b(business|strategy|market|analysis|customer|product|service)\b',
            "data_analysis": r'\b(data|analysis|statistics|visualization|pattern|dashboard|report)\b',
            "technical_documentation": r'\b(documentation|guide|manual|reference|tutorial|api|specification)\b'
        }
        
        domain_scores = {}
        for domain, pattern in keyword_patterns.items():
            matches = len(re.findall(pattern, prompt, re.I))
            domain_scores[domain] = matches
        
        max_domain = max(domain_scores.items(), key=lambda x: x[1])
        
        # If no strong domain signals, use "general"
        if max_domain[1] == 0:
            return "general"
            
        return max_domain[0]


class PromptEnhancer:
    """
    Enhancer class for generating improvements to existing prompts.
    """
    
    def __init__(self, analyzer=None):
        """
        Initialize the prompt enhancer.
        
        Args:
            analyzer: PromptAnalyzer instance (will create new one if None)
        """
        self.analyzer = analyzer or PromptAnalyzer()
        
        # Enhancement templates
        self.enhancement_templates = {
            "missing_context": "Add a Context section at the beginning: '# Context\\n{context_suggestion}'",
            "vague_instructions": "Expand the instructions with more details: '{expanded_instructions}'",
            "missing_examples": "Add an Examples section: '# Examples\\n{examples_suggestion}'",
            "missing_output_format": "Add an Output Format section: '# Expected Output Format\\n{format_suggestion}'",
            "no_sections": "Restructure the prompt into sections: '{structured_content}'"
        }
    
    def enhance(self, prompt: str, objective: str = None, desired_improvements: List[str] = None) -> Dict[str, Any]:
        """
        Generate enhancements for a prompt.
        
        Args:
            prompt: The original prompt text
            objective: Optional new objective for refinement
            desired_improvements: Specific improvement types desired
            
        Returns:
            Dictionary with enhancement results
        """
        # Analyze the prompt
        analysis = self.analyzer.analyze(prompt)
        
        # Generate enhancements based on analysis and desired improvements
        enhancements = self._generate_enhancements(
            prompt, 
            analysis, 
            objective, 
            desired_improvements
        )
        
        # Apply enhancements to create refined prompt
        refined_prompt = self._apply_enhancements(prompt, enhancements)
        
        # Return the results
        return {
            "original_prompt": prompt,
            "refined_prompt": refined_prompt,
            "analysis": analysis,
            "enhancements": enhancements,
            "improvement_score": self._calculate_improvement_score(analysis, self.analyzer.analyze(refined_prompt))
        }
    
    def _generate_enhancements(self, 
                             prompt: str, 
                             analysis: Dict[str, Any],
                             objective: str = None,
                             desired_improvements: List[str] = None) -> List[Dict[str, Any]]:
        """
        Generate specific enhancement suggestions.
        
        Args:
            prompt: The original prompt
            analysis: Analysis results
            objective: New objective, if any
            desired_improvements: Specific improvements desired
            
        Returns:
            List of enhancement suggestions
        """
        enhancements = []
        
        # Handle issues identified in analysis
        for issue in analysis["issues"]:
            issue_type = issue["type"]
            
            # Skip if not in desired improvements (if specified)
            if desired_improvements and issue_type not in desired_improvements:
                continue
                
            enhancement = {
                "type": f"fix_{issue_type}",
                "description": f"Fix: {issue['description']}",
                "section": None,
                "content": self._generate_content_for_issue(issue_type, prompt, analysis)
            }
            
            enhancements.append(enhancement)
        
        # If a new objective is provided, suggest updating the content
        if objective:
            # Find the main content section
            main_section = None
            for section in analysis["sections"]:
                if section["name"].lower() in ["context", "introduction", "background", "unstructured content"]:
                    main_section = section
                    break
            
            if main_section:
                enhancements.append({
                    "type": "update_objective",
                    "description": "Update the prompt objective",
                    "section": main_section["name"],
                    "content": objective
                })
            else:
                enhancements.append({
                    "type": "update_objective",
                    "description": "Add new objective",
                    "section": "Context",
                    "content": f"# Context\n{objective}"
                })
        
        # If specific improvements are requested but not covered by issues
        if desired_improvements:
            for improvement in desired_improvements:
                # Skip if already handled through issues
                if any(e["type"] == f"fix_{improvement}" for e in enhancements):
                    continue
                    
                if improvement == "add_examples" and "missing_examples" not in [i["type"] for i in analysis["issues"]]:
                    enhancements.append({
                        "type": "add_examples",
                        "description": "Add examples to illustrate expected output",
                        "section": "Examples",
                        "content": "# Examples\nHere are some examples of the expected output:\n\nExample 1: [Example details]"
                    })
                elif improvement == "add_constraints" and not any(s["name"].lower() == "constraints" for s in analysis["sections"]):
                    enhancements.append({
                        "type": "add_constraints",
                        "description": "Add constraints section to clarify limitations",
                        "section": "Constraints",
                        "content": "# Constraints\nPlease consider the following constraints:\n\n- [Constraint 1]\n- [Constraint 2]"
                    })
        
        return enhancements
    
    def _generate_content_for_issue(self, issue_type: str, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate suggested content for fixing a specific issue."""
        if issue_type == "missing_context":
            return "# Context\nThis task involves [describe task objective and context]."
            
        elif issue_type == "vague_instructions":
            return "# Instructions\n1. [Specific instruction 1]\n2. [Specific instruction 2]\n3. [Specific instruction 3]"
            
        elif issue_type == "missing_examples":
            if analysis["domain"] == "software":
                return "# Examples\nExample input:\n```\n[sample input]\n```\n\nExample output:\n```\n[expected output]\n```"
            else:
                return "# Examples\nExample 1: [detailed example with explanation]\nExample 2: [another example showing a different case]"
                
        elif issue_type == "missing_output_format":
            if analysis["domain"] == "software":
                return "# Expected Output Format\nProvide your solution as [output format details]."
            elif analysis["domain"] == "content":
                return "# Output Format\nYour response should include:\n- [Section 1]\n- [Section 2]\n- [Section 3]"
            else:
                return "# Expected Output\nPlease structure your response in the following format:\n1. [First component]\n2. [Second component]"
                
        elif issue_type == "no_sections":
            # Extract main content and create basic sections
            return "# Context\n[Context goes here]\n\n# Instructions\n[Instructions go here]\n\n# Output Format\n[Output format goes here]"
            
        return f"[Suggested content for {issue_type}]"
    
    def _apply_enhancements(self, original_prompt: str, enhancements: List[Dict[str, Any]]) -> str:
        """
        Apply enhancements to create a refined prompt.
        
        Args:
            original_prompt: The original prompt text
            enhancements: List of enhancements to apply
            
        Returns:
            Refined prompt text
        """
        # Start with original prompt
        refined_prompt = original_prompt
        
        # Simple application - in reality, this would be more sophisticated
        # to properly integrate enhancements with existing content
        for enhancement in enhancements:
            enhancement_type = enhancement["type"]
            content = enhancement["content"]
            
            if enhancement_type.startswith("fix_no_sections"):
                # Complete restructuring - replace entire prompt
                refined_prompt = content
                break
                
            elif enhancement_type.startswith("fix_") or enhancement_type.startswith("add_"):
                # Add new section to the end
                section_header = enhancement.get("section")
                if section_header and f"# {section_header}" not in refined_prompt:
                    refined_prompt += f"\n\n{content}"
                    
            elif enhancement_type == "update_objective":
                # This would need more sophisticated text manipulation
                # For simplicity, we'll just note the update
                refined_prompt += f"\n\nUpdated objective: {content}"
        
        return refined_prompt
    
    def _calculate_improvement_score(self, original_analysis: Dict[str, Any], refined_analysis: Dict[str, Any]) -> float:
        """
        Calculate a score representing the degree of improvement.
        
        Args:
            original_analysis: Analysis of the original prompt
            refined_analysis: Analysis of the refined prompt
            
        Returns:
            Improvement score between 0 and 1
        """
        original_quality = original_analysis["quality_score"]
        refined_quality = refined_analysis["quality_score"]
        
        # Calculate relative improvement
        if original_quality >= refined_quality:
            return 0.0
            
        relative_improvement = (refined_quality - original_quality) / (1.0 - original_quality)
        return relative_improvement


# Default instances for convenience
default_analyzer = PromptAnalyzer()
default_enhancer = PromptEnhancer(default_analyzer)


def analyze_prompt(prompt: str) -> Dict[str, Any]:
    """
    Convenience function to analyze a prompt using the default analyzer.
    
    Args:
        prompt: The prompt text to analyze
        
    Returns:
        Analysis results
    """
    return default_analyzer.analyze(prompt)


def enhance_prompt(prompt: str, objective: str = None, desired_improvements: List[str] = None) -> Dict[str, Any]:
    """
    Convenience function to enhance a prompt using the default enhancer.
    
    Args:
        prompt: The original prompt text
        objective: Optional new objective
        desired_improvements: Specific improvements desired
        
    Returns:
        Enhancement results
    """
    return default_enhancer.enhance(prompt, objective, desired_improvements)


class PromptRefiner:
    """
    Main class for analyzing and refining existing prompts.
    
    This is a composite class that uses both the PromptAnalyzer and PromptEnhancer
    internally to provide a complete refinement workflow.
    """
    
    def __init__(self):
        """Initialize the prompt refiner with analyzer and enhancer."""
        self.analyzer = PromptAnalyzer()
        self.enhancer = PromptEnhancer(analyzer=self.analyzer)
    
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze an existing prompt.
        
        Args:
            prompt: The prompt text to analyze
            
        Returns:
            Analysis results dictionary
        """
        return self.analyzer.analyze(prompt)
    
    def refine(self, prompt: str, objective: str = None, 
              desired_improvements: List[str] = None) -> Dict[str, Any]:
        """
        Analyze and refine an existing prompt.
        
        Args:
            prompt: The original prompt text
            objective: Optional clarifying objective for the prompt
            desired_improvements: Optional list of specific improvements to focus on
            
        Returns:
            Dictionary with refined prompt and analysis information
        """
        # First analyze the prompt
        analysis = self.analyzer.analyze(prompt)
        
        # Then enhance it
        enhancement_result = self.enhancer.enhance(
            prompt=prompt,
            objective=objective,
            desired_improvements=desired_improvements
        )
        
        return {
            "original_prompt": prompt,
            "refined_prompt": enhancement_result["refined_prompt"],
            "original_analysis": analysis,
            "refined_analysis": self.analyzer.analyze(enhancement_result["refined_prompt"]),
            "improvements": enhancement_result["enhancements"],
            "improvement_score": enhancement_result["improvement_score"]
        }
    
    def suggest_improvements(self, prompt: str) -> List[str]:
        """
        Suggest potential improvements for a prompt without making changes.
        
        Args:
            prompt: The prompt text to analyze
            
        Returns:
            List of suggested improvement descriptions
        """
        analysis = self.analyzer.analyze(prompt)
        suggestions = []
        
        # Convert issues to suggestions
        for issue in analysis["issues"]:
            if issue["type"] == "missing_context":
                suggestions.append("Add background information and context")
            elif issue["type"] == "vague_instructions":
                suggestions.append("Provide more specific instructions")
            elif issue["type"] == "missing_examples":
                suggestions.append("Include examples to guide the response")
            elif issue["type"] == "missing_output_format":
                suggestions.append("Specify the desired output format")
            elif issue["type"] == "no_sections":
                suggestions.append("Organize the prompt into clear sections")
        
        # Additional suggestions based on other factors
        if analysis["complexity"] < 3:
            suggestions.append("Add more detail to increase prompt complexity")
        if analysis["word_count"] < 100:
            suggestions.append("Expand the prompt with more information")
        if len(analysis["sections"]) < 3:
            suggestions.append("Add more sections to better structure the prompt")
            
        return suggestions 