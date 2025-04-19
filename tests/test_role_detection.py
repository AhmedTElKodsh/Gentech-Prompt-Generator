"""
Tests for the role-based domain detection functionality.
"""

import unittest
from promptgen.domains.domain_service import DomainService

class TestRoleDetection(unittest.TestCase):
    """Test cases for the role-based domain detection in DomainService."""
    
    def setUp(self):
        """Set up the test environment."""
        self.domain_service = DomainService()
    
    def test_software_role_detection(self):
        """Test detection of software development roles."""
        test_cases = [
            ("Software Developer: I need to create a REST API for user authentication", "software"),
            ("Developer: How do I implement pagination in a React application?", "software"),
            ("As a full stack developer, I need to connect my frontend to a backend API", "software"),
            ("Backend Developer - Need to optimize database queries for performance", "software"),
            ("Frontend Developer, looking to implement responsive design patterns", "software")
        ]
        
        for objective, expected_domain in test_cases:
            domain, cleaned_objective = self.domain_service.extract_role_from_objective(objective)
            self.assertEqual(domain, expected_domain, f"Failed to detect '{expected_domain}' domain in '{objective}'")
            self.assertNotIn(objective.split(':')[0].split('-')[0].split(',')[0].strip(), cleaned_objective, 
                          f"Role prefix not properly removed from '{objective}'")
    
    def test_digital_marketing_role_detection(self):
        """Test detection of digital marketing roles."""
        test_cases = [
            ("Digital Marketer: Need to create an email campaign for product launch", "content"),
            ("SEO Specialist - How to improve organic search rankings for a B2B website", "content"),
            ("As a social media manager, I need content ideas for Instagram", "content"),
            ("Marketing Analyst: Looking to track conversion rates from different channels", "business"),
            ("Digital Marketing Manager, need to develop a content calendar", "content")
        ]
        
        for objective, expected_domain in test_cases:
            domain, cleaned_objective = self.domain_service.extract_role_from_objective(objective)
            self.assertEqual(domain, expected_domain, f"Failed to detect '{expected_domain}' domain in '{objective}'")
            self.assertNotIn(objective.split(':')[0].split('-')[0].split(',')[0].strip(), cleaned_objective, 
                          f"Role prefix not properly removed from '{objective}'")
    
    def test_content_creation_role_detection(self):
        """Test detection of content creation roles."""
        test_cases = [
            ("Content Creator: How to write compelling product descriptions", "content"),
            ("Copywriter - Need to create persuasive landing page copy", "content"),
            ("As a blogger, I need to create an outline for a how-to article", "content"),
            ("Content Writer: Tips for technical writing", "content"),
            ("Journalist, need to structure a feature article", "content")
        ]
        
        for objective, expected_domain in test_cases:
            domain, cleaned_objective = self.domain_service.extract_role_from_objective(objective)
            self.assertEqual(domain, expected_domain, f"Failed to detect '{expected_domain}' domain in '{objective}'")
            self.assertNotIn(objective.split(':')[0].split('-')[0].split(',')[0].strip(), cleaned_objective, 
                          f"Role prefix not properly removed from '{objective}'")
    
    def test_video_editing_role_detection(self):
        """Test detection of video editing roles."""
        test_cases = [
            ("Video Editor: How to create smooth transitions between clips", "content"),
            ("Videographer - Need cinematic color grading techniques", "content"),
            ("As a film editor, I need to improve pacing in dialogue scenes", "content"),
            ("Video Producer: Best practices for YouTube tutorial videos", "content"),
            ("Motion Graphics Designer, need to create animated lower thirds", "content")
        ]
        
        for objective, expected_domain in test_cases:
            domain, cleaned_objective = self.domain_service.extract_role_from_objective(objective)
            self.assertEqual(domain, expected_domain, f"Failed to detect '{expected_domain}' domain in '{objective}'")
            self.assertNotIn(objective.split(':')[0].split('-')[0].split(',')[0].strip(), cleaned_objective, 
                          f"Role prefix not properly removed from '{objective}'")
    
    def test_no_role_prefix(self):
        """Test handling of inputs with no role prefix."""
        objectives = [
            "Create a REST API for user authentication",
            "How do I implement pagination in a React application?",
            "I need to develop a content calendar for social media",
            "Tips for smooth video transitions"
        ]
        
        for objective in objectives:
            domain, cleaned_objective = self.domain_service.extract_role_from_objective(objective)
            self.assertEqual(domain, "general", f"Incorrectly detected a domain for '{objective}'")
            self.assertEqual(cleaned_objective, objective, f"Objective was modified when no role was present: '{objective}'")
    
    def test_role_pattern_variations(self):
        """Test different formats of role specifications."""
        variations = [
            ("Software Developer: Task description", "software"),
            ("Software Developer - Task description", "software"),
            ("Software Developer, Task description", "software"),
            ("Software Developer   Task description", "software"),
            ("As a Software Developer, I need to Task description", "software")
        ]
        
        for objective, expected_domain in variations:
            domain, cleaned_objective = self.domain_service.extract_role_from_objective(objective)
            self.assertEqual(domain, expected_domain, f"Failed to detect '{expected_domain}' domain in '{objective}'")


if __name__ == '__main__':
    unittest.main() 