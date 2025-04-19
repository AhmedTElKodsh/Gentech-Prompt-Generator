"""
Tests for the complexity analysis functionality.
"""

import pytest
from ..core.complexity import ComplexityAnalyzer, analyze_complexity

def test_basic_initialization():
    """Test basic initialization of ComplexityAnalyzer."""
    analyzer = ComplexityAnalyzer()
    assert isinstance(analyzer.domain_technical_terms, dict)
    assert isinstance(analyzer.subtask_verbs, set)
    assert isinstance(analyzer.dependency_indicators, set)
    assert isinstance(analyzer.complexity_multipliers, dict)

def test_empty_input():
    """Test handling of empty input."""
    analyzer = ComplexityAnalyzer()
    with pytest.raises(ValueError):
        analyzer.analyze_complexity("", "software")
    with pytest.raises(ValueError):
        analyzer.analyze_complexity(None, "software")

def test_invalid_domain():
    """Test handling of invalid domain."""
    analyzer = ComplexityAnalyzer()
    # Should not raise error, but return base complexity
    level, analysis = analyzer.analyze_complexity("Simple task", "invalid_domain")
    assert level >= 1
    assert 'score' in analysis
    assert 'factors' in analysis

def test_technical_terms_identification():
    """Test identification of technical terms."""
    analyzer = ComplexityAnalyzer()
    
    # Test software domain terms
    text = "Create an API endpoint using REST and implement JWT authentication"
    terms = analyzer._identify_technical_terms(text, "software")
    assert "API" in terms
    assert "REST" in terms
    assert "JWT" in terms
    assert "authentication" in terms
    
    # Test programming languages
    text = "Write code in Python and JavaScript"
    terms = analyzer._identify_technical_terms(text)
    assert "python" in terms
    assert "javascript" in terms
    
    # Test version numbers
    text = "Upgrade to version v2.0.1 and ensure compatibility with 3.8.0"
    terms = analyzer._identify_technical_terms(text)
    assert "v2.0.1" in terms
    assert "3.8.0" in terms

def test_component_identification():
    """Test identification of components/subtasks."""
    analyzer = ComplexityAnalyzer()
    
    # Test with subtask verbs
    text = "implement authentication and create database schema"
    components = analyzer._identify_components(text)
    assert any("implement authentication" in comp for comp in components)
    assert any("create database schema" in comp for comp in components)
    
    # Test with list items
    text = "Tasks:\n- Set up database\n- Configure API\n- Test integration"
    components = analyzer._identify_components(text)
    assert "Set up database" in components
    assert "Configure API" in components
    assert "Test integration" in components

def test_dependency_identification():
    """Test identification of dependencies."""
    analyzer = ComplexityAnalyzer()
    
    text = "Set up the database before implementing the API. The frontend depends on the API implementation."
    deps = analyzer._identify_dependencies(text)
    assert len(deps) >= 2
    assert any(dep[1].strip().lower().endswith("api implementation") for dep in deps)

def test_complexity_levels():
    """Test different complexity levels."""
    analyzer = ComplexityAnalyzer()
    
    # Simple task
    level, _ = analyzer.analyze_complexity("Add a simple button to the webpage", "software")
    assert level == 1
    
    # Medium complexity
    level, _ = analyzer.analyze_complexity(
        "Implement user authentication with JWT and integrate with the existing API",
        "software"
    )
    assert level >= 3
    
    # High complexity
    level, _ = analyzer.analyze_complexity(
        """Design and implement a distributed microservices architecture with:
        - Authentication service using JWT
        - Real-time data processing with Redis
        - Load balancing and auto-scaling
        - Monitoring and logging infrastructure
        Must ensure high availability and disaster recovery.""",
        "software"
    )
    assert level >= 4

def test_edge_cases():
    """Test various edge cases."""
    analyzer = ComplexityAnalyzer()
    
    # Very long single word
    level, _ = analyzer.analyze_complexity("a" * 1000, "software")
    assert level >= 1  # Should not crash
    
    # Very long text
    long_text = "word " * 1000
    level, _ = analyzer.analyze_complexity(long_text, "software")
    assert level >= 1  # Should not crash
    
    # Special characters
    special_text = "!@#$%^&*()_+ implement this feature !@#$%^&*()"
    level, _ = analyzer.analyze_complexity(special_text, "software")
    assert level >= 1  # Should handle special characters
    
    # Unicode characters
    unicode_text = "implement this feature 你好 привет مرحبا"
    level, _ = analyzer.analyze_complexity(unicode_text, "software")
    assert level >= 1  # Should handle unicode

def test_convenience_function():
    """Test the convenience function."""
    level, analysis = analyze_complexity(
        "Create a simple REST API endpoint",
        "software"
    )
    assert isinstance(level, int)
    assert isinstance(analysis, dict)
    assert 'score' in analysis
    assert 'factors' in analysis
    assert 'components' in analysis
    assert 'technical_terms' in analysis
    assert 'dependencies' in analysis

def test_domain_specific_terms():
    """Test domain-specific technical terms."""
    analyzer = ComplexityAnalyzer()
    
    # Software domain
    level, analysis = analyzer.analyze_complexity(
        "Implement caching and optimize database queries",
        "software"
    )
    assert "cache" in [term.lower() for term in analysis['technical_terms']]
    assert "database" in [term.lower() for term in analysis['technical_terms']]
    
    # Content domain
    level, analysis = analyzer.analyze_complexity(
        "Improve SEO and analyze user engagement metrics",
        "content"
    )
    assert "seo" in [term.lower() for term in analysis['technical_terms']]
    assert "engagement" in [term.lower() for term in analysis['technical_terms']]
    
    # Business domain
    level, analysis = analyzer.analyze_complexity(
        "Calculate ROI and perform market analysis",
        "business"
    )
    assert any("analysis" in term.lower() for term in analysis['technical_terms'])

def test_complexity_factors():
    """Test various complexity factors."""
    analyzer = ComplexityAnalyzer()
    
    # Test system integration complexity
    _, analysis = analyzer.analyze_complexity(
        "Integrate with third-party system",
        "software"
    )
    assert any("integration" in factor.lower() for factor in analysis['factors'])
    
    # Test security complexity
    _, analysis = analyzer.analyze_complexity(
        "Implement security measures and compliance checks",
        "software"
    )
    assert any("security" in factor.lower() for factor in analysis['factors'])
    
    # Test performance complexity
    _, analysis = analyzer.analyze_complexity(
        "Optimize performance and scale the system",
        "software"
    )
    assert any("performance" in factor.lower() for factor in analysis['factors'])

if __name__ == '__main__':
    pytest.main([__file__]) 