"""
Software domain components for the AI Prompt Generator.

This module provides specialized content generators and domain knowledge
for software development and programming-related prompts.
"""

from typing import Dict, List, Any, Optional
import logging

# Setup logger
logger = logging.getLogger(__name__)


class SoftwareContentStrategy:
    """
    Strategy for generating content for software development prompts.
    
    Implements the Strategy Pattern for software-specific content population.
    """
    
    def __init__(self):
        """Initialize the software content strategy."""
        # Load best practices and domain knowledge
        self.best_practices = self._load_best_practices()
        self.language_considerations = self._load_language_considerations()
        self.architecture_patterns = self._load_architecture_patterns()
        self.testing_strategies = self._load_testing_strategies()
    
    def populate(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Populate a template section with software-specific content.
        
        Args:
            section: Template section definition
            context: Content generation context
            
        Returns:
            Generated content for the section
        """
        section_name = section.get("name", "").lower()
        
        # Different generation strategies based on section type
        if section_name in ["context", "background", "introduction"]:
            return self._generate_context_content(section, context)
            
        elif section_name in ["requirements", "specifications", "technical requirements"]:
            return self._generate_requirements_content(section, context)
            
        elif section_name in ["codestructure", "structure", "architecture"]:
            return self._generate_structure_content(section, context)
            
        elif section_name in ["bestpractices", "guidelines", "standards"]:
            return self._generate_best_practices_content(section, context)
            
        elif section_name in ["testing", "validation", "quality assurance"]:
            return self._generate_testing_content(section, context)
            
        # For other sections, use the template's default content
        return section.get("content_template", "").format(**context)
    
    def _generate_context_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for context/background sections."""
        objective = context.get("objective", "")
        language = context.get("language", "unspecified programming language")
        complexity = context.get("complexity", 3)
        
        # Customize based on context
        language_info = self.language_considerations.get(language.lower(), 
                                                       {"description": "a versatile programming language"})
        
        context_template = """
You are a senior software developer tasked with the following programming challenge:

{objective}

Technical Environment:
- Language/Platform: {language} - {language_description}
- Project Type: {project_type}
- Complexity Level: {complexity}/5
        """
        
        return context_template.format(
            objective=objective,
            language=language,
            language_description=language_info.get("description", ""),
            project_type=context.get("project_type", "Software Application"),
            complexity=complexity
        )
    
    def _generate_requirements_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for requirements sections."""
        objective = context.get("objective", "")
        language = context.get("language", "general")
        
        # Extract likely requirements based on objective
        functional_requirements = ["Implement core functionality described in the objective"]
        if "database" in objective.lower() or "data" in objective.lower():
            functional_requirements.append("Implement data storage and retrieval capabilities")
        if "api" in objective.lower() or "interface" in objective.lower():
            functional_requirements.append("Create well-defined API endpoints/interfaces")
        if "user" in objective.lower() or "ui" in objective.lower() or "interface" in objective.lower():
            functional_requirements.append("Develop user interface components")
        
        # Get language-specific technical requirements
        language_info = self.language_considerations.get(language.lower(), {})
        technical_requirements = language_info.get("best_practices", [
            "Write clean, maintainable code",
            "Follow standard conventions",
            "Include appropriate error handling",
            "Add comments for complex logic"
        ])
        
        requirements_template = """
Requirements:

1. Functional Requirements:
{functional_requirements}

2. Technical Requirements:
{technical_requirements}
{additional_requirements}
        """
        
        return requirements_template.format(
            functional_requirements="\n".join(f"   - {req}" for req in functional_requirements),
            technical_requirements="\n".join(f"   - {req}" for req in technical_requirements),
            additional_requirements=context.get("additional_requirements", "")
        )
    
    def _generate_structure_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for structure/architecture sections."""
        language = context.get("language", "").lower()
        complexity = context.get("complexity", 3)
        objective = context.get("objective", "")
        
        # Select appropriate architectural patterns based on context
        potential_patterns = []
        for pattern, details in self.architecture_patterns.items():
            pattern_complexity = details.get("complexity", 3)
            keywords = details.get("keywords", [])
            
            # Check if pattern applies to this task
            if (pattern_complexity <= complexity and 
                any(keyword in objective.lower() for keyword in keywords)):
                potential_patterns.append(pattern)
        
        # If no patterns match, suggest general structure
        if not potential_patterns:
            potential_patterns = ["Modular Design"]
        
        # Get language-specific structure recommendations
        lang_structure = self.language_considerations.get(language, {}).get("structure", [
            "Organize code into logical modules/files",
            "Separate concerns appropriately",
            "Use consistent naming conventions"
        ])
        
        structure_template = """
Code Structure:

1. Architecture Approach:
   Consider using {architecture_pattern} for this task.
   This approach is appropriate because {architecture_reason}.

2. Component Organization:
{component_organization}

3. Key Implementation Considerations:
{implementation_considerations}
        """
        
        # Get details for the first suggested pattern
        pattern_details = self.architecture_patterns.get(potential_patterns[0], {})
        
        return structure_template.format(
            architecture_pattern=potential_patterns[0],
            architecture_reason=pattern_details.get("description", "it provides a clean separation of concerns"),
            component_organization="\n".join(f"   - {item}" for item in pattern_details.get("components", ["Main component"])),
            implementation_considerations="\n".join(f"   - {item}" for item in lang_structure)
        )
    
    def _generate_best_practices_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for best practices sections."""
        language = context.get("language", "").lower()
        complexity = context.get("complexity", 3)
        
        # Get language-specific best practices
        lang_practices = self.language_considerations.get(language, {}).get("best_practices", [])
        
        # Get general best practices appropriate for the complexity level
        general_practices = []
        for practice, details in self.best_practices.items():
            if details.get("min_complexity", 1) <= complexity <= details.get("max_complexity", 5):
                general_practices.append(f"{practice}: {details.get('description', '')}")
        
        # If we have too many practices, select the most relevant ones
        if len(general_practices) > 5:
            general_practices = general_practices[:5]
        
        practices_template = """
Best Practices:

1. Language-Specific Practices:
{language_practices}

2. General Software Development Practices:
{general_practices}

3. Code Quality Considerations:
   - Write readable code with clear naming
   - Include appropriate documentation
   - Consider edge cases and error scenarios
        """
        
        return practices_template.format(
            language_practices="\n".join(f"   - {practice}" for practice in lang_practices[:3]),
            general_practices="\n".join(f"   - {practice}" for practice in general_practices)
        )
    
    def _generate_testing_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for testing sections."""
        language = context.get("language", "").lower()
        complexity = context.get("complexity", 3)
        
        # Get testing strategies appropriate for the language and complexity
        testing_approaches = []
        for strategy, details in self.testing_strategies.items():
            if (details.get("min_complexity", 1) <= complexity and
                language in details.get("applicable_languages", ["all"])):
                testing_approaches.append({
                    "name": strategy,
                    "description": details.get("description", ""),
                    "tools": details.get("tools", {}).get(language, "appropriate testing tools")
                })
        
        # Limit to the 3 most relevant testing approaches
        if testing_approaches:
            testing_approaches = testing_approaches[:3]
        else:
            # Fallback if no specific approaches found
            testing_approaches = [{
                "name": "Unit Testing",
                "description": "Testing individual components in isolation",
                "tools": "standard testing framework"
            }]
        
        testing_template = """
Testing Approach:

1. Recommended Testing Strategies:
{testing_strategies}

2. Test Coverage Considerations:
   - Aim for comprehensive coverage of core functionality
   - Include edge cases and error conditions
   - Test both expected and unexpected inputs

3. Test Implementation:
   - Write tests alongside or before code implementation
   - Automate tests where possible
   - Document test cases and expected results
        """
        
        strategies_text = ""
        for i, strategy in enumerate(testing_approaches):
            strategies_text += f"   {i+1}. {strategy['name']}: {strategy['description']}\n"
            strategies_text += f"      Tools: {strategy['tools']}\n"
        
        return testing_template.format(testing_strategies=strategies_text)
    
    def _load_best_practices(self) -> Dict[str, Any]:
        """Load software development best practices."""
        return {
            "SOLID Principles": {
                "description": "Follow Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles",
                "min_complexity": 3,
                "max_complexity": 5
            },
            "DRY (Don't Repeat Yourself)": {
                "description": "Avoid code duplication by abstracting common functionality",
                "min_complexity": 1,
                "max_complexity": 5
            },
            "KISS (Keep It Simple, Stupid)": {
                "description": "Prefer simple solutions over complex ones",
                "min_complexity": 1,
                "max_complexity": 5
            },
            "YAGNI (You Aren't Gonna Need It)": {
                "description": "Don't add functionality until it's necessary",
                "min_complexity": 2,
                "max_complexity": 5
            },
            "Use Version Control": {
                "description": "Track changes with Git or another VCS",
                "min_complexity": 1,
                "max_complexity": 5
            },
            "Defensive Programming": {
                "description": "Anticipate and handle potential errors",
                "min_complexity": 2,
                "max_complexity": 5
            },
            "Code Reviews": {
                "description": "Have others review your code for quality and correctness",
                "min_complexity": 3,
                "max_complexity": 5
            },
            "Continuous Integration": {
                "description": "Regularly merge and test code changes",
                "min_complexity": 3,
                "max_complexity": 5
            },
            "Test-Driven Development": {
                "description": "Write tests before implementing features",
                "min_complexity": 3,
                "max_complexity": 5
            }
        }
    
    def _load_language_considerations(self) -> Dict[str, Any]:
        """Load programming language-specific considerations."""
        return {
            "python": {
                "description": "a high-level, interpreted language known for readability and versatility",
                "best_practices": [
                    "Follow the PEP 8 style guide",
                    "Use virtual environments for dependency management",
                    "Leverage Python's rich standard library",
                    "Write docstrings for modules, classes, and functions",
                    "Use list comprehensions and generators for efficient data processing"
                ],
                "structure": [
                    "Organize code into modules and packages",
                    "Use classes when appropriate, but don't force OOP",
                    "Prefer explicit imports over implicit ones",
                    "Follow the principle of 'Explicit is better than implicit'"
                ]
            },
            "javascript": {
                "description": "a versatile language for web development, both frontend and backend",
                "best_practices": [
                    "Use modern ES6+ features where supported",
                    "Understand asynchronous programming (Promises, async/await)",
                    "Employ strict equality (===) for comparisons",
                    "Use linting tools like ESLint",
                    "Manage state carefully in applications"
                ],
                "structure": [
                    "Organize code into modules using import/export",
                    "Use appropriate design patterns (Module, Factory, Observer)",
                    "Consider functional programming approaches",
                    "Separate concerns between components"
                ]
            },
            "java": {
                "description": "a robust, object-oriented language with strong typing",
                "best_practices": [
                    "Follow standard Java naming conventions",
                    "Utilize Java's object-oriented features appropriately",
                    "Implement proper exception handling",
                    "Use interfaces to define contracts",
                    "Leverage Java's type system for compile-time safety"
                ],
                "structure": [
                    "Organize code into packages and classes",
                    "Follow the principle of encapsulation",
                    "Design with inheritance and polymorphism where appropriate",
                    "Use design patterns to solve common problems"
                ]
            },
            "c#": {
                "description": "a modern, object-oriented language with strong typing and extensive libraries",
                "best_practices": [
                    "Follow C# naming conventions and style guidelines",
                    "Use LINQ for data manipulation",
                    "Leverage C#'s strong typing and generics",
                    "Implement proper exception handling",
                    "Utilize async/await for asynchronous operations"
                ],
                "structure": [
                    "Organize code into namespaces, classes, and methods",
                    "Use interfaces to define contracts",
                    "Implement appropriate design patterns",
                    "Consider dependency injection for loosely coupled components"
                ]
            }
        }
    
    def _load_architecture_patterns(self) -> Dict[str, Any]:
        """Load software architecture patterns."""
        return {
            "MVC (Model-View-Controller)": {
                "description": "Separates application into three components for improved maintainability",
                "complexity": 3,
                "keywords": ["web", "ui", "interface", "application"],
                "components": [
                    "Model: Data and business logic",
                    "View: User interface elements",
                    "Controller: Handles user input and updates model/view"
                ]
            },
            "Microservices": {
                "description": "Distributes application as independent, deployable services",
                "complexity": 5,
                "keywords": ["scalable", "distributed", "service", "cloud"],
                "components": [
                    "Independent services with focused functionality",
                    "API Gateway for client communication",
                    "Service Discovery mechanism",
                    "Messaging system for service communication"
                ]
            },
            "Repository Pattern": {
                "description": "Abstracts data access logic from business logic",
                "complexity": 3,
                "keywords": ["database", "data", "storage", "crud"],
                "components": [
                    "Repository interfaces defining data operations",
                    "Repository implementations for specific data sources",
                    "Domain models representing business entities",
                    "Service layer utilizing repositories"
                ]
            },
            "CQRS (Command Query Responsibility Segregation)": {
                "description": "Separates read and write operations for complex domains",
                "complexity": 4,
                "keywords": ["performance", "scalability", "database", "complex"],
                "components": [
                    "Command model for write operations",
                    "Query model for read operations",
                    "Command handlers for business logic",
                    "Query handlers for data retrieval"
                ]
            },
            "Event-Driven Architecture": {
                "description": "Components communicate through events for loose coupling",
                "complexity": 4,
                "keywords": ["events", "realtime", "responsive", "messaging"],
                "components": [
                    "Event producers that generate events",
                    "Event consumers that react to events",
                    "Event bus/message broker for distribution",
                    "Event store for persistence (if needed)"
                ]
            },
            "Modular Design": {
                "description": "Organizes code into cohesive, loosely coupled modules",
                "complexity": 2,
                "keywords": ["maintainable", "organized", "reusable"],
                "components": [
                    "Core functionality module",
                    "Utility/helper modules",
                    "Feature-specific modules",
                    "Clear interfaces between modules"
                ]
            }
        }
    
    def _load_testing_strategies(self) -> Dict[str, Any]:
        """Load testing strategies for software development."""
        return {
            "Unit Testing": {
                "description": "Testing individual components in isolation",
                "min_complexity": 1,
                "applicable_languages": ["all"],
                "tools": {
                    "python": "pytest, unittest",
                    "javascript": "Jest, Mocha",
                    "java": "JUnit, TestNG",
                    "c#": "MSTest, NUnit, xUnit"
                }
            },
            "Integration Testing": {
                "description": "Testing interactions between components",
                "min_complexity": 2,
                "applicable_languages": ["all"],
                "tools": {
                    "python": "pytest",
                    "javascript": "Jest, Supertest",
                    "java": "Spring Test, Testcontainers",
                    "c#": "xUnit, Testcontainers"
                }
            },
            "End-to-End Testing": {
                "description": "Testing complete application flows",
                "min_complexity": 3,
                "applicable_languages": ["all"],
                "tools": {
                    "python": "Selenium, Playwright",
                    "javascript": "Cypress, Playwright",
                    "java": "Selenium, Playwright",
                    "c#": "Selenium, Playwright"
                }
            },
            "Property-Based Testing": {
                "description": "Testing with automatically generated inputs",
                "min_complexity": 4,
                "applicable_languages": ["python", "javascript", "java"],
                "tools": {
                    "python": "Hypothesis",
                    "javascript": "fast-check",
                    "java": "jqwik"
                }
            },
            "Performance Testing": {
                "description": "Testing application performance characteristics",
                "min_complexity": 4,
                "applicable_languages": ["all"],
                "tools": {
                    "python": "locust, pytest-benchmark",
                    "javascript": "k6, Artillery",
                    "java": "JMeter, Gatling",
                    "c#": "NBench, BenchmarkDotNet"
                }
            }
        }


# Default instance for convenience
default_strategy = SoftwareContentStrategy()


def populate_section(section: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Convenience function to populate a section using the default strategy.
    
    Args:
        section: Section definition
        context: Content generation context
        
    Returns:
        Generated content
    """
    return default_strategy.populate(section, context) 