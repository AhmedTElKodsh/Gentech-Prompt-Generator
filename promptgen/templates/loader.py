"""
Template loader for the AI Prompt Generator.

This module provides functionality to load prompt templates from YAML files
and apply selected techniques to them.
"""

import os
import yaml
import re
from typing import Dict, List, Any, Optional, Tuple, Union
from promptgen.techniques.library import PromptTechnique, default_library


class PromptTemplate:
    """
    Represents a prompt template with sections and metadata.
    """
    
    def __init__(self, 
                 name: str, 
                 domain: str,
                 description: str = "",
                 complexity_range: Tuple[int, int] = (1, 5),
                 tags: List[str] = None,
                 sections: List[Dict[str, Any]] = None,
                 best_practices: List[str] = None,
                 prompt_techniques: List[Dict[str, Any]] = None,
                 conditional_sections: List[Dict[str, Any]] = None):
        """
        Initialize a prompt template.
        
        Args:
            name: Name of the template
            domain: Domain the template is for (e.g., 'software', 'content')
            description: Description of the template
            complexity_range: Min and max complexity this template supports
            tags: List of tags for categorization
            sections: List of section definitions
            best_practices: List of domain-specific best practices
            prompt_techniques: List of associated prompting techniques
            conditional_sections: Sections that are conditionally included
        """
        self.name = name
        self.domain = domain
        self.description = description
        self.complexity_range = complexity_range
        self.tags = tags or []
        self.sections = sections or []
        self.best_practices = best_practices or []
        self.prompt_techniques = prompt_techniques or []
        self.conditional_sections = conditional_sections or []
        
        # Initialize section content
        self.section_content = {}
        for section in self.sections:
            self.section_content[section['name']] = {
                'content': '',
                'populated': False
            }
    
    def is_suitable(self, domain: str, complexity: int) -> bool:
        """
        Check if this template is suitable for the given domain and complexity.
        
        Args:
            domain: Domain to check
            complexity: Complexity level to check
            
        Returns:
            Boolean indicating suitability
        """
        # Check domain match
        if self.domain != domain:
            return False
            
        # Check complexity range
        min_complexity, max_complexity = self.complexity_range
        return min_complexity <= complexity <= max_complexity
    
    def get_required_sections(self) -> List[str]:
        """Get names of required sections in this template."""
        return [section['name'] for section in self.sections if section.get('required', True)]
    
    def get_optional_sections(self) -> List[str]:
        """Get names of optional sections in this template."""
        return [section['name'] for section in self.sections if not section.get('required', True)]
    
    def get_section_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a section definition by name."""
        for section in self.sections:
            if section['name'] == name:
                return section
        return None
    
    def set_section_content(self, name: str, content: str) -> bool:
        """
        Set content for a specific section.
        
        Args:
            name: Section name
            content: Content for the section
            
        Returns:
            Boolean indicating success
        """
        if name in self.section_content:
            self.section_content[name]['content'] = content
            self.section_content[name]['populated'] = True
            return True
        return False
    
    def get_section_content(self, name: str) -> Optional[str]:
        """Get the content of a specific section."""
        if name in self.section_content:
            return self.section_content[name]['content']
        return None
    
    def apply_conditional_sections(self, context: Dict[str, Any]) -> None:
        """
        Apply conditional sections based on context.
        
        Args:
            context: Context dictionary with condition variables
        """
        for condition in self.conditional_sections:
            trigger = condition.get('trigger', {})
            key = trigger.get('key', '')
            value = trigger.get('value', None)
            
            # Check if condition is met
            if key in context and context[key] == value:
                # Add conditional sections
                for section_def in condition.get('add_sections', []):
                    section_name = section_def.get('name', '')
                    position = section_def.get('position', 999)  # Default to end
                    content_template = section_def.get('content_template', '')
                    
                    # Create and add the section
                    new_section = {
                        'name': section_name,
                        'position': position,
                        'required': False,
                        'description': section_def.get('description', ''),
                        'content_template': content_template
                    }
                    
                    # Add to sections list and initialize content
                    self.sections.append(new_section)
                    self.section_content[section_name] = {
                        'content': '',
                        'populated': False
                    }
        
        # Sort sections by position after adding conditionals
        self.sections.sort(key=lambda x: x.get('position', 999))
    
    def render(self, include_empty: bool = False) -> str:
        """
        Render the complete prompt with all populated sections.
        
        Args:
            include_empty: Whether to include unpopulated sections
            
        Returns:
            Rendered prompt text
        """
        # Sort sections by position
        sorted_sections = sorted(self.sections, key=lambda x: x.get('position', 999))
        
        result = []
        for section in sorted_sections:
            name = section['name']
            if name in self.section_content:
                content = self.section_content[name]['content']
                is_populated = self.section_content[name]['populated']
                
                if content and (is_populated or include_empty):
                    result.append(f"# {name}\n{content}")
        
        return "\n\n".join(result)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PromptTemplate':
        """
        Create a template from a dictionary.
        
        Args:
            data: Dictionary representation of a template
            
        Returns:
            PromptTemplate instance
        """
        return cls(
            name=data.get('name', 'Unnamed Template'),
            domain=data.get('domain', 'general'),
            description=data.get('description', ''),
            complexity_range=tuple(data.get('complexity_range', [1, 5])),
            tags=data.get('tags', []),
            sections=data.get('sections', []),
            best_practices=data.get('best_practices', []),
            prompt_techniques=data.get('prompt_techniques', []),
            conditional_sections=data.get('conditional_sections', [])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the template to a dictionary."""
        return {
            'name': self.name,
            'domain': self.domain,
            'description': self.description,
            'complexity_range': list(self.complexity_range),
            'tags': self.tags,
            'sections': self.sections,
            'best_practices': self.best_practices,
            'prompt_techniques': self.prompt_techniques,
            'conditional_sections': self.conditional_sections
        }


class TemplateLibrary:
    """
    Library of prompt templates with loading and management capabilities.
    """
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize a template library.
        
        Args:
            templates_dir: Directory containing template YAML files
        """
        self.templates: Dict[str, PromptTemplate] = {}
        self.templates_dir = templates_dir
        
        # Load templates from directory if provided
        if templates_dir and os.path.exists(templates_dir):
            self.load_templates(templates_dir)
    
    def register(self, template: PromptTemplate) -> None:
        """
        Register a template in the library.
        
        Args:
            template: PromptTemplate instance to register
        """
        self.templates[template.name] = template
    
    def get(self, template_name: str) -> Optional[PromptTemplate]:
        """
        Get a template by name.
        
        Args:
            template_name: Name of the template to retrieve
            
        Returns:
            PromptTemplate instance or None if not found
        """
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """Get a list of all registered template names."""
        return list(self.templates.keys())
    
    def load_templates(self, directory: str) -> None:
        """
        Load template definitions from YAML files in the specified directory.
        
        Args:
            directory: Directory containing template YAML files
        """
        if not os.path.exists(directory):
            print(f"Warning: Templates directory {directory} does not exist")
            return
            
        for filename in os.listdir(directory):
            if not filename.endswith(('.yaml', '.yml')):
                continue
                
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as f:
                    template_data = yaml.safe_load(f)
                    
                if isinstance(template_data, list):
                    for t_data in template_data:
                        self.register(PromptTemplate.from_dict(t_data))
                elif isinstance(template_data, dict):
                    self.register(PromptTemplate.from_dict(template_data))
                    
            except Exception as e:
                print(f"Error loading template from {file_path}: {str(e)}")
    
    def find_templates(self, domain: str, complexity: int) -> List[PromptTemplate]:
        """
        Find suitable templates for the given domain and complexity.
        
        Args:
            domain: Domain to match
            complexity: Complexity level to match
            
        Returns:
            List of suitable templates
        """
        return [
            template for template in self.templates.values()
            if template.is_suitable(domain, complexity)
        ]


class PromptGenerator:
    """
    Generates prompts by combining templates with techniques and content.
    """
    
    def __init__(self, template_library=None, technique_library=None):
        """
        Initialize a prompt generator.
        
        Args:
            template_library: Library of prompt templates (uses default if None)
            technique_library: Library of prompting techniques (uses default if None)
        """
        self.template_library = template_library or TemplateLibrary()
        self.technique_library = technique_library or default_library
    
    def populate_section(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Populate a template section with context variables.
        
        Args:
            section: Section definition
            context: Context variables for substitution
            
        Returns:
            Populated section content
        """
        template_str = section.get('content_template', '')
        if not template_str:
            return ''
            
        # Basic template substitution
        try:
            # Replace placeholders that have corresponding values in context
            for key, value in context.items():
                placeholder = '{' + key + '}'
                if placeholder in template_str:
                    template_str = template_str.replace(placeholder, str(value))
            
            # Find any remaining placeholders
            placeholders = re.findall(r'\{([^{}]+)\}', template_str)
            for placeholder in placeholders:
                # Replace with empty string if not in context
                if placeholder != 'content' and placeholder not in context:  # Skip {content} as it's special
                    template_str = template_str.replace('{' + placeholder + '}', f"[{placeholder}]")
            
            return template_str
        except Exception as e:
            print(f"Error populating section: {str(e)}")
            return template_str
    
    def apply_techniques(self, prompt: str, techniques: List[Tuple[str, Dict[str, Any]]]) -> str:
        """
        Apply a sequence of prompting techniques to a prompt.
        
        Args:
            prompt: Base prompt to enhance
            techniques: List of (technique_name, context) tuples
            
        Returns:
            Enhanced prompt
        """
        result = prompt
        
        for technique_name, context in techniques:
            technique = self.technique_library.get(technique_name, context)
            if technique:
                result = technique.apply(result, context)
        
        return result
    
    def generate_prompt(self, 
                       objective: str, 
                       domain: str,
                       task: str,
                       complexity: int,
                       context: Dict[str, Any] = None,
                       techniques: List[Tuple[str, Dict[str, Any]]] = None,
                       template_name: str = None) -> Tuple[str, PromptTemplate]:
        """
        Generate a prompt for the given objective.
        
        Args:
            objective: User-provided objective
            domain: Task domain (e.g., 'software', 'content')
            task: Specific task within the domain
            complexity: Complexity level (1-5)
            context: Additional context variables
            techniques: Optional pre-selected techniques
            template_name: Optional specific template to use
            
        Returns:
            Tuple of (generated prompt, template used)
        """
        context = context or {}
        context['objective'] = objective
        
        # Find a suitable template
        template = None
        if template_name:
            template = self.template_library.get(template_name)
        
        if not template:
            # Find templates suitable for this domain and complexity
            candidates = self.template_library.find_templates(domain, complexity)
            if candidates:
                # Select the first suitable template (could be enhanced with better selection logic)
                template = candidates[0]
            else:
                # No suitable template found
                return f"Could not find a suitable template for {domain} domain with complexity {complexity}.", None
        
        # Apply conditional sections based on context
        template.apply_conditional_sections(context)
        
        # Populate each section
        for section in template.sections:
            section_name = section['name']
            section_content = self.populate_section(section, context)
            template.set_section_content(section_name, section_content)
        
        # Render the populated template
        prompt = template.render()
        
        # Apply any specified techniques
        if techniques:
            prompt = self.apply_techniques(prompt, techniques)
        
        # Add best practices if available
        if template.best_practices:
            best_practices = "\n\n# Best Practices\n" + "\n".join(f"- {practice}" for practice in template.best_practices)
            prompt += best_practices
        
        return prompt, template


# Global instance for convenience
default_library = TemplateLibrary()


def load_template(file_path: str) -> Optional[PromptTemplate]:
    """
    Load a template from a YAML file.
    
    Args:
        file_path: Path to the template YAML file
        
    Returns:
        PromptTemplate instance or None if loading fails
    """
    try:
        with open(file_path, 'r') as f:
            template_data = yaml.safe_load(f)
        return PromptTemplate.from_dict(template_data)
    except Exception as e:
        print(f"Error loading template from {file_path}: {str(e)}")
        return None 