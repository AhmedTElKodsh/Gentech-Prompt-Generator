#!/usr/bin/env python3
"""
Simple test script for the prompt generator.
"""

import os
import pytest
from promptgen.core.generator import PromptGenerator, TemplateFactory
from promptgen.templates.loader import TemplateLibrary
from promptgen.domains.domain_service import default_service

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
def generator(template_factory):
    """Fixture to provide a prompt generator instance."""
    return PromptGenerator(template_factory=template_factory)

def test_simple_prompt_generation(generator):
    """Test simple prompt generation without additional context."""
    test_prompt = "I'm a software developer and I want to create a daily joke NextJS web app with tailwind library"
    
    # Extract domain and clean objective
    domain, clean_objective = default_service.extract_role_from_objective(test_prompt)
    
    # Verify domain extraction
    assert domain == "general"
    assert "create a daily joke NextJS web app" in clean_objective.lower()
    
    # Generate the prompt
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
    
    # Verify the objective is included
    assert clean_objective in generated_prompt

def test_simple_prompt_generation_with_different_complexity(generator):
    """Test prompt generation with different complexity levels."""
    test_prompt = "Create a simple calculator web app"
    domain, clean_objective = default_service.extract_role_from_objective(test_prompt)
    
    # Test with complexity level 1
    prompt_simple = generator.generate_prompt(
        objective=clean_objective,
        domain=domain,
        complexity=1
    )
    assert "Key Components:" in prompt_simple
    
    # Test with complexity level 2
    prompt_medium = generator.generate_prompt(
        objective=clean_objective,
        domain=domain,
        complexity=2
    )
    assert "Key Components:" in prompt_medium
    
    # Test with complexity level 3
    prompt_complex = generator.generate_prompt(
        objective=clean_objective,
        domain=domain,
        complexity=3
    )
    assert "Key Components:" in prompt_complex

def test_simple_prompt_generation_with_different_domains(generator):
    """Test prompt generation with different domains."""
    # Test with web development domain
    web_prompt = "Create a blog website"
    web_domain, web_objective = default_service.extract_role_from_objective(web_prompt)
    web_generated = generator.generate_prompt(
        objective=web_objective,
        domain=web_domain,
        complexity=3
    )
    assert "Key Components:" in web_generated
    
    # Test with data science domain
    data_prompt = "Build a machine learning model for image classification"
    data_domain, data_objective = default_service.extract_role_from_objective(data_prompt)
    data_generated = generator.generate_prompt(
        objective=data_objective,
        domain=data_domain,
        complexity=3
    )
    assert "Key Components:" in data_generated 