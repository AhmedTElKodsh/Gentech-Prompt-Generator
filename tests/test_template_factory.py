"""
Tests for the template selection and factory functionality.
"""

import pytest
from unittest.mock import Mock, patch
from promptgen.core.generator import TemplateFactory
from promptgen.templates.loader import PromptTemplate, TemplateLibrary

# Mock templates for testing
def create_mock_template(name, domain, complexity_range=(1, 5), sections=None, tags=None):
    template = Mock(spec=PromptTemplate)
    template.name = name
    template.domain = domain
    template.complexity_range = complexity_range
    template.tags = tags or []
    
    required_sections = []
    optional_sections = []
    if sections:
        required_sections = [s for s, req in sections.items() if req]
        optional_sections = [s for s, req in sections.items() if not req]
    
    template.get_required_sections.return_value = required_sections
    template.get_optional_sections.return_value = optional_sections
    return template

class TestTemplateFactory:
    @pytest.fixture
    def template_library(self):
        """Create a mock template library with various templates"""
        library = Mock(spec=TemplateLibrary)
        
        # Software domain templates
        sw_template1 = create_mock_template(
            "software_basic",
            "software",
            complexity_range=(1, 3),
            sections={"requirements": True, "implementation": True, "testing": False},
            tags=["basic", "coding"]
        )
        sw_template2 = create_mock_template(
            "software_advanced",
            "software",
            complexity_range=(3, 5),
            sections={"architecture": True, "implementation": True, "testing": True, "deployment": True},
            tags=["advanced", "architecture"]
        )
        
        # Content domain templates
        content_template = create_mock_template(
            "content_basic",
            "content",
            complexity_range=(1, 4),
            sections={"outline": True, "content": True, "seo": False},
            tags=["writing", "seo"]
        )
        
        # General templates
        general_template = create_mock_template(
            "general_template",
            "general",
            complexity_range=(1, 5),
            sections={"description": True, "steps": True},
            tags=["general"]
        )
        
        # Configure library mock
        def find_templates(domain, complexity):
            if domain == "software":
                return [t for t in [sw_template1, sw_template2] 
                       if t.complexity_range[0] <= complexity <= t.complexity_range[1]]
            elif domain == "content":
                return [content_template] if content_template.complexity_range[0] <= complexity <= content_template.complexity_range[1] else []
            elif domain == "general":
                return [general_template]
            return []
            
        library.find_templates.side_effect = find_templates
        return library
    
    @pytest.fixture
    def factory(self, template_library):
        """Create a TemplateFactory instance with the mock library"""
        return TemplateFactory(template_library)
    
    def test_basic_template_selection(self, factory):
        """Test basic template selection for different domains"""
        # Test software domain
        template = factory.create_template("software", 2)
        assert template.name == "software_basic"
        
        template = factory.create_template("software", 4)
        assert template.name == "software_advanced"
        
        # Test content domain
        template = factory.create_template("content", 3)
        assert template.name == "content_basic"
        
        # Test general domain
        template = factory.create_template("general", 3)
        assert template.name == "general_template"
    
    def test_component_based_selection(self, factory):
        """Test template selection based on required components"""
        # Test with required components
        template = factory.create_template(
            "software", 4, 
            components=["architecture", "implementation", "testing"]
        )
        assert template.name == "software_advanced"
        
        # Test with mix of required and optional components
        template = factory.create_template(
            "software", 2,
            components=["requirements", "testing"]
        )
        assert template.name == "software_basic"
    
    def test_tag_based_selection(self, factory):
        """Test template selection with tag preferences"""
        template = factory.create_template(
            "software", 4,
            tags=["architecture"]
        )
        assert template.name == "software_advanced"
        
        template = factory.create_template(
            "content", 2,
            tags=["seo"]
        )
        assert template.name == "content_basic"
    
    def test_fallback_behavior(self, factory):
        """Test fallback to general templates when no domain-specific match"""
        # Test fallback for unknown domain
        template = factory.create_template("unknown_domain", 3)
        assert template.name == "general_template"
        
        # Test fallback when complexity out of range
        template = factory.create_template("content", 5)
        assert template.name == "general_template"
    
    def test_edge_cases(self, factory):
        """Test various edge cases"""
        # Test with empty components list
        template = factory.create_template("software", 3, components=[])
        assert template.name in ["software_basic", "software_advanced"]
        
        # Test with empty tags list
        template = factory.create_template("software", 3, tags=[])
        assert template.name in ["software_basic", "software_advanced"]
        
        # Test with non-existent components
        template = factory.create_template(
            "software", 3,
            components=["nonexistent_component"]
        )
        assert template.name in ["software_basic", "software_advanced"]
        
        # Test with non-existent tags
        template = factory.create_template(
            "software", 3,
            tags=["nonexistent_tag"]
        )
        assert template.name in ["software_basic", "software_advanced"]
    
    def test_error_cases(self, factory, template_library):
        """Test error handling"""
        # Test when no templates are available at all
        template_library.find_templates.return_value = []
        
        with pytest.raises(ValueError) as exc_info:
            factory.create_template("software", 3)
        assert "No templates available" in str(exc_info.value)
    
    def test_scoring_system(self, factory):
        """Test the template scoring system"""
        # Test exact domain and complexity match
        score = factory.score_template(
            create_mock_template("test", "software", (1, 3)),
            domain="software",
            complexity=2
        )
        assert score > 0.8  # Should have high score for exact match
        
        # Test general domain fallback
        score = factory.score_template(
            create_mock_template("test", "general", (1, 5)),
            domain="software",
            complexity=2
        )
        assert 0.3 < score < 0.8  # Should have moderate score
        
        # Test complexity mismatch penalty
        score = factory.score_template(
            create_mock_template("test", "software", (1, 2)),
            domain="software",
            complexity=5
        )
        assert score < 0.5  # Should have lower score due to complexity mismatch
        
        # Test component matching
        template = create_mock_template(
            "test",
            "software",
            sections={"comp1": True, "comp2": True}
        )
        score = factory.score_template(
            template,
            domain="software",
            complexity=2,
            components=["comp1", "comp2"]
        )
        assert score > 0.8  # Should have high score for component match
        
        # Test tag matching
        template = create_mock_template(
            "test",
            "software",
            tags=["tag1", "tag2"]
        )
        score = factory.score_template(
            template,
            domain="software",
            complexity=2,
            tags=["tag1"]
        )
        assert score > 0.7  # Should have good score for tag match 