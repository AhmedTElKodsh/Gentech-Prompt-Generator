#!/usr/bin/env python3
"""
Test script for the prompt generator.
"""

import os
import pytest
from promptgen.core.generator import PromptGenerator, TemplateFactory
from promptgen.templates.loader import TemplateLibrary
from promptgen.domains.domain_service import DomainService

@pytest.fixture
def template_library():
    """Fixture to provide a template library instance."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, "promptgen", "templates", "examples")
    return TemplateLibrary(templates_dir)

@pytest.fixture
def template_factory(template_library):
    """Fixture to provide a template factory instance."""
    return TemplateFactory(template_library)

@pytest.fixture
def domain_service():
    """Fixture to provide a domain service instance."""
    return DomainService()

@pytest.fixture
def generator(template_factory):
    """Fixture to provide a prompt generator instance."""
    return PromptGenerator(template_factory=template_factory)

@pytest.fixture
def test_context():
    """Fixture to provide test context data."""
    return {
        "key_components": "a Next.js frontend with Tailwind CSS, a jokes API integration, and a daily joke scheduling system",
        "requirements": "- Next.js for the frontend\n- Tailwind CSS for styling\n- Integration with a jokes API\n- Daily joke refresh functionality\n- Responsive design for all device sizes",
        "architecture_patterns": "MVC, JAMstack for frontend development",
        "language_stack": "JavaScript/TypeScript, React, Next.js, Tailwind CSS",
        "data_entities": "- Joke: {id, content, category, date_shown}\n- User Preference: {user_id, preferred_categories, favorite_jokes}",
        "quality_attributes": "responsive, intuitive to use, and visually appealing",
        "usage_example": "A user visits the site and is presented with the joke of the day. They can bookmark favorite jokes or set preferences for joke categories."
    }

def test_domain_extraction(domain_service):
    """Test domain extraction from objective."""
    test_prompt = "I'm a software developer and I want to create a daily joke NextJS web app with tailwind library"
    domain, clean_objective = domain_service.extract_role_from_objective(test_prompt)
    
    assert domain == "general"
    assert "create a daily joke NextJS web app" in clean_objective.lower()

def test_prompt_generation(generator, domain_service, test_context):
    """Test prompt generation with context."""
    test_prompt = "I'm a software developer and I want to create a daily joke NextJS web app with tailwind library"
    domain, clean_objective = domain_service.extract_role_from_objective(test_prompt)
    
    generated_prompt = generator.generate_prompt(
        objective=clean_objective,
        domain=domain,
        complexity=3,
        context=test_context
    )
    
    # Verify the generated prompt contains expected sections
    assert "Key Components:" in generated_prompt
    assert "Requirements:" in generated_prompt
    assert "Architecture and Patterns:" in generated_prompt
    assert "Technology Stack:" in generated_prompt
    assert "Data Model:" in generated_prompt
    assert "Quality Attributes:" in generated_prompt
    assert "Example Usage:" in generated_prompt
    
    # Verify context values are included
    assert test_context["key_components"] in generated_prompt
    assert test_context["requirements"] in generated_prompt
    assert test_context["architecture_patterns"] in generated_prompt
    assert test_context["language_stack"] in generated_prompt
    assert test_context["data_entities"] in generated_prompt
    assert test_context["quality_attributes"] in generated_prompt
    assert test_context["usage_example"] in generated_prompt

def test_prompt_generation_without_context(generator, domain_service):
    """Test prompt generation without context."""
    test_prompt = "I'm a software developer and I want to create a daily joke NextJS web app with tailwind library"
    domain, clean_objective = domain_service.extract_role_from_objective(test_prompt)
    
    generated_prompt = generator.generate_prompt(
        objective=clean_objective,
        domain=domain,
        complexity=3
    )
    
    # Verify the generated prompt contains expected sections
    assert "Key Components:" in generated_prompt
    assert "Requirements:" in generated_prompt
    assert "Architecture and Patterns:" in generated_prompt
    assert "Technology Stack:" in generated_prompt
    assert "Data Model:" in generated_prompt
    assert "Quality Attributes:" in generated_prompt
    assert "Example Usage:" in generated_prompt

def test_invalid_domain(generator):
    """Test prompt generation with invalid domain."""
    with pytest.raises(ValueError):
        generator.generate_prompt(
            objective="Create a web app",
            domain="invalid_domain",
            complexity=3
        )

def test_invalid_complexity(generator):
    """Test prompt generation with invalid complexity."""
    with pytest.raises(ValueError):
        generator.generate_prompt(
            objective="Create a web app",
            domain="general",
            complexity=10  # Invalid complexity level
        ) 