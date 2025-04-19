"""
Domain-specific prompt evaluation utilities for the AI Prompt Generator.

This module extends the base prompt evaluator with domain-specific evaluation
metrics tailored for different domains (software, content, business, etc.).
"""

import re
from typing import Dict, List, Any, Optional
import logging
from .evaluator import PromptEvaluator

# Setup logger
logger = logging.getLogger(__name__)

class DomainSpecificEvaluator(PromptEvaluator):
    """
    Extends the base PromptEvaluator with domain-specific evaluation metrics.
    
    This evaluator adds additional quality factors and patterns that are relevant
    to specific domains such as software development, content creation,
    business strategy, etc.
    """
    
    def __init__(self, domain: str = None, llm_client=None):
        """
        Initialize a domain-specific prompt evaluator.
        
        Args:
            domain: The domain to use for evaluation (software, content, business, etc.)
            llm_client: Client for making test requests to LLMs
        """
        super().__init__(llm_client)
        self.domain = domain
        
        # Domain-specific quality factors (will be merged with base factors)
        self.domain_quality_factors = {
            "software": {
                "technical_accuracy": 0.15,    # Correct technical terms and concepts
                "implementation_detail": 0.10,  # Appropriate level of implementation detail
                "security_consideration": 0.05, # Inclusion of security considerations
                "maintainability": 0.05,        # Code maintenance considerations
                "testability": 0.05             # Test considerations
            },
            "content": {
                "audience_focus": 0.15,         # Clear target audience specification
                "tone_consistency": 0.10,       # Appropriate and consistent tone
                "engagement_potential": 0.05,   # Elements that promote engagement
                "content_structure": 0.10,      # Logical content structure
                "seo_consideration": 0.05       # SEO optimization considerations
            },
            "business": {
                "metric_orientation": 0.15,     # Inclusion of measurable metrics/KPIs
                "stakeholder_consideration": 0.10, # Consideration of stakeholders
                "strategic_alignment": 0.10,    # Alignment with strategic objectives
                "feasibility": 0.05,            # Implementation feasibility
                "risk_assessment": 0.05         # Risk consideration
            },
            "creative": {
                "originality": 0.15,            # Emphasis on originality
                "emotional_impact": 0.10,       # Emotional response considerations
                "sensory_detail": 0.10,         # Inclusion of sensory elements
                "audience_connection": 0.05,    # Connection with audience
                "thematic_depth": 0.05          # Depth of themes or concepts
            },
            "education": {
                "learning_objectives": 0.15,    # Clear learning objectives
                "assessment_strategies": 0.10,  # Methods to assess learning
                "engagement_techniques": 0.05,  # Techniques to engage learners
                "scaffolding": 0.10,            # Progressive learning structure
                "accessibility": 0.05           # Inclusive learning considerations
            }
        }
        
        # Domain-specific patterns for evaluation
        self.domain_patterns = {
            "software": {
                "technical_accuracy": [
                    r"(?i)\b(algorithm|function|method|class|object|variable|parameter|api|interface|module|library|framework|database|query|server|client|endpoint|request|response|authentication|authorization|token|json|xml|http|rest|graphql|sdk|api|git|cloud|container|docker|kubernetes)\b",
                    r"(?i)\b(typescript|javascript|python|java|c\+\+|c#|ruby|go|rust|php|swift|kotlin|scala|sql|nosql|mongodb|mysql|postgresql|oracle|redis)\b"
                ],
                "implementation_detail": [
                    r"(?i)\b(implement|implementation|code|pseudocode|function|method|class|interface|module|import|export|require|dependency)\b",
                    r"(?i)\b(for\s+loop|while\s+loop|if\s+statement|switch\s+statement|try\s+catch|exception|error\s+handling)\b"
                ],
                "security_consideration": [
                    r"(?i)\b(security|authentication|authorization|encryption|password|hash|salt|token|jwt|oauth|xss|csrf|sql\s+injection|input\s+validation|sanitize|vulnerability|exploit|attack|firewall|protection)\b"
                ],
                "maintainability": [
                    r"(?i)\b(maintainable|readability|readable|clean\s+code|refactor|technical\s+debt|documentation|comment|test|coverage|modularity|reusable|extensible|flexible|scalable|solid\s+principles)\b"
                ],
                "testability": [
                    r"(?i)\b(test|unit\s+test|integration\s+test|e2e\s+test|mock|stub|fixture|assert|expect|should|testing\s+framework|jest|mocha|pytest|junit|testable|coverage|tdd|bdd)\b"
                ]
            },
            "content": {
                "audience_focus": [
                    r"(?i)\b(audience|reader|viewer|customer|user|demographic|target\s+market|segment|persona|profile)\b",
                    r"(?i)\b(age\s+group|gender|interest|background|knowledge\s+level|expertise|beginner|intermediate|advanced|professional)\b",
                    r"(?i)\btarget\s+audience\b"
                ],
                "tone_consistency": [
                    r"(?i)\b(tone|voice|style|formal|informal|friendly|professional|conversational|authoritative|humorous|serious|inspirational|persuasive)\b",
                    r"(?i)\b(educational|casual|encouraging|informative)\b"
                ],
                "engagement_potential": [
                    r"(?i)\b(engage|engagement|compelling|captivating|interesting|attention|hook|draw\s+in|appeal|attract|clickbait|headline|title|subtitle)\b",
                    r"(?i)\b(call-to-action|visual|bullet points|headings)\b"
                ],
                "content_structure": [
                    r"(?i)\b(introduction|body|conclusion|paragraph|section|headline|subheading|outline|format|structure|organization|flow|transition)\b",
                    r"(?i)\b(list|bullet point|numbered|steps)\b"
                ],
                "seo_consideration": [
                    r"(?i)\b(seo|search\s+engine|keyword|meta\s+description|alt\s+text|tag|ranking|serp|organic|traffic|backlink|indexing|crawl|google|algorithm)\b",
                    r"(?i)\b(seo\s+keywords|keywords)\b"
                ]
            },
            "business": {
                "metric_orientation": [
                    r"(?i)\b(kpi|metric|measure|roi|return\s+on\s+investment|revenue|profit|margin|cost|expense|budget|conversion\s+rate|ctr|cac|ltv|arpu|growth|performance|benchmark)\b",
                    r"(?i)\b(\d+%|market\s+share|percent|percentage)\b",
                    r"(?i)\b(\d+\s+year|\d+\s+month|\d+\s+quarter)\b"
                ],
                "stakeholder_consideration": [
                    r"(?i)\b(stakeholder|shareholder|investor|board|executive|management|employee|customer|client|partner|supplier|vendor|regulator|government)\b"
                ],
                "strategic_alignment": [
                    r"(?i)\b(strategy|strategic|mission|vision|goal|objective|initiative|priority|roadmap|plan|alignment|direction|positioning|competitive\s+advantage)\b"
                ],
                "feasibility": [
                    r"(?i)\b(feasible|feasibility|viable|viability|practical|practicality|implementable|achievable|realistic|attainable|executable|doable)\b"
                ],
                "risk_assessment": [
                    r"(?i)\b(risk|threat|vulnerability|mitigation|contingency|fallback|scenario|assessment|evaluation|analysis|swot|pestle|uncertainty|probability|impact)\b"
                ]
            },
            "creative": {
                "originality": [
                    r"(?i)\b(original|unique|innovative|novel|creative|imagination|inventive|fresh|new|distinctive|unconventional|perspective|angle|approach)\b"
                ],
                "emotional_impact": [
                    r"(?i)\b(emotion|feeling|mood|atmosphere|tone|evoke|inspire|move|touch|resonate|connect|impact|powerful|dramatic|tension|release|catharsis)\b"
                ],
                "sensory_detail": [
                    r"(?i)\b(visual|auditory|tactile|taste|smell|sense|sensory|image|imagery|description|vivid|texture|color|sound|scene|setting|picture|visualize)\b"
                ],
                "audience_connection": [
                    r"(?i)\b(relatable|connection|identify|relate|empathy|understand|recognition|familiar|universal|shared\s+experience|human\s+condition|resonance)\b"
                ],
                "thematic_depth": [
                    r"(?i)\b(theme|meaning|symbolism|metaphor|allegory|subtext|depth|layer|nuance|complexity|interpretation|analysis|message|significance)\b"
                ]
            },
            "education": {
                "learning_objectives": [
                    r"(?i)\b(learning\s+objective|learning\s+outcome|goal|skill|knowledge|understanding|comprehension|mastery|proficiency|competency|ability)\b"
                ],
                "assessment_strategies": [
                    r"(?i)\b(assessment|evaluation|quiz|test|exam|project|assignment|rubric|criteria|feedback|measure|gauge|check|verify|validate)\b"
                ],
                "engagement_techniques": [
                    r"(?i)\b(engage|participation|interactive|activity|exercise|discussion|collaboration|group\s+work|hands-on|practical|application|game|gamification)\b"
                ],
                "scaffolding": [
                    r"(?i)\b(scaffold|build\s+upon|foundation|prerequisite|prior\s+knowledge|progression|sequence|step-by-step|incremental|gradual|stage|phase|level)\b"
                ],
                "accessibility": [
                    r"(?i)\b(accessible|accessibility|inclusive|diversity|accommodation|adaptation|differentiation|learning\s+style|need|support|assistance)\b"
                ]
            }
        }
    
    def evaluate(self, prompt: str) -> Dict[str, Any]:
        """
        Evaluate the quality of a prompt with domain-specific metrics.
        
        Args:
            prompt: The prompt text to evaluate
            
        Returns:
            Dictionary with standard and domain-specific evaluation metrics
        """
        # Get base evaluation results
        results = super().evaluate(prompt)
        
        # If no domain is specified, return standard evaluation
        if not self.domain or self.domain not in self.domain_quality_factors:
            return results
        
        # Add domain-specific evaluation
        domain_scores = self._evaluate_domain_specific(prompt)
        
        # Calculate domain-specific quality score
        domain_quality_factors = self.domain_quality_factors.get(self.domain, {})
        domain_quality_score = sum(
            domain_scores[factor] * weight 
            for factor, weight in domain_quality_factors.items()
        )
        
        # Add domain-specific results
        results["domain"] = self.domain
        results["domain_scores"] = domain_scores
        results["domain_quality_score"] = round(domain_quality_score * 100) / 100
        
        # Calculate combined quality score (weighted average of general and domain-specific)
        combined_quality_score = (results["quality_score"] * 0.6) + (domain_quality_score * 0.4)
        results["combined_quality_score"] = round(combined_quality_score * 100) / 100
        
        # Add domain-specific suggestions
        results["domain_suggestions"] = self._generate_domain_suggestions(domain_scores)
        
        return results
    
    def _evaluate_domain_specific(self, prompt_text: str) -> Dict[str, float]:
        """
        Evaluate domain-specific qualities of a prompt.
        
        Args:
            prompt_text: Normalized prompt text
            
        Returns:
            Dictionary with scores for each domain-specific quality factor
        """
        if not self.domain or self.domain not in self.domain_patterns:
            return {}
        
        # Get domain-specific patterns
        domain_patterns = self.domain_patterns.get(self.domain, {})
        domain_factors = self.domain_quality_factors.get(self.domain, {})
        
        # Split the prompt into lines and words for analysis
        lines = prompt_text.split("\n")
        words = prompt_text.split()
        total_words = len(words)
        
        if total_words == 0:
            return {factor: 0 for factor in domain_factors}
        
        # Initialize scores
        scores = {}
        
        # Evaluate each domain-specific factor
        for factor, patterns in domain_patterns.items():
            if factor not in domain_factors:
                continue
                
            factor_matches = sum(
                1 for pattern in patterns
                for match in re.finditer(pattern, prompt_text, re.MULTILINE)
            )
            
            # Calculate factor score based on number of matches
            # Scale the divisor based on the expected prevalence of this factor
            if factor in ["technical_accuracy", "audience_focus", "metric_orientation", 
                          "originality", "learning_objectives"]:
                # These are expected to be more prevalent
                divisor = max(5, total_words * 0.03)
            else:
                # These might be less prevalent but still important
                divisor = max(3, total_words * 0.02)
                
            factor_score = min(1.0, factor_matches / divisor)
            scores[factor] = factor_score
        
        return scores
    
    def _generate_domain_suggestions(self, scores: Dict[str, float]) -> List[str]:
        """
        Generate domain-specific improvement suggestions.
        
        Args:
            scores: Domain-specific factor scores
            
        Returns:
            List of domain-specific improvement suggestions
        """
        if not self.domain:
            return []
            
        suggestions = []
        
        # Software domain suggestions
        if self.domain == "software":
            if scores.get("technical_accuracy", 1.0) < 0.6:
                suggestions.append("Include more specific technical terms relevant to the programming language or technology stack")
            
            if scores.get("implementation_detail", 1.0) < 0.6:
                suggestions.append("Provide more specific implementation guidance or code structure details")
            
            if scores.get("security_consideration", 1.0) < 0.4:
                suggestions.append("Add security considerations relevant to this development task")
            
            if scores.get("maintainability", 1.0) < 0.4:
                suggestions.append("Include guidelines for code maintainability and readability")
            
            if scores.get("testability", 1.0) < 0.4:
                suggestions.append("Add testing requirements or considerations")
                
        # Content domain suggestions
        elif self.domain == "content":
            if scores.get("audience_focus", 1.0) < 0.6:
                suggestions.append("Clearly define the target audience or reader persona")
            
            if scores.get("tone_consistency", 1.0) < 0.6:
                suggestions.append("Specify the desired tone and voice for the content")
            
            if scores.get("engagement_potential", 1.0) < 0.5:
                suggestions.append("Add elements to increase reader engagement (hooks, questions, etc.)")
            
            if scores.get("content_structure", 1.0) < 0.6:
                suggestions.append("Provide more guidance on content structure and organization")
            
            if scores.get("seo_consideration", 1.0) < 0.4:
                suggestions.append("Include SEO requirements or keyword guidance")
                
        # Business domain suggestions
        elif self.domain == "business":
            if scores.get("metric_orientation", 1.0) < 0.6:
                suggestions.append("Define specific KPIs or success metrics for this business objective")
            
            if scores.get("stakeholder_consideration", 1.0) < 0.5:
                suggestions.append("Identify key stakeholders and their interests or requirements")
            
            if scores.get("strategic_alignment", 1.0) < 0.6:
                suggestions.append("Clarify how this aligns with broader strategic objectives")
            
            if scores.get("feasibility", 1.0) < 0.5:
                suggestions.append("Address implementation feasibility and resource requirements")
            
            if scores.get("risk_assessment", 1.0) < 0.4:
                suggestions.append("Include potential risks and mitigation strategies")
                
        # Creative domain suggestions
        elif self.domain == "creative":
            if scores.get("originality", 1.0) < 0.6:
                suggestions.append("Emphasize uniqueness and originality requirements")
            
            if scores.get("emotional_impact", 1.0) < 0.5:
                suggestions.append("Specify the desired emotional response or impact")
            
            if scores.get("sensory_detail", 1.0) < 0.5:
                suggestions.append("Request inclusion of sensory details (visual, auditory, etc.)")
            
            if scores.get("audience_connection", 1.0) < 0.5:
                suggestions.append("Focus on creating connection or resonance with the audience")
            
            if scores.get("thematic_depth", 1.0) < 0.4:
                suggestions.append("Request deeper thematic exploration or symbolism")
                
        # Education domain suggestions
        elif self.domain == "education":
            if scores.get("learning_objectives", 1.0) < 0.7:
                suggestions.append("Clearly define specific learning objectives or outcomes")
            
            if scores.get("assessment_strategies", 1.0) < 0.5:
                suggestions.append("Include assessment methods to evaluate learning")
            
            if scores.get("engagement_techniques", 1.0) < 0.5:
                suggestions.append("Add engaging activities or interactive elements")
            
            if scores.get("scaffolding", 1.0) < 0.5:
                suggestions.append("Structure content with progressive complexity or scaffolding")
            
            if scores.get("accessibility", 1.0) < 0.4:
                suggestions.append("Consider accessibility and inclusive learning approaches")
        
        return suggestions

# Convenience function for quick evaluations
def evaluate_prompt_with_domain(prompt_text: str, domain: str = None, llm_client=None) -> Dict[str, Any]:
    """
    Evaluate a prompt with domain-specific metrics.
    
    Args:
        prompt_text: The prompt to evaluate
        domain: The domain to use for evaluation (software, content, business, etc.)
        llm_client: Optional LLM client for response testing
        
    Returns:
        Evaluation metrics including domain-specific scores
    """
    evaluator = DomainSpecificEvaluator(domain, llm_client)
    return evaluator.evaluate(prompt_text) 