#!/usr/bin/env python3
"""
Test script for the prompt refiner functionality.
"""

import sys
from promptgen.core.refiner import PromptRefiner

print("Starting test...")

# Initialize the refiner
refiner = PromptRefiner()
print("Refiner initialized.")

# Sample prompt to refine
sample_prompt = """Write code for a calculator app"""
print(f"Sample prompt: '{sample_prompt}'")

# Analyze the prompt
print("Analyzing prompt...")
try:
    analysis = refiner.analyze(sample_prompt)
    print("Analysis completed successfully.")
    print("\n" + "="*80)
    print("ORIGINAL PROMPT ANALYSIS:")
    print(f"Quality Score: {analysis['quality_score']:.2f}")
    print(f"Complexity: {analysis['complexity']}")
    print(f"Word Count: {analysis['word_count']}")
    print(f"Issues Found: {[issue['type'] for issue in analysis['issues']]}")
    print(f"Sections: {[section['name'] for section in analysis['sections']]}")
except Exception as e:
    print(f"Error during analysis: {e}")
    print(f"Type: {type(e)}")
    import traceback
    traceback.print_exc(file=sys.stdout)

# Get suggestions for improvement
print("\nGetting improvement suggestions...")
try:
    suggestions = refiner.suggest_improvements(sample_prompt)
    print("Suggestions generated successfully.")
    print("\n" + "="*80)
    print("IMPROVEMENT SUGGESTIONS:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
except Exception as e:
    print(f"Error getting suggestions: {e}")
    print(f"Type: {type(e)}")
    import traceback
    traceback.print_exc(file=sys.stdout)

# Refine the prompt
print("\nRefining prompt...")
try:
    refinement = refiner.refine(
        prompt=sample_prompt,
        objective="Create a fully functional calculator app with basic arithmetic operations",
        desired_improvements=["add_examples", "add_constraints"]
    )
    print("Refinement completed successfully.")
    
    print("\n" + "="*80)
    print("REFINED PROMPT:")
    print(refinement["refined_prompt"])
    
    print("\n" + "="*80)
    print("IMPROVEMENTS MADE:")
    for improvement in refinement["improvements"]:
        print(f"- {improvement['description']}")
    
    print("\n" + "="*80)
    print(f"IMPROVEMENT SCORE: {refinement['improvement_score']:.2f}")
    print("="*80)
except Exception as e:
    print(f"Error during refinement: {e}")
    print(f"Type: {type(e)}")
    import traceback
    traceback.print_exc(file=sys.stdout)

print("\nTest completed.") 