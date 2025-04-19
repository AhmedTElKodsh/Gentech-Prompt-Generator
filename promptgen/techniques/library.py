"""
Library of prompting techniques for the AI Prompt Generator.

This module defines the PromptTechnique class and related components
for managing and applying different prompting techniques to templates.
"""

import os
import yaml
from typing import Dict, List, Any, Optional, Union, Callable


class PromptTechnique:
    """
    Base class for all prompting techniques.
    
    A prompting technique represents a specific approach to structuring
    or formatting a prompt to improve LLM responses.
    """

    def __init__(self, 
                 name: str, 
                 description: str, 
                 template: str,
                 example: str = "",
                 applicability: List[str] = None,
                 compatibility: List[str] = None,
                 parameters: Dict[str, Any] = None):
        """
        Initialize a prompting technique.
        
        Args:
            name: Unique identifier for the technique
            description: Human-readable description of the technique
            template: Template string for applying the technique
            example: Example of the technique in use
            applicability: List of domains or tasks where technique is useful
            compatibility: List of other techniques this works well with
            parameters: Optional parameters for customizing the technique
        """
        self.name = name
        self.description = description
        self.template = template
        self.example = example
        self.applicability = applicability or []
        self.compatibility = compatibility or []
        self.parameters = parameters or {}
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """
        Apply this technique to the given prompt content with context.
        
        Args:
            prompt_content: Original prompt content to enhance
            context: Additional context for applying the technique
            
        Returns:
            Enhanced prompt content with the technique applied
        """
        context = context or {}
        params = {**self.parameters, **context}
        
        # Basic template substitution - subclasses can override for more complex behavior
        try:
            return self.template.format(content=prompt_content, **params)
        except KeyError as e:
            # Fall back to original content if formatting fails
            print(f"Warning: Failed to apply technique {self.name}. Missing parameter: {e}")
            return prompt_content
    
    def is_applicable(self, domain: str, task: str, complexity: int) -> bool:
        """
        Check if this technique is applicable to the given domain, task, and complexity.
        
        Args:
            domain: Domain of the prompt (e.g., 'software', 'content')
            task: Specific task within the domain
            complexity: Complexity level (1-5)
            
        Returns:
            Boolean indicating whether the technique is applicable
        """
        # Check domain and task applicability
        if not self.applicability:
            return True  # If no specific applicability defined, assume generally applicable
        
        return (domain in self.applicability or 
                task in self.applicability or 
                f"{domain}_{task}" in self.applicability)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the technique to a dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "template": self.template,
            "example": self.example,
            "applicability": self.applicability,
            "compatibility": self.compatibility,
            "parameters": self.parameters
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PromptTechnique':
        """Create a technique instance from a dictionary representation."""
        return cls(
            name=data["name"],
            description=data["description"],
            template=data["template"],
            example=data.get("example", ""),
            applicability=data.get("applicability", []),
            compatibility=data.get("compatibility", []),
            parameters=data.get("parameters", {})
        )


# Specialized technique classes for different technique types

class ChainOfThoughtTechnique(PromptTechnique):
    """
    Chain of Thought technique guides the LLM to break down complex problems into steps.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply chain-of-thought reasoning to the prompt."""
        context = context or {}
        steps_format = context.get("steps_format", "numbered")
        reasoning_depth = context.get("reasoning_depth", "detailed")
        
        cot_prefix = "Let's think through this step-by-step:\n\n"
        
        if steps_format == "numbered":
            cot_steps = "1. Understand the problem\n2. Break it down into components\n3. Address each component systematically\n"
        else:
            cot_steps = "First, understand the problem. Then, break it down into components. Finally, address each component systematically.\n"
            
        if reasoning_depth == "detailed":
            cot_suffix = "\nMake sure to explain your reasoning at each step before moving to the next one."
        else:
            cot_suffix = "\nBriefly note your reasoning at each step."
            
        return f"{prompt_content}\n\n{cot_prefix}{cot_steps}{cot_suffix}"


class RolePromptingTechnique(PromptTechnique):
    """
    Role prompting assigns a specific role or persona to the LLM.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply role prompting to the prompt."""
        context = context or {}
        role = context.get("role", "expert")
        expertise = context.get("expertise", "")
        
        role_prefix = f"You are an {role}"
        if expertise:
            role_prefix += f" with expertise in {expertise}"
        role_prefix += ".\n\n"
        
        return f"{role_prefix}{prompt_content}"


class FewShotTechnique(PromptTechnique):
    """
    Few-shot prompting provides examples to guide the LLM response.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply few-shot examples to the prompt."""
        context = context or {}
        examples = context.get("examples", [])
        
        if not examples:
            return prompt_content
            
        few_shot_prefix = "Here are some examples of what I'm looking for:\n\n"
        
        example_text = ""
        for i, example in enumerate(examples):
            example_text += f"Example {i+1}:\nInput: {example.get('input', '')}\nOutput: {example.get('output', '')}\n\n"
            
        return f"{few_shot_prefix}{example_text}Now, apply a similar approach to the following:\n\n{prompt_content}"


class XMLTaggingTechnique(PromptTechnique):
    """
    XML tagging structures the prompt and response using XML tags.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply XML tagging to the prompt."""
        context = context or {}
        tags = context.get("tags", ["<input>", "<output>"])
        
        # If no specific tags provided, use default input/output structure
        if not tags or len(tags) < 2:
            return f"<input>\n{prompt_content}\n</input>\n\nPlease provide your response in <output> tags."
            
        # For specific tag structures
        result = prompt_content
        for tag in tags:
            # Strip angle brackets for the section name
            section_name = tag.strip("<>").capitalize()
            result += f"\n\nPlease include a {section_name} section using {tag} tags in your response."
            
        return result


class TechniqueLibrary:
    """
    Manages a collection of prompting techniques and provides methods
    for loading, retrieving, and applying them.
    """
    
    def __init__(self, techniques_dir: str = None):
        """
        Initialize the technique library.
        
        Args:
            techniques_dir: Directory containing technique definition files
        """
        self.techniques: Dict[str, PromptTechnique] = {}
        self.techniques_dir = techniques_dir
        
        # Register built-in techniques
        self._register_builtin_techniques()
        
        # Load techniques from directory if provided
        if techniques_dir and os.path.exists(techniques_dir):
            self.load_techniques(techniques_dir)
    
    def _register_builtin_techniques(self):
        """Register built-in technique implementations."""
        self.register(ChainOfThoughtTechnique(
            name="chain_of_thought",
            description="Guides the model to break down complex problems into logical steps",
            template="{content}\n\nThink through this step-by-step.",
            applicability=["complex_problems", "reasoning", "math", "coding"],
            compatibility=["role_prompting", "few_shot"]
        ))
        
        self.register(RolePromptingTechnique(
            name="role_prompting",
            description="Assigns a specific role to the model to guide its responses",
            template="You are an {role} with expertise in {expertise}.\n\n{content}",
            applicability=["all"],
            compatibility=["chain_of_thought", "few_shot", "xml_tagging"]
        ))
        
        self.register(FewShotTechnique(
            name="few_shot",
            description="Provides examples to demonstrate the expected input-output pattern",
            template="Here are some examples:\n{examples}\n\nNow, apply this to: {content}",
            applicability=["all"],
            compatibility=["role_prompting", "chain_of_thought"]
        ))
        
        self.register(XMLTaggingTechnique(
            name="xml_tagging",
            description="Structures prompt and expected response using XML tags",
            template="<instruction>\n{content}\n</instruction>\n\nProvide your response using appropriate XML tags.",
            applicability=["structured_output", "parsing"],
            compatibility=["role_prompting", "few_shot"]
        ))
    
    def register(self, technique: PromptTechnique) -> None:
        """
        Register a new technique in the library.
        
        Args:
            technique: PromptTechnique instance to register
        """
        self.techniques[technique.name] = technique
    
    def get(self, technique_name: str, context: Dict[str, Any] = None) -> Optional[PromptTechnique]:
        """
        Get a technique by name with optional context.
        
        Args:
            technique_name: Name of the technique to retrieve
            context: Optional context to customize the technique
            
        Returns:
            PromptTechnique instance or None if not found
        """
        technique = self.techniques.get(technique_name)
        if technique and context:
            # Create a copy with customized parameters
            technique_dict = technique.to_dict()
            technique_dict["parameters"] = {**technique_dict.get("parameters", {}), **context}
            return type(technique).from_dict(technique_dict)
        return technique
    
    def list_techniques(self) -> List[str]:
        """Get a list of all registered technique names."""
        return list(self.techniques.keys())
    
    def load_techniques(self, directory: str) -> None:
        """
        Load technique definitions from YAML files in the specified directory.
        
        Args:
            directory: Directory containing technique YAML files
        """
        if not os.path.exists(directory):
            print(f"Warning: Techniques directory {directory} does not exist")
            return
            
        for filename in os.listdir(directory):
            if not filename.endswith(('.yaml', '.yml')):
                continue
                
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as f:
                    technique_data = yaml.safe_load(f)
                    
                if isinstance(technique_data, list):
                    for t_data in technique_data:
                        self.register(PromptTechnique.from_dict(t_data))
                elif isinstance(technique_data, dict):
                    self.register(PromptTechnique.from_dict(technique_data))
                    
            except Exception as e:
                print(f"Error loading technique from {file_path}: {str(e)}")
    
    def find_techniques(self, domain: str, task: str, complexity: int) -> List[PromptTechnique]:
        """
        Find applicable techniques for the given context.
        
        Args:
            domain: Domain of the prompt (e.g., 'software', 'content')
            task: Specific task within the domain
            complexity: Complexity level (1-5)
            
        Returns:
            List of applicable techniques
        """
        return [
            technique for technique in self.techniques.values()
            if technique.is_applicable(domain, task, complexity)
        ]


# Global instance for convenience
default_library = TechniqueLibrary()


def get_technique(name: str, context: Dict[str, Any] = None) -> Optional[PromptTechnique]:
    """
    Convenience function to get a technique from the default library.
    
    Args:
        name: Name of the technique
        context: Optional context to customize the technique
        
    Returns:
        PromptTechnique instance or None
    """
    return default_library.get(name, context)


def apply_technique(technique_name: str, prompt_content: str, context: Dict[str, Any] = None) -> str:
    """
    Apply a technique to prompt content by name.
    
    Args:
        technique_name: Name of the technique to apply
        prompt_content: Prompt content to enhance
        context: Optional context for technique application
        
    Returns:
        Enhanced prompt content
    """
    technique = get_technique(technique_name, context)
    if not technique:
        return prompt_content  # Return original if technique not found
    return technique.apply(prompt_content, context) 