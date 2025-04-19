#!/usr/bin/env python3
"""
Test suite for the DomainClassifier.

This module contains comprehensive tests for the domain classification functionality,
testing various input cases and edge conditions.
"""

import unittest
from promptgen.core.classifier import DomainClassifier

class TestDomainClassifier(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.classifier = DomainClassifier()
        
    def test_software_domain(self):
        """Test software development domain classification."""
        test_cases = [
            "Create a Python web application using Flask",
            "Debug my React component that's not rendering properly",
            "Help me write a unit test for my database connection",
            "Design a REST API for user authentication"
        ]
        
        for case in test_cases:
            domain, confidence = self.classifier.classify_domain(case)
            self.assertEqual(domain, "software")
            self.assertGreater(confidence, 0.5)
            
    def test_content_domain(self):
        """Test content creation domain classification."""
        test_cases = [
            "Write a blog post about artificial intelligence",
            "Create engaging social media content for my business",
            "Help me edit my YouTube video script",
            "Draft an email newsletter for my subscribers"
        ]
        
        for case in test_cases:
            domain, confidence = self.classifier.classify_domain(case)
            self.assertEqual(domain, "content")
            self.assertGreater(confidence, 0.5)
            
    def test_business_domain(self):
        """Test business strategy domain classification."""
        test_cases = [
            "Create a business plan for my startup",
            "Analyze market trends in the tech industry",
            "Develop a sales strategy for Q4",
            "Write an investor pitch deck"
        ]
        
        for case in test_cases:
            domain, confidence = self.classifier.classify_domain(case)
            self.assertEqual(domain, "business")
            self.assertGreater(confidence, 0.5)
            
    def test_data_analysis_domain(self):
        """Test data analysis domain classification."""
        test_cases = [
            "Create a dashboard showing sales metrics",
            "Analyze customer behavior patterns in our dataset",
            "Generate a report on website traffic trends",
            "Build a predictive model for user churn"
        ]
        
        for case in test_cases:
            domain, confidence = self.classifier.classify_domain(case)
            self.assertEqual(domain, "data_analysis")
            self.assertGreater(confidence, 0.5)
            
    def test_technical_documentation_domain(self):
        """Test technical documentation domain classification."""
        test_cases = [
            "Write API documentation for our REST endpoints",
            "Create a user manual for our software",
            "Document the system architecture",
            "Write technical specifications for new features"
        ]
        
        for case in test_cases:
            domain, confidence = self.classifier.classify_domain(case)
            self.assertEqual(domain, "technical_documentation")
            self.assertGreater(confidence, 0.5)
            
    def test_mixed_domain_cases(self):
        """Test cases that might involve multiple domains."""
        test_cases = [
            ("Create a data visualization website using D3.js", ["software", "data_analysis"]),
            ("Write technical documentation for our API endpoints", ["technical_documentation", "software"]),
            ("Develop a content management system", ["software", "content"]),
            ("Create a business analytics dashboard", ["business", "data_analysis"])
        ]
        
        for case, expected_domains in test_cases:
            domain, confidence = self.classifier.classify_domain(case)
            self.assertIn(domain, expected_domains)
            self.assertGreater(confidence, 0.3)  # Lower threshold for mixed cases
            
    def test_edge_cases(self):
        """Test edge cases and potential error conditions."""
        test_cases = [
            ("", "general"),  # Empty string
            ("   ", "general"),  # Whitespace only
            ("xyz123", "general"),  # Random string
            ("Help me", "general"),  # Very generic request
            ("I need assistance", "general")  # Generic assistance request
        ]
        
        for case, expected_domain in test_cases:
            domain, confidence = self.classifier.classify_domain(case)
            self.assertEqual(domain, expected_domain)
            
    def test_case_insensitivity(self):
        """Test that classification is case-insensitive."""
        lowercase = "create a python web application"
        uppercase = "CREATE A PYTHON WEB APPLICATION"
        mixed_case = "Create A Python Web Application"
        
        domain1, conf1 = self.classifier.classify_domain(lowercase)
        domain2, conf2 = self.classifier.classify_domain(uppercase)
        domain3, conf3 = self.classifier.classify_domain(mixed_case)
        
        self.assertEqual(domain1, domain2)
        self.assertEqual(domain2, domain3)
        self.assertAlmostEqual(conf1, conf2, places=2)
        self.assertAlmostEqual(conf2, conf3, places=2)

if __name__ == '__main__':
    unittest.main() 