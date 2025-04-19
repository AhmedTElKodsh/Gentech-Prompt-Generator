#!/usr/bin/env python3
"""
Test script for the prompt domain service.
"""

from promptgen.domains.domain_service import default_service

# Test input
test_input = "I'm a software developer and I want to create a daily joke NextJS web app with tailwind library"

# Extract domain and clean objective
domain, clean_objective = default_service.extract_role_from_objective(test_input)

print(f"Detected domain: {domain}")
print(f"Clean objective: {clean_objective}")

# Create a test section
test_section = {
    "name": "Task Description",
    "content_template": "You are tasked with building {objective}. This will involve creating a {project_type} using {technology_stack}."
}

# Create context
context = {
    "objective": clean_objective,
    "domain": domain,
    "complexity": 3,
    "technology_stack": "Next.js, React, Tailwind CSS",
    "project_type": "web application",
    "features": "daily joke display, joke categories, user favorites",
    "purpose": "entertainment"
}

# Populate the section using the domain service
populated_content = default_service.populate_section(test_section, context)

# Print the result
print("\n" + "="*80)
print("POPULATED SECTION:")
print(populated_content)
print("="*80)

# List available domains
print("\nAvailable domains:")
for d in default_service.get_available_domains():
    print(f"- {d}")

# List supported roles
print("\nSupported roles:")
for role in default_service.get_supported_roles():
    print(f"- {role} -> {default_service.role_to_domain.get(role)}") 