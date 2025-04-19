"""
Integration tests for domain-specific prompt evaluation.
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from promptgen.utils.domain_evaluator import DomainSpecificEvaluator, evaluate_prompt_with_domain

# Test prompts
TEST_SOFTWARE_PROMPT = """
Create a Python microservice that handles user authentication with JWT.
The service should provide endpoints for registration, login, password reset,
and token validation. Use Flask and SQLAlchemy for the implementation.

Requirements:
1. Implement secure password hashing with bcrypt
2. Create RESTful API endpoints with proper error handling
3. Use JWT for token-based authentication
4. Implement proper input validation and sanitization
5. Write unit tests for the authentication logic
6. Include documentation for the API endpoints

Make sure to follow clean code principles and ensure the code is maintainable.
Also consider security best practices to prevent common vulnerabilities like SQL injection and XSS.
"""

TEST_CONTENT_PROMPT = """
Write a blog post about machine learning for beginners.

Target audience: College students with basic programming knowledge who are interested in AI.
Tone: Friendly, educational, and conversational but still professional.
Length: 1500-2000 words
SEO keywords: machine learning basics, AI for beginners, ML tutorial

Structure:
- Introduction with a hook to engage readers
- Define machine learning in simple terms
- Section explaining different types of machine learning algorithms
- Practical code example for a simple classification problem
- Real-world applications of machine learning
- Resources for further learning
- Conclusion with call-to-action

Include engaging headings, bullet points, and visual descriptions to keep the audience engaged.
Focus on making complex concepts accessible to beginners while maintaining accuracy.
"""

TEST_BUSINESS_PROMPT = """
Develop a market entry strategy for a premium electric bicycle company 
looking to expand into the European market.

Business Objectives:
- Achieve 5% market share within 24 months
- Establish brand recognition in key urban centers
- Develop partnerships with local retailers and service providers
- Ensure ROI of at least 15% by year 3

Include analysis of:
1. Target market segments and customer profiles
2. Competitive landscape and positioning strategy
3. Pricing strategy considering local economic factors
4. Distribution channels and logistics considerations
5. Marketing and promotional strategy with KPIs
6. Risk assessment and mitigation plans

The strategy should account for regulatory requirements across different 
EU countries and address potential challenges in the supply chain.
Consider stakeholder concerns at all levels, from investors to local communities.
Include metrics for measuring success and a timeline for implementation phases.
Evaluate feasibility of different entry approaches: direct-to-consumer vs. retail partnerships.
"""

def test_software_evaluation():
    """Test evaluation of a software development prompt."""
    evaluator = DomainSpecificEvaluator(domain="software")
    results = evaluator.evaluate(TEST_SOFTWARE_PROMPT)
    
    # Check that domain-specific evaluation was performed
    assert "domain_scores" in results
    assert "domain_quality_score" in results
    assert "combined_quality_score" in results
    assert results["domain"] == "software"
    
    # Check that software-specific factors were evaluated
    domain_scores = results["domain_scores"]
    assert "technical_accuracy" in domain_scores
    assert "implementation_detail" in domain_scores
    assert "security_consideration" in domain_scores
    assert "maintainability" in domain_scores
    assert "testability" in domain_scores
    
    # Technical terms should be recognized
    assert domain_scores["technical_accuracy"] > 0.5
    
    # Security considerations should be recognized
    assert domain_scores["security_consideration"] > 0.3
    
    # Domain suggestions should be present if scores are low enough
    assert "domain_suggestions" in results

def test_content_evaluation():
    """Test evaluation of a content creation prompt."""
    evaluator = DomainSpecificEvaluator(domain="content")
    results = evaluator.evaluate(TEST_CONTENT_PROMPT)
    
    # Check that domain-specific evaluation was performed
    assert "domain_scores" in results
    assert results["domain"] == "content"
    
    # Check that content-specific factors were evaluated
    domain_scores = results["domain_scores"]
    assert "audience_focus" in domain_scores
    assert "tone_consistency" in domain_scores
    assert "engagement_potential" in domain_scores
    assert "content_structure" in domain_scores
    assert "seo_consideration" in domain_scores
    
    # Audience focus should be recognized (the pattern matches "Target audience:")
    assert domain_scores["audience_focus"] > 0.3
    
    # SEO considerations should be recognized (the pattern matches "SEO keywords:")
    assert domain_scores["seo_consideration"] > 0.3
    
    # Content structure should be recognized (matches structure section)
    assert domain_scores["content_structure"] > 0.3

def test_business_evaluation():
    """Test evaluation of a business strategy prompt."""
    evaluator = DomainSpecificEvaluator(domain="business")
    results = evaluator.evaluate(TEST_BUSINESS_PROMPT)
    
    # Check that domain-specific evaluation was performed
    assert "domain_scores" in results
    assert results["domain"] == "business"
    
    # Check that business-specific factors were evaluated
    domain_scores = results["domain_scores"]
    assert "metric_orientation" in domain_scores
    assert "stakeholder_consideration" in domain_scores
    assert "strategic_alignment" in domain_scores
    assert "feasibility" in domain_scores
    assert "risk_assessment" in domain_scores
    
    # Market metrics should be recognized (matches 5%, ROI, etc.)
    assert domain_scores["metric_orientation"] > 0.2
    
    # Risk assessment should be recognized (matches "risk assessment")
    assert domain_scores["risk_assessment"] > 0.2
    
    # Strategic alignment should be recognized (matches "strategy")
    assert domain_scores["strategic_alignment"] > 0.2

def test_combined_quality_score():
    """Test that combined quality score blends base and domain scores."""
    evaluator = DomainSpecificEvaluator(domain="software")
    results = evaluator.evaluate(TEST_SOFTWARE_PROMPT)
    
    # Combined score should be between base and domain scores
    base_score = results["quality_score"]
    domain_score = results["domain_quality_score"]
    combined_score = results["combined_quality_score"]
    
    # Verify the weighted combination (60% base, 40% domain)
    expected_combined = (base_score * 0.6) + (domain_score * 0.4)
    assert abs(combined_score - expected_combined) < 0.01

def test_domain_suggestions():
    """Test that appropriate domain-specific suggestions are generated."""
    # Use a prompt with deliberate omissions in security and testing
    prompt = """
    Create a Python web application using Flask that allows users to upload images.
    
    Requirements:
    1. Implement a responsive UI with Bootstrap
    2. Optimize the application for performance
    """
    
    evaluator = DomainSpecificEvaluator(domain="software")
    results = evaluator.evaluate(prompt)
    
    # Check suggestions
    assert "domain_suggestions" in results
    suggestions = results["domain_suggestions"]
    
    # There should be suggestions about security and testing
    security_suggestion = any("security" in suggestion.lower() for suggestion in suggestions)
    testing_suggestion = any("test" in suggestion.lower() for suggestion in suggestions)
    
    assert security_suggestion
    assert testing_suggestion

def test_convenience_function():
    """Test that the convenience function returns expected structure."""
    # Use the convenience function
    result = evaluate_prompt_with_domain(TEST_CONTENT_PROMPT, domain="content")
    
    # Check structure
    assert "quality_score" in result
    assert "domain_scores" in result
    assert "domain" in result
    assert result["domain"] == "content"
    
    # Check content-specific scores
    domain_scores = result["domain_scores"]
    expected_keys = ["audience_focus", "tone_consistency", "engagement_potential", 
                    "content_structure", "seo_consideration"]
    
    for key in expected_keys:
        assert key in domain_scores

def test_no_domain_specified():
    """Test that standard evaluation is returned when no domain is specified."""
    evaluator = DomainSpecificEvaluator()  # No domain specified
    results = evaluator.evaluate(TEST_SOFTWARE_PROMPT)
    
    # Should not have domain-specific results
    assert "domain_scores" not in results
    assert "domain_quality_score" not in results
    assert "domain_suggestions" not in results
    
    # Should have standard quality score
    assert "quality_score" in results
    assert "factor_scores" in results

def test_pandas_integration():
    """Test integration with pandas for UI visualization."""
    # Get evaluation results
    evaluator = DomainSpecificEvaluator(domain="software")
    results = evaluator.evaluate(TEST_SOFTWARE_PROMPT)
    
    # Try to create a DataFrame from the results
    try:
        factor_df = pd.DataFrame({
            'Factor': list(results["factor_scores"].keys()),
            'Score': list(results["factor_scores"].values())
        })
        
        domain_df = pd.DataFrame({
            'Factor': list(results["domain_scores"].keys()),
            'Score': list(results["domain_scores"].values())
        })
        
        # Check that DataFrames were created correctly
        assert len(factor_df) == len(results["factor_scores"])
        assert len(domain_df) == len(results["domain_scores"])
        
        # Check that column types are as expected
        assert factor_df['Factor'].dtype == 'object'
        assert factor_df['Score'].dtype == 'float64'
        
    except Exception as e:
        pytest.fail(f"Failed to create pandas DataFrame: {e}")

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 