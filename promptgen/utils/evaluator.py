"""
Prompt evaluation utilities for the AI Prompt Generator.

This module provides functionality to evaluate the quality of prompts
and calculate various metrics to assess their effectiveness.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import logging
from tqdm import tqdm
import time

# Setup logger
logger = logging.getLogger(__name__)

class PromptEvaluator:
    """
    Evaluates the quality and effectiveness of prompts.
    
    Inspired by the betterprompt repository's evaluation approach.
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize a prompt evaluator.
        
        Args:
            llm_client: Client for making test requests to LLMs (if None, evaluation
                        is limited to structural metrics only)
        """
        self.llm_client = llm_client
        
        # Weighted quality factors
        self.quality_factors = {
            "clarity": 0.25,         # Clear and unambiguous wording
            "specificity": 0.20,     # Sufficient details and constraints
            "structure": 0.15,       # Logical organization and formatting
            "context": 0.15,         # Appropriate background information
            "actionability": 0.25    # Clear task definition
        }
        
        # Regex patterns for structural evaluation
        self.patterns = {
            "clarity": [
                r"(you|your|yours)\b",                    # Second person pronouns (reduces clarity)
                r"\b(maybe|perhaps|might|could|possibly)", # Uncertainty markers (reduces clarity)
                r"\b(this|that|these|those|it|they)\b(?!\s+\w+)", # Ambiguous referents (reduces clarity)
            ],
            "specificity": [
                r"\b(\w+ly)\b",            # Adverbs (often vague)
                r"\b(good|great|nice|bad|terrible|awesome)\b", # Generic evaluative terms
                r"\b(thing|stuff|something|anything)\b", # Non-specific nouns
            ],
            "structure": [
                r"^\s*#.*$",             # Headers
                r"^\s*\d+\.\s+.*$",      # Numbered lists
                r"^\s*\*\s+.*$",         # Bullet points
                r"^\s*-\s+.*$",          # Dash lists
                r"```[\s\S]*?```",       # Code blocks
            ],
            "context": [
                r"(?i)\b(context|background|introduction|given|assume)\b", # Context markers
                r"(?i)\b(previous|before|after|following)\b",              # Sequential markers
                r"(?i)\b(example|instance|case|scenario)\b",               # Example markers
            ],
            "actionability": [
                r"(?i)\b(create|make|develop|implement|design|build|write|code|analyze|evaluate|explain|describe|list|identify|outline|summarize)\b", # Action verbs
                r"\b(need|require|must|should|shall|will)\b",                # Requirement terms
                r"(?i)\b(output|result|deliverable|product|artifact)\b",     # Output markers
            ]
        }
    
    def evaluate(self, prompt: str) -> Dict[str, Any]:
        """
        Evaluate the quality of a prompt.
        
        Args:
            prompt: The prompt text to evaluate
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Normalize the prompt text
        prompt_text = prompt.strip()
        word_count = len(prompt_text.split())
        
        # Run the basic structural evaluation
        structure_scores = self._evaluate_structure(prompt_text)
        
        # Calculate overall weighted quality score
        quality_score = sum(
            structure_scores[factor] * weight 
            for factor, weight in self.quality_factors.items()
        )
        
        results = {
            "quality_score": round(quality_score * 100) / 100,  # Scale 0-1, rounded to 2 decimals
            "word_count": word_count,
            "factor_scores": structure_scores,
            "suggestions": self._generate_suggestions(structure_scores, prompt_text)
        }
        
        # If LLM client is available, perform response-based evaluation
        if self.llm_client and word_count > 10:
            try:
                response_metrics = self._evaluate_with_llm(prompt_text)
                results.update(response_metrics)
            except Exception as e:
                logger.error(f"LLM evaluation failed: {str(e)}")
                results["llm_evaluation_error"] = str(e)
        
        return results
    
    def _evaluate_structure(self, prompt_text: str) -> Dict[str, float]:
        """
        Evaluate the structural qualities of a prompt.
        
        Args:
            prompt_text: Normalized prompt text
            
        Returns:
            Dictionary with scores for each quality factor
        """
        # Split the prompt into lines and words for analysis
        lines = prompt_text.split("\n")
        words = prompt_text.split()
        total_words = len(words)
        
        if total_words == 0:
            return {factor: 0 for factor in self.quality_factors}
        
        # Initialize scores
        scores = {}
        
        # Clarity score (1 is most clear)
        clarity_matches = sum(
            1 for pattern in self.patterns["clarity"]
            for match in re.finditer(pattern, prompt_text, re.MULTILINE)
        )
        clarity_penalty = min(1.0, clarity_matches / (total_words * 0.1))
        scores["clarity"] = 1 - clarity_penalty
        
        # Specificity score
        specificity_matches = sum(
            1 for pattern in self.patterns["specificity"]
            for match in re.finditer(pattern, prompt_text, re.MULTILINE)
        )
        specificity_penalty = min(1.0, specificity_matches / (total_words * 0.1))
        
        # Adjust specificity based on length
        length_bonus = min(1.0, total_words / 100) * 0.3
        scores["specificity"] = (1 - specificity_penalty) * 0.7 + length_bonus
        
        # Structure score
        structure_matches = sum(
            1 for pattern in self.patterns["structure"]
            for line in lines
            if re.match(pattern, line)
        )
        structure_ratio = min(1.0, structure_matches / max(1, len(lines) * 0.25))
        scores["structure"] = structure_ratio
        
        # Context score
        context_matches = sum(
            1 for pattern in self.patterns["context"]
            for match in re.finditer(pattern, prompt_text, re.MULTILINE)
        )
        context_score = min(1.0, context_matches / max(5, total_words * 0.02))
        scores["context"] = context_score
        
        # Actionability score
        action_matches = sum(
            1 for pattern in self.patterns["actionability"]
            for match in re.finditer(pattern, prompt_text, re.MULTILINE)
        )
        action_score = min(1.0, action_matches / max(3, total_words * 0.05))
        scores["actionability"] = action_score
        
        return scores
    
    def _evaluate_with_llm(self, prompt_text: str) -> Dict[str, Any]:
        """
        Evaluate prompt by testing responses from an LLM.
        
        Args:
            prompt_text: The prompt to test
            
        Returns:
            Dictionary with response-based metrics
        """
        if not self.llm_client:
            return {}
        
        # Sample different response variations
        response_metrics = {
            "response_consistency": 0,
            "response_length": 0,
            "response_time": 0,
            "sample_responses": []
        }
        
        try:
            # Get multiple responses to assess consistency
            responses = []
            total_time = 0
            total_length = 0
            
            # Make 3 test requests with the prompt
            for _ in range(3):
                start_time = time.time()
                response = self.llm_client.generate(prompt_text)
                end_time = time.time()
                
                response_time = end_time - start_time
                total_time += response_time
                
                # Clean up response and store key metrics
                cleaned_response = response.strip()
                responses.append(cleaned_response)
                
                # Track response length
                response_length = len(cleaned_response.split())
                total_length += response_length
                
                # Add to samples (truncated if very long)
                if len(cleaned_response) > 500:
                    sample = cleaned_response[:497] + "..."
                else:
                    sample = cleaned_response
                    
                response_metrics["sample_responses"].append({
                    "text": sample,
                    "length": response_length,
                    "time": round(response_time, 2)
                })
            
            # Calculate average metrics
            response_metrics["response_time"] = round(total_time / 3, 2)
            response_metrics["response_length"] = round(total_length / 3)
            
            # Calculate consistency (using simple similarity metric)
            if len(responses) > 1:
                similarity_sum = 0
                comparisons = 0
                
                for i in range(len(responses)):
                    for j in range(i+1, len(responses)):
                        similarity = self._calculate_similarity(responses[i], responses[j])
                        similarity_sum += similarity
                        comparisons += 1
                
                if comparisons > 0:
                    response_metrics["response_consistency"] = round(similarity_sum / comparisons, 2)
            
            return response_metrics
            
        except Exception as e:
            logger.error(f"LLM testing failed: {str(e)}")
            return {"llm_test_error": str(e)}
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate a simple similarity score between two text responses.
        
        Args:
            text1, text2: Texts to compare
            
        Returns:
            Similarity score between 0 and 1
        """
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _generate_suggestions(self, scores: Dict[str, float], prompt_text: str) -> List[str]:
        """
        Generate improvement suggestions based on evaluation scores.
        
        Args:
            scores: Factor scores from evaluation
            prompt_text: The original prompt text
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Make recommendations based on low scores
        if scores["clarity"] < 0.7:
            suggestions.append("Reduce ambiguous pronouns (this, that, it) and clarify what they refer to")
            suggestions.append("Replace uncertain language (maybe, perhaps, might) with definitive statements")
        
        if scores["specificity"] < 0.6:
            suggestions.append("Add more specific details about expected output or deliverables")
            suggestions.append("Replace generic terms with precise requirements or constraints")
        
        if scores["structure"] < 0.5:
            suggestions.append("Improve organization with headers, lists, or sections")
            suggestions.append("Break down complex instructions into clear steps or bullet points")
        
        if scores["context"] < 0.6:
            suggestions.append("Add more background information or context")
            suggestions.append("Clarify assumptions or pre-conditions for the task")
        
        if scores["actionability"] < 0.7:
            suggestions.append("Specify clear action items or deliverables")
            suggestions.append("Include explicit instructions about what needs to be done")
        
        # Length-based suggestions
        word_count = len(prompt_text.split())
        if word_count < 30:
            suggestions.append("Consider expanding the prompt with more details and context")
        elif word_count > 500:
            suggestions.append("The prompt is quite long - consider focusing on the most essential elements")
        
        return suggestions
    
    def compare_prompts(self, prompts: List[str]) -> Dict[str, Any]:
        """
        Compare multiple prompts and identify the best option.
        
        Args:
            prompts: List of prompt texts to compare
            
        Returns:
            Comparison results with rankings and evaluations
        """
        if not prompts:
            return {"error": "No prompts provided for comparison"}
        
        # Evaluate each prompt
        evaluations = []
        for i, prompt in enumerate(prompts):
            eval_result = self.evaluate(prompt)
            eval_result["prompt_index"] = i
            eval_result["prompt_text"] = prompt
            evaluations.append(eval_result)
        
        # Sort by quality score
        sorted_evals = sorted(evaluations, key=lambda x: x["quality_score"], reverse=True)
        
        return {
            "best_prompt_index": sorted_evals[0]["prompt_index"],
            "evaluations": sorted_evals,
            "comparison_notes": self._generate_comparison_notes(sorted_evals)
        }
    
    def _generate_comparison_notes(self, evaluations: List[Dict[str, Any]]) -> List[str]:
        """
        Generate notes comparing the evaluated prompts.
        
        Args:
            evaluations: List of evaluation results
            
        Returns:
            List of comparison notes
        """
        notes = []
        
        if len(evaluations) <= 1:
            return notes
        
        best = evaluations[0]
        worst = evaluations[-1]
        
        # Compare best vs worst
        score_diff = best["quality_score"] - worst["quality_score"]
        notes.append(f"The best prompt scores {score_diff:.2f} points higher than the worst prompt")
        
        # Identify key differentiators
        for factor in self.quality_factors:
            if best["factor_scores"][factor] - worst["factor_scores"][factor] > 0.3:
                notes.append(f"Major difference in {factor}: {best['factor_scores'][factor]:.2f} vs {worst['factor_scores'][factor]:.2f}")
        
        # Length comparison
        if abs(best["word_count"] - worst["word_count"]) > best["word_count"] * 0.5:
            notes.append(f"Significant length difference: {best['word_count']} words vs {worst['word_count']} words")
        
        return notes


def evaluate_prompt(prompt_text: str, llm_client=None) -> Dict[str, Any]:
    """
    Evaluate a prompt using the PromptEvaluator.
    
    Convenience function for quick evaluations.
    
    Args:
        prompt_text: The prompt to evaluate
        llm_client: Optional LLM client for response testing
        
    Returns:
        Evaluation metrics
    """
    evaluator = PromptEvaluator(llm_client)
    return evaluator.evaluate(prompt_text) 