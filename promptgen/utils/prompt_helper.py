"""
Helper utilities for enhancing prompt generation with NLP.
"""

import re
from typing import Dict, List, Any, Optional

def extract_context_from_description(description: str, domain: str) -> Dict[str, Any]:
    """
    Extract relevant context from a user description based on the domain.
    
    Args:
        description: User's description of what they want to achieve
        domain: The selected domain (software, content, etc.)
        
    Returns:
        Dictionary with extracted context for template filling
    """
    # Base context with the original description
    context = {
        "objective": description,
        "complexity": 3  # Default complexity
    }
    
    # Domain-specific extraction patterns
    if domain == "software":
        # Extract technology stack if mentioned
        tech_stack_match = re.search(r"(?:using|with|in)\s+([A-Za-z0-9\s,\.+#]+?)\s+(?:for|to|as|framework|language)", description, re.IGNORECASE)
        if tech_stack_match:
            context["language_stack"] = tech_stack_match.group(1).strip()
        else:
            context["language_stack"] = "appropriate programming languages and frameworks"
        
        # Extract requirements
        context["requirements"] = extract_requirements(description)
        
        # Extract quality attributes
        quality_match = re.search(r"(?:should be|must be|needs to be)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if quality_match:
            context["quality_attributes"] = quality_match.group(1).strip()
        else:
            context["quality_attributes"] = "maintainable, secure, and performant"
            
        # Add architecture patterns
        context["architecture_patterns"] = "MVC, microservices, or other patterns as appropriate"
        
        # Extract potential data entities
        entities = extract_data_entities(description)
        if entities:
            context["data_entities"] = entities
    
    elif domain == "content":
        # Extract audience
        audience_match = re.search(r"(?:for|targeting|aimed at)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if audience_match:
            context["audience"] = audience_match.group(1).strip()
        else:
            context["audience"] = "target audience for this content"
        
        # Extract content type
        content_type_match = re.search(r"(?:create|write|develop)\s+(?:a|an)\s+([A-Za-z0-9\s,\.]+?)(?:for|to|that|which|about|\.)", description, re.IGNORECASE)
        if content_type_match:
            context["content_type"] = content_type_match.group(1).strip()
        else:
            context["content_type"] = "appropriate content format"
        
        # Extract tone
        tone_match = re.search(r"(?:tone|style|voice|language)\s+(?:should be|must be|needs to be|is|of)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if tone_match:
            context["tone"] = tone_match.group(1).strip()
        else:
            context["tone"] = "professional, conversational, or other appropriate tone"
        
        # Extract key messages
        context["key_messages"] = extract_key_points(description)
    
    elif domain == "business":
        # Extract stakeholders
        stakeholder_match = re.search(r"(?:for|targeting|aimed at|involving)\s+([A-Za-z0-9\s,\.]+?stakeholders|customers|clients|users|employees|management|executives|departments|teams)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if stakeholder_match:
            context["stakeholders"] = stakeholder_match.group(1).strip()
        else:
            context["stakeholders"] = "relevant business stakeholders"
        
        # Extract metrics
        metrics_match = re.search(r"(?:measure|metric|kpi|goal|target|objective)\s+(?:of|for|to|is|are)\s+([A-Za-z0-9\s,\.%$]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if metrics_match:
            context["metrics"] = metrics_match.group(1).strip()
        else:
            context["metrics"] = "appropriate business metrics and KPIs"
        
        # Extract timeline
        timeline_match = re.search(r"(?:within|in|over|for|during)\s+([A-Za-z0-9\s,\.]+?(?:days|weeks|months|years|quarters))(?:\.|\band\b|$)", description, re.IGNORECASE)
        if timeline_match:
            context["timeline"] = timeline_match.group(1).strip()
        else:
            context["timeline"] = "appropriate timeline"
        
        # Extract resources
        context["resources"] = "needed resources and constraints"
    
    elif domain == "creative":
        # Extract style
        style_match = re.search(r"(?:style|aesthetic|feel|look|appearance|design)\s+(?:of|should be|like|similar to|inspired by)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if style_match:
            context["style"] = style_match.group(1).strip()
        else:
            context["style"] = "appropriate creative style"
        
        # Extract emotional response
        emotion_match = re.search(r"(?:feel|feeling|emotion|mood|atmosphere|tone|evoke|inspire|convey)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if emotion_match:
            context["emotional_response"] = emotion_match.group(1).strip()
        else:
            context["emotional_response"] = "desired emotional impact"
        
        # Extract inspirations
        inspiration_match = re.search(r"(?:inspired by|like|similar to|in the style of|referencing)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if inspiration_match:
            context["inspirations"] = inspiration_match.group(1).strip()
        else:
            context["inspirations"] = "relevant sources of inspiration"
        
        # Extract constraints
        context["constraints"] = "creative constraints or requirements"
    
    elif domain == "education":
        # Extract learning objectives
        learning_match = re.search(r"(?:learn|teach|understand|comprehend|master|grasp)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if learning_match:
            context["learning_objectives"] = learning_match.group(1).strip()
        else:
            context["learning_objectives"] = "key learning goals"
        
        # Extract audience level
        level_match = re.search(r"(?:for|targeting|aimed at)\s+([A-Za-z0-9\s,\.]+?(?:beginners|intermediates|advanced|experts|students|learners|professionals|novices))(?:\.|\band\b|$)", description, re.IGNORECASE)
        if level_match:
            context["audience_level"] = level_match.group(1).strip()
        else:
            context["audience_level"] = "appropriate audience level"
        
        # Extract delivery method
        delivery_match = re.search(r"(?:through|via|using|by|with)\s+([A-Za-z0-9\s,\.]+?(?:course|lesson|module|tutorial|workshop|webinar|class|lecture|presentation))(?:\.|\band\b|$)", description, re.IGNORECASE)
        if delivery_match:
            context["delivery_method"] = delivery_match.group(1).strip()
        else:
            context["delivery_method"] = "appropriate educational format"
        
        # Extract assessment method
        assessment_match = re.search(r"(?:assess|evaluate|measure|test|quiz|exam)\s+([A-Za-z0-9\s,\.]+?)(?:\.|\band\b|$)", description, re.IGNORECASE)
        if assessment_match:
            context["assessment"] = assessment_match.group(1).strip()
        else:
            context["assessment"] = "appropriate assessment methods"
    
    # Set task based on domain
    context["task"] = "implementation" if domain == "software" else "creation"
    
    return context

def extract_requirements(description: str) -> str:
    """Extract potential requirements from a description."""
    requirements = []
    
    # Look for requirement patterns
    patterns = [
        r"(?:must|should|need to|has to|will|shall)\s+([^\.;,]+)(?:\.|\band\b|$)",
        r"(?:requirement is|requirements are|required to)\s+([^\.;,]+)(?:\.|\band\b|$)",
        r"(?:implement|create|build|develop|include|support)\s+([^\.;,]+?)(?:\.|\band\b|$)"
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, description, re.IGNORECASE)
        for match in matches:
            req = match.group(1).strip()
            if len(req) > 5 and req not in requirements:  # Avoid too short matches
                requirements.append(req)
    
    if not requirements:
        return "functional and non-functional requirements as appropriate"
    
    return "\n".join([f"- {req}" for req in requirements])

def extract_data_entities(description: str) -> str:
    """Extract potential data entities from a description."""
    entities = []
    
    # Look for entity patterns
    entity_pattern = r"(?:entity|model|table|object|class|data for|store|database for)\s+([A-Za-z0-9\s]+?)(?:s)?(?:\.|\band\b|$)"
    
    matches = re.finditer(entity_pattern, description, re.IGNORECASE)
    for match in matches:
        entity = match.group(1).strip()
        if len(entity) > 2 and entity not in entities:  # Avoid too short matches
            entities.append(entity)
    
    # Also look for nouns that might be entities
    nouns = re.findall(r'\b([A-Z][a-z]+|[a-z]+)\b', description)
    common_entities = ["user", "product", "order", "customer", "account", "profile", 
                      "transaction", "item", "category", "comment", "review", "post", 
                      "message", "notification", "event", "task", "project"]
    
    for noun in nouns:
        if noun.lower() in common_entities and noun not in entities:
            entities.append(noun.lower())
    
    if not entities:
        return "relevant data entities and their relationships"
    
    return "\n".join([f"- {entity.title()} entity with appropriate attributes" for entity in entities])

def extract_key_points(description: str) -> str:
    """Extract potential key points or messages from a description."""
    points = []
    
    # Look for key point patterns
    patterns = [
        r"(?:key points?|main points?|important points?|highlights?|key messages?|key aspects?)\s+(?:include|are|is)?\s*(?::|-|–|)?\s*([^\.;]+)(?:\.|\band\b|$)",
        r"(?:focus on|emphasize|highlight|stress|underscore)\s+([^\.;,]+)(?:\.|\band\b|$)",
        r"(?:covering|covering topics|discussing|explaining|about)\s+([^\.;,]+?)(?:\.|\band\b|$)"
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, description, re.IGNORECASE)
        for match in matches:
            point = match.group(1).strip()
            if len(point) > 5 and point not in points:  # Avoid too short matches
                points.append(point)
    
    # If no clear points found, extract sentences
    if not points and len(description) > 20:
        sentences = re.split(r'[.!?]', description)
        for sentence in sentences:
            if len(sentence.strip()) > 15:  # Only consider substantial sentences
                points.append(sentence.strip())
                if len(points) >= 3:  # Limit to 3 key points
                    break
    
    if not points:
        return "key messages to communicate with the audience"
    
    return "\n".join([f"- {point}" for point in points[:3]])  # Limit to top 3 points 