"""
Technique selector for the AI Prompt Generator.

This module provides functionality to select the most appropriate
prompting techniques based on the task domain, complexity, and other factors.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from promptgen.techniques.library import PromptTechnique, default_library


class TechniqueSelector:
    """
    Selects appropriate prompting techniques based on task characteristics.
    """
    
    def __init__(self, technique_library=None):
        """
        Initialize a technique selector.
        
        Args:
            technique_library: Library of available techniques (uses default if None)
        """
        self.library = technique_library or default_library
        
        # Default technique weights by domain
        self.domain_technique_weights = {
            "software": {
                "chain_of_thought": 0.9,
                "role_prompting": 0.8,
                "few_shot": 0.7,
                "xml_tagging": 0.7,
                "tree_of_thoughts": 0.6,
                "react": 0.6,
                "prompt_chaining": 0.8,
                "graph_prompting": 0.6
            },
            "content": {
                "role_prompting": 0.9,
                "few_shot": 0.8,
                "generate_knowledge": 0.7,
                "directional_stimulus": 0.7,
                "prefill_response": 0.6,
                "reflexion": 0.5
            },
            "business": {
                "chain_of_thought": 0.8,
                "role_prompting": 0.9,
                "few_shot": 0.6,
                "tree_of_thoughts": 0.7,
                "self_consistency": 0.6,
                "graph_prompting": 0.7
            },
            "education": {
                "chain_of_thought": 0.9,
                "few_shot": 0.9,
                "generate_knowledge": 0.8,
                "prefill_response": 0.7
            },
            "creative": {
                "directional_stimulus": 0.9,
                "tree_of_thoughts": 0.8,
                "meta_prompting": 0.7,
                "role_prompting": 0.7,
                "active_prompt": 0.6
            }
        }
        
        # Default task-specific technique mappings
        self.task_technique_mappings = {
            "coding": ["chain_of_thought", "few_shot", "xml_tagging"],
            "debugging": ["react", "chain_of_thought", "self_consistency"],
            "architecture": ["tree_of_thoughts", "graph_prompting", "prompt_chaining"],
            "content_writing": ["role_prompting", "generate_knowledge", "prefill_response"],
            "marketing": ["directional_stimulus", "few_shot", "role_prompting"],
            "analysis": ["chain_of_thought", "graph_prompting", "generate_knowledge"],
            "decision_making": ["tree_of_thoughts", "self_consistency", "reflexion"],
            "creative_writing": ["directional_stimulus", "meta_prompting", "active_prompt"],
            "research": ["generate_knowledge", "react", "prompt_chaining"],
            "explanation": ["chain_of_thought", "few_shot", "prefill_response"]
        }
        
        # Complexity-based technique recommendations
        self.complexity_techniques = {
            1: ["role_prompting", "few_shot"],  # Simple tasks
            2: ["role_prompting", "few_shot", "chain_of_thought"],
            3: ["chain_of_thought", "role_prompting", "few_shot", "xml_tagging"],
            4: ["tree_of_thoughts", "self_consistency", "prompt_chaining", "chain_of_thought"],
            5: ["tree_of_thoughts", "react", "prompt_chaining", "graph_prompting", "self_consistency"]  # Complex tasks
        }
    
    def extract_keywords(self, objective: str) -> List[str]:
        """
        Extract relevant keywords from the objective.
        
        Args:
            objective: User-provided objective text
            
        Returns:
            List of extracted keywords
        """
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', objective.lower())
        
        # Filter out common stop words
        stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
            'be', 'been', 'being', 'to', 'from', 'for', 'with', 'by', 'about', 
            'against', 'between', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'on', 'off', 'over', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'any', 'both', 'each', 'few', 'more', 'most', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
            's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'i', 'me',
            'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
            'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
            'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',
            'them', 'their', 'theirs', 'themselves'
        }
        
        return [word for word in words if word not in stop_words]
    
    def determine_domain(self, objective: str, keywords: List[str] = None) -> Tuple[str, float]:
        """
        Determine the most likely domain for the objective.
        
        Args:
            objective: User-provided objective text
            keywords: Optional pre-extracted keywords
            
        Returns:
            Tuple of (domain, confidence)
        """
        keywords = keywords or self.extract_keywords(objective)
        
        # Domain-specific keyword sets
        domain_keywords = {
            "software": {
                'code', 'programming', 'developer', 'software', 'app', 'application',
                'website', 'web', 'api', 'database', 'frontend', 'backend', 'fullstack',
                'algorithm', 'function', 'class', 'object', 'method', 'variable',
                'library', 'framework', 'module', 'component', 'debugging', 'testing',
                'deployment', 'architecture', 'system', 'interface', 'user', 'authentication',
                'authorization', 'security', 'performance', 'optimization', 'scalability',
                'refactoring', 'documentation', 'git', 'version', 'control', 'devops',
                'agile', 'scrum', 'sprint', 'feature', 'bug', 'issue', 'fix', 'release',
                'update', 'maintenance'
            },
            "content": {
                'content', 'writing', 'article', 'blog', 'post', 'copywriting', 'copy',
                'marketing', 'brand', 'message', 'audience', 'reader', 'headline',
                'title', 'introduction', 'conclusion', 'paragraph', 'sentence', 'grammar',
                'spelling', 'tone', 'voice', 'style', 'narrative', 'storytelling', 'story',
                'description', 'explanation', 'instruction', 'guide', 'tutorial', 'review',
                'analysis', 'comparison', 'summary', 'outline', 'draft', 'edit', 'revision',
                'proofreading', 'seo', 'keyword', 'engagement', 'click', 'conversion', 'call',
                'action', 'persuasive', 'convincing', 'compelling', 'email', 'newsletter',
                'social', 'media', 'facebook', 'twitter', 'instagram', 'linkedin'
            },
            "business": {
                'business', 'strategy', 'plan', 'model', 'company', 'organization',
                'management', 'leadership', 'executive', 'ceo', 'cfo', 'coo', 'hr',
                'human', 'resources', 'recruitment', 'hiring', 'employee', 'team',
                'department', 'division', 'project', 'product', 'service', 'customer',
                'client', 'vendor', 'supplier', 'partner', 'stakeholder', 'investor',
                'shareholder', 'profit', 'revenue', 'sales', 'marketing', 'advertising',
                'promotion', 'branding', 'market', 'industry', 'sector', 'competitor',
                'competition', 'advantage', 'growth', 'expansion', 'merger', 'acquisition',
                'startup', 'entrepreneur', 'venture', 'capital', 'funding', 'investment',
                'finance', 'accounting', 'budget', 'forecast', 'analysis', 'report', 'data',
                'metric', 'kpi', 'goal', 'objective', 'mission', 'vision', 'value', 'culture'
            },
            "creative": {
                'creative', 'art', 'design', 'graphic', 'illustration', 'drawing', 'painting',
                'sketch', 'concept', 'idea', 'inspiration', 'imagination', 'innovative',
                'original', 'unique', 'novel', 'story', 'fiction', 'narrative', 'character',
                'plot', 'setting', 'theme', 'genre', 'poem', 'poetry', 'verse', 'stanza',
                'rhyme', 'rhythm', 'meter', 'metaphor', 'simile', 'imagery', 'symbolism',
                'music', 'song', 'melody', 'harmony', 'rhythm', 'lyric', 'composition',
                'performance', 'film', 'movie', 'cinema', 'screenplay', 'script', 'scene',
                'dialogue', 'monologue', 'photography', 'photo', 'picture', 'image', 'shot',
                'angle', 'lighting', 'composition', 'filter', 'fashion', 'style', 'trend'
            },
            "education": {
                'education', 'learning', 'teaching', 'school', 'university', 'college',
                'academy', 'institute', 'student', 'teacher', 'professor', 'instructor',
                'tutor', 'mentor', 'course', 'class', 'lecture', 'lesson', 'tutorial',
                'curriculum', 'syllabus', 'assignment', 'homework', 'project', 'exam',
                'test', 'quiz', 'grade', 'score', 'assessment', 'evaluation', 'feedback',
                'study', 'research', 'thesis', 'dissertation', 'degree', 'diploma',
                'certificate', 'qualification', 'knowledge', 'skill', 'ability', 'competence',
                'literacy', 'numeracy', 'subject', 'discipline', 'topic', 'concept', 'theory',
                'principle', 'method', 'technique', 'approach', 'pedagogy', 'andragogy',
                'elearning', 'online', 'distance', 'remote', 'classroom', 'lecture', 'hall'
            }
        }
        
        # Count matches for each domain
        domain_scores = {domain: 0 for domain in domain_keywords}
        
        for keyword in keywords:
            for domain, keyword_set in domain_keywords.items():
                if keyword in keyword_set:
                    domain_scores[domain] += 1
        
        # Find the domain with the highest score
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        
        # Adjust domain based on common phrases
        software_phrases = ['web app', 'mobile app', 'code', 'program', 'develop software', 'build an app']
        content_phrases = ['write an article', 'blog post', 'content strategy', 'marketing copy']
        business_phrases = ['business plan', 'marketing strategy', 'financial analysis']
        creative_phrases = ['design a logo', 'write a story', 'create artwork']
        education_phrases = ['lesson plan', 'teaching material', 'learning module']
        
        for phrase in software_phrases:
            if phrase in objective.lower():
                domain_scores["software"] += 3
                
        for phrase in content_phrases:
            if phrase in objective.lower():
                domain_scores["content"] += 3
                
        for phrase in business_phrases:
            if phrase in objective.lower():
                domain_scores["business"] += 3
                
        for phrase in creative_phrases:
            if phrase in objective.lower():
                domain_scores["creative"] += 3
                
        for phrase in education_phrases:
            if phrase in objective.lower():
                domain_scores["education"] += 3
        
        # Recalculate best domain
        total_score = sum(domain_scores.values()) or 1  # Avoid division by zero
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        confidence = best_domain[1] / total_score
        
        # Default to "software" with low confidence if no clear domain is detected
        if best_domain[1] == 0:
            return "software", 0.3
        
        return best_domain[0], confidence
    
    def determine_task(self, objective: str, domain: str, keywords: List[str] = None) -> str:
        """
        Determine the specific task within a domain.
        
        Args:
            objective: User-provided objective text
            domain: Previously determined domain
            keywords: Optional pre-extracted keywords
            
        Returns:
            Task identifier
        """
        keywords = keywords or self.extract_keywords(objective)
        
        # Domain-specific task mappings
        task_keywords = {
            "software": {
                "coding": ['code', 'program', 'implement', 'build', 'develop', 'create', 'function'],
                "debugging": ['debug', 'fix', 'issue', 'problem', 'error', 'bug', 'exception'],
                "architecture": ['architecture', 'design', 'structure', 'system', 'component', 'pattern']
            },
            "content": {
                "content_writing": ['write', 'article', 'blog', 'post', 'content', 'copy'],
                "marketing": ['marketing', 'ad', 'advertisement', 'campaign', 'promotion'],
                "research": ['research', 'analyze', 'find', 'discover', 'investigate']
            },
            "business": {
                "analysis": ['analyze', 'analysis', 'evaluate', 'assess', 'measure'],
                "decision_making": ['decide', 'decision', 'choice', 'select', 'determine', 'strategy'],
                "planning": ['plan', 'strategy', 'roadmap', 'forecast', 'projection']
            },
            "creative": {
                "creative_writing": ['story', 'novel', 'poem', 'fiction', 'narrative', 'character'],
                "design": ['design', 'visual', 'graphics', 'layout', 'style', 'look'],
                "brainstorming": ['idea', 'concept', 'brainstorm', 'innovate', 'think', 'creative']
            },
            "education": {
                "explanation": ['explain', 'describe', 'clarify', 'teach', 'instruct'],
                "curriculum": ['course', 'curriculum', 'lesson', 'module', 'program', 'syllabus'],
                "assessment": ['test', 'quiz', 'exam', 'assessment', 'evaluate', 'measure']
            }
        }
        
        # Check for task-specific keywords
        task_scores = {}
        
        # Initialize scores for the current domain
        if domain in task_keywords:
            for task in task_keywords[domain]:
                task_scores[task] = 0
                
            # Count matches for each task in the domain
            for keyword in keywords:
                for task, task_keyword_set in task_keywords[domain].items():
                    if keyword in task_keyword_set:
                        task_scores[task] += 1
            
            # Find the task with the highest score
            if task_scores:
                best_task = max(task_scores.items(), key=lambda x: x[1])
                if best_task[1] > 0:
                    return best_task[0]
        
        # Default tasks by domain if no clear task is detected
        default_tasks = {
            "software": "coding",
            "content": "content_writing",
            "business": "analysis",
            "creative": "creative_writing",
            "education": "explanation"
        }
        
        return default_tasks.get(domain, "general")
    
    def estimate_complexity(self, objective: str, domain: str, task: str) -> int:
        """
        Estimate the complexity of the task on a scale of 1-5.
        
        Args:
            objective: User-provided objective text
            domain: Determined domain
            task: Determined task
            
        Returns:
            Complexity score (1-5)
        """
        # Start with a base complexity of 3 (medium)
        complexity = 3
        
        # Adjust based on length (longer objectives tend to be more complex)
        words = objective.split()
        if len(words) < 10:
            complexity -= 1
        elif len(words) > 30:
            complexity += 1
        
        # Adjust based on complexity indicators
        complexity_indicators = {
            "simple": -1,
            "easy": -1,
            "basic": -1,
            "straightforward": -1,
            "complex": 1,
            "advanced": 1,
            "sophisticated": 1,
            "comprehensive": 1,
            "detailed": 1,
            "intricate": 1,
            "challenging": 1,
            "difficult": 1
        }
        
        for word, adjustment in complexity_indicators.items():
            if word in objective.lower():
                complexity += adjustment
        
        # Adjust based on domain and task
        domain_task_complexity = {
            "software": {
                "architecture": 1,  # Software architecture tends to be more complex
                "debugging": 0      # Neutral
            },
            "business": {
                "analysis": 1      # Business analysis tends to be more complex
            }
        }
        
        if domain in domain_task_complexity and task in domain_task_complexity[domain]:
            complexity += domain_task_complexity[domain][task]
        
        # Ensure complexity stays within bounds
        return max(1, min(5, complexity))
    
    def select_techniques(self, 
                         objective: str, 
                         domain: str = None, 
                         task: str = None, 
                         complexity: int = None, 
                         max_techniques: int = 3) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Select appropriate techniques based on the objective characteristics.
        
        Args:
            objective: User-provided objective text
            domain: Optional pre-determined domain (auto-detected if None)
            task: Optional pre-determined task (auto-detected if None)
            complexity: Optional pre-determined complexity (auto-detected if None)
            max_techniques: Maximum number of techniques to select
            
        Returns:
            List of tuples of (technique_name, context_dict)
        """
        # Extract keywords from the objective
        keywords = self.extract_keywords(objective)
        
        # Determine domain if not provided
        if domain is None:
            domain, confidence = self.determine_domain(objective, keywords)
        
        # Determine task if not provided
        if task is None:
            task = self.determine_task(objective, domain, keywords)
        
        # Estimate complexity if not provided
        if complexity is None:
            complexity = self.estimate_complexity(objective, domain, task)
        
        # Candidate techniques with scores
        candidate_techniques = {}
        
        # 1. Add domain-weighted techniques
        if domain in self.domain_technique_weights:
            for technique, weight in self.domain_technique_weights[domain].items():
                candidate_techniques[technique] = weight
        
        # 2. Add task-specific techniques
        if task in self.task_technique_mappings:
            for technique in self.task_technique_mappings[task]:
                candidate_techniques[technique] = candidate_techniques.get(technique, 0) + 0.5
        
        # 3. Add complexity-based techniques
        if complexity in self.complexity_techniques:
            for technique in self.complexity_techniques[complexity]:
                candidate_techniques[technique] = candidate_techniques.get(technique, 0) + 0.3
        
        # Sort techniques by score (descending)
        sorted_techniques = sorted(candidate_techniques.items(), key=lambda x: x[1], reverse=True)
        
        # Select top techniques up to max_techniques
        selected_techniques = []
        
        # Check compatibility between techniques
        for technique_name, _ in sorted_techniques:
            # Skip if we already have enough techniques
            if len(selected_techniques) >= max_techniques:
                break
                
            technique = self.library.get(technique_name)
            if not technique:
                continue
                
            # Check compatibility with already selected techniques
            compatible = True
            for selected_name, _ in selected_techniques:
                selected_technique = self.library.get(selected_name)
                if (selected_name not in technique.compatibility and 
                    technique_name not in selected_technique.compatibility):
                    compatible = False
                    break
                    
            if compatible:
                # Add technique with appropriate context
                context = self._get_technique_context(technique_name, domain, task, objective)
                selected_techniques.append((technique_name, context))
        
        return selected_techniques[:max_techniques]
    
    def _get_technique_context(self, technique_name: str, domain: str, task: str, objective: str) -> Dict[str, Any]:
        """
        Generate appropriate context parameters for a technique.
        
        Args:
            technique_name: Name of the technique
            domain: Determined domain
            task: Determined task
            objective: User-provided objective
            
        Returns:
            Dictionary of context parameters
        """
        context = {}
        
        # Role prompting contexts by domain
        if technique_name == "role_prompting":
            domain_roles = {
                "software": {
                    "role": "experienced software developer",
                    "expertise": "writing clean, efficient, and maintainable code"
                },
                "content": {
                    "role": "professional content strategist",
                    "expertise": "creating engaging and effective content"
                },
                "business": {
                    "role": "seasoned business consultant",
                    "expertise": "developing effective business strategies and solutions"
                },
                "creative": {
                    "role": "creative professional",
                    "expertise": "generating innovative and impactful creative work"
                },
                "education": {
                    "role": "experienced educator",
                    "expertise": "explaining complex concepts clearly and effectively"
                }
            }
            
            if domain in domain_roles:
                context.update(domain_roles[domain])
        
        # Few-shot examples by domain and task
        elif technique_name == "few_shot":
            # This would be expanded with actual examples in a production system
            context["examples"] = []
        
        # Chain of thought configuration
        elif technique_name == "chain_of_thought":
            context["steps_format"] = "numbered"
            context["reasoning_depth"] = "detailed" if "explain" in objective.lower() else "standard"
        
        # Tree of thoughts configuration
        elif technique_name == "tree_of_thoughts":
            context["num_paths"] = 3
            
            if domain == "business":
                context["evaluation_criteria"] = "feasibility, impact, and cost-effectiveness"
            elif domain == "software":
                context["evaluation_criteria"] = "efficiency, maintainability, and scalability"
            else:
                context["evaluation_criteria"] = "correctness, efficiency, and simplicity"
        
        # React configuration
        elif technique_name == "react":
            if domain == "software":
                context["available_actions"] = ["Think", "Research", "Code", "Test", "Debug", "Refactor"]
            elif domain == "content":
                context["available_actions"] = ["Think", "Research", "Outline", "Draft", "Edit", "Finalize"]
            elif domain == "business":
                context["available_actions"] = ["Think", "Analyze", "Research", "Calculate", "Recommend", "Evaluate"]
        
        return context 