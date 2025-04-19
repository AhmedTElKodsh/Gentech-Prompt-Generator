"""
Content domain components for the AI Prompt Generator.

This module provides specialized content generators and domain knowledge
for content creation and writing-related prompts.
"""

from typing import Dict, List, Any, Optional
import logging

# Setup logger
logger = logging.getLogger(__name__)


class ContentCreationStrategy:
    """
    Strategy for generating content for content creation prompts.
    
    Implements the Strategy Pattern for content-specific content population.
    """
    
    def __init__(self):
        """Initialize the content creation strategy."""
        # Load content creation domain knowledge
        self.content_types = self._load_content_types()
        self.audience_considerations = self._load_audience_considerations()
        self.tone_and_voice = self._load_tone_and_voice()
        self.content_structures = self._load_content_structures()
        self.seo_best_practices = self._load_seo_best_practices()
    
    def populate(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Populate a template section with content creation-specific content.
        
        Args:
            section: Template section definition
            context: Content generation context
            
        Returns:
            Generated content for the section
        """
        section_name = section.get("name", "").lower()
        
        # Different generation strategies based on section type
        if section_name in ["context", "background", "introduction"]:
            return self._generate_context_content(section, context)
            
        elif section_name in ["contentstructure", "structure", "outline"]:
            return self._generate_structure_content(section, context)
            
        elif section_name in ["audience", "target audience", "readers"]:
            return self._generate_audience_content(section, context)
            
        elif section_name in ["toneguidelines", "tone", "voice", "style"]:
            return self._generate_tone_content(section, context)
            
        elif section_name in ["seo", "optimization", "keywords"]:
            return self._generate_seo_content(section, context)
            
        elif section_name in ["video editing", "editing guidelines", "video production"]:
            return self._generate_video_editing_content(section, context)
            
        # For other sections, use the template's default content
        return section.get("content_template", "").format(**context)
    
    def _generate_context_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for context/background sections."""
        objective = context.get("objective", "")
        content_type = context.get("content_type", "article")
        complexity = context.get("complexity", 3)
        
        # Get details for the content type
        content_info = self.content_types.get(content_type.lower(), 
                                             {"description": "a piece of content"})
        
        context_template = """
You are a professional content creator tasked with the following assignment:

{objective}

Content Details:
- Content Type: {content_type} - {content_description}
- Target Length: {target_length}
- Purpose: {purpose}
- Complexity Level: {complexity}/5
        """
        
        # Determine an appropriate target length based on content type
        default_length = content_info.get("default_length", "500-800 words")
        
        return context_template.format(
            objective=objective,
            content_type=content_type.title(),
            content_description=content_info.get("description", ""),
            target_length=context.get("target_length", default_length),
            purpose=context.get("purpose", "To inform and engage the audience"),
            complexity=complexity
        )
    
    def _generate_structure_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for structure sections."""
        content_type = context.get("content_type", "article").lower()
        complexity = context.get("complexity", 3)
        
        # Get structure for the content type
        structure_info = self.content_structures.get(content_type, {})
        sections = structure_info.get("sections", [])
        
        # Adjust sections based on complexity
        if complexity <= 2 and len(sections) > 3:
            sections = sections[:3]  # Simplified structure for low complexity
        elif complexity >= 4 and content_type in ["article", "blog post", "whitepaper"]:
            # Add more detailed sections for high complexity
            if "Further Reading" not in sections:
                sections.append("Further Reading")
            if "Expert Opinions" not in sections and complexity >= 5:
                sections.append("Expert Opinions")
        
        structure_template = """
Content Structure:

Your {content_type} should follow this structure:

{sections}

Additional Structure Guidelines:
- Each section should flow logically into the next
- Use appropriate headings and subheadings
- Include transitions between major sections
{additional_guidelines}
        """
        
        additional_guidelines = ""
        if content_type in ["article", "blog post", "guide"]:
            additional_guidelines = "- Consider using bullet points for readability\n- Break up long paragraphs"
        elif content_type in ["email", "newsletter"]:
            additional_guidelines = "- Keep paragraphs short and scannable\n- Use a clear call-to-action"
        elif content_type in ["script", "video script"]:
            additional_guidelines = "- Include timing guidelines\n- Note visual elements where relevant"
        
        return structure_template.format(
            content_type=content_type.title(),
            sections="\n".join(f"{i+1}. {section}" for i, section in enumerate(sections)),
            additional_guidelines=additional_guidelines
        )
    
    def _generate_audience_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for audience sections."""
        audience = context.get("audience", "general").lower()
        content_type = context.get("content_type", "article").lower()
        
        # Get audience considerations
        audience_info = self.audience_considerations.get(audience, {})
        characteristics = audience_info.get("characteristics", [])
        preferences = audience_info.get("preferences", [])
        considerations = audience_info.get("considerations", [])
        
        # Filter considerations based on content type
        relevant_considerations = []
        for item in considerations:
            if "all" in item.get("applies_to", []) or content_type in item.get("applies_to", []):
                relevant_considerations.append(item.get("description", ""))
        
        audience_template = """
Target Audience:

Your content is intended for {audience_name} readers.

Audience Characteristics:
{characteristics}

Content Preferences for this Audience:
{preferences}

Special Considerations:
{considerations}
        """
        
        return audience_template.format(
            audience_name=audience.title(),
            characteristics="\n".join(f"- {item}" for item in characteristics) if characteristics else "- General audience with varied backgrounds",
            preferences="\n".join(f"- {item}" for item in preferences) if preferences else "- Clear, straightforward content",
            considerations="\n".join(f"- {item}" for item in relevant_considerations) if relevant_considerations else "- Focus on clarity and value"
        )
    
    def _generate_tone_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for tone/voice sections."""
        tone = context.get("tone", "professional").lower()
        content_type = context.get("content_type", "article").lower()
        
        # Get tone guidelines
        tone_info = self.tone_and_voice.get(tone, {})
        characteristics = tone_info.get("characteristics", [])
        dos = tone_info.get("dos", [])
        donts = tone_info.get("donts", [])
        
        # Get content type specific tone adjustments
        content_tone_adjust = ""
        if content_type in ["email", "newsletter"]:
            content_tone_adjust = "For emails, be slightly more conversational and direct."
        elif content_type in ["whitepaper", "research"]:
            content_tone_adjust = "For formal documents, maintain a more authoritative and evidence-based tone."
        elif content_type in ["social media"]:
            content_tone_adjust = "For social media, be more concise and engaging."
        
        tone_template = """
Tone and Voice Guidelines:

The content should adopt a {tone} tone.

Tone Characteristics:
{characteristics}

Do's:
{dos}

Don'ts:
{donts}

{content_specific_tone}
        """
        
        return tone_template.format(
            tone=tone.title(),
            characteristics="\n".join(f"- {item}" for item in characteristics) if characteristics else "- Clear, straightforward, and focused",
            dos="\n".join(f"- {item}" for item in dos) if dos else "- Be clear and concise\n- Prioritize meaning over style",
            donts="\n".join(f"- {item}" for item in donts) if donts else "- Avoid overly complex language\n- Don't use clichés",
            content_specific_tone=content_tone_adjust
        )
    
    def _generate_seo_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for SEO sections."""
        content_type = context.get("content_type", "article").lower()
        complexity = context.get("complexity", 3)
        
        # Only provide SEO guidance for web content
        if content_type not in ["article", "blog post", "webpage", "landing page"]:
            return "SEO Considerations: Not applicable for this content type."
        
        # Get SEO best practices
        seo_practices = []
        for practice, details in self.seo_best_practices.items():
            if details.get("min_complexity", 1) <= complexity:
                seo_practices.append(f"{practice}: {details.get('description', '')}")
        
        # Limit to most important for lower complexity
        if complexity <= 3 and len(seo_practices) > 5:
            seo_practices = seo_practices[:5]
        
        seo_template = """
SEO Optimization Guidelines:

Primary Keyword Focus: {primary_keyword}
Secondary Keywords: {secondary_keywords}

SEO Best Practices to Apply:
{seo_practices}

Content Optimization Tips:
- Include keywords naturally, never force them
- Optimize headings (H1, H2, H3) with relevant keywords
- Ensure content provides value beyond keywords
- Consider user intent when creating content
        """
        
        return seo_template.format(
            primary_keyword=context.get("primary_keyword", "[Primary keyword]"),
            secondary_keywords=context.get("secondary_keywords", "[Secondary keyword 1], [Secondary keyword 2]"),
            seo_practices="\n".join(f"- {practice}" for practice in seo_practices)
        )
    
    def _generate_video_editing_content(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate content for video editing sections."""
        objective = context.get("objective", "")
        complexity = context.get("complexity", 3)
        
        # Determine the likely video type based on context
        video_type = context.get("video_type", "")
        if not video_type:
            if any(term in objective.lower() for term in ["youtube", "vlog", "tutorial"]):
                video_type = "YouTube/Tutorial"
            elif any(term in objective.lower() for term in ["ad", "commercial", "promo", "advertisement"]):
                video_type = "Commercial/Advertisement"
            elif any(term in objective.lower() for term in ["social", "instagram", "tiktok", "reels", "shorts"]):
                video_type = "Social Media Short"
            elif any(term in objective.lower() for term in ["documentary", "film", "movie", "short film"]):
                video_type = "Film/Documentary"
            elif any(term in objective.lower() for term in ["corporate", "business", "presentation"]):
                video_type = "Corporate/Business"
            else:
                video_type = "General Video"
        
        # Determine suitable editing styles
        editing_styles = []
        if video_type == "YouTube/Tutorial":
            editing_styles = ["Cut to talking points", "B-roll overlays", "Text/graphic overlays", "Jump cuts"]
        elif video_type == "Commercial/Advertisement":
            editing_styles = ["Fast-paced cuts", "Visual effects", "Color grading", "Motion graphics"]
        elif video_type == "Social Media Short":
            editing_styles = ["Vertical format", "Quick transitions", "Text overlays", "Trending effects"]
        elif video_type == "Film/Documentary":
            editing_styles = ["Long takes", "Seamless transitions", "Atmospheric color grading", "Minimal text"]
        elif video_type == "Corporate/Business":
            editing_styles = ["Clean transitions", "Limited effects", "Corporate branding", "Text-based information"]
        else:
            editing_styles = ["Basic cuts", "Transitions", "Text overlays", "Background music"]
        
        video_editing_template = """
Video Editing Guidelines:

1. Project Details:
   - Video Type: {video_type}
   - Target Platform: {platform}
   - Estimated Length: {duration}
   - Target Audience: {audience}

2. Recommended Editing Approach:
{editing_styles}

3. Technical Specifications:
   - Resolution: {resolution}
   - Frame Rate: {frame_rate}
   - Aspect Ratio: {aspect_ratio}
   - Audio: {audio_specs}

4. Post-Production Workflow:
   - Begin with organizing and reviewing all footage
   - Create a rough cut focusing on narrative structure
   - Refine with precise cuts and transitions
   - Add visual effects, text, and graphics as needed
   - Color correction and audio enhancement
   - Final review for technical quality and storytelling
   - Export according to platform specifications
        """
        
        # Default technical specifications based on video type
        resolution = "1920x1080 (1080p Full HD)"
        frame_rate = "30fps"
        aspect_ratio = "16:9"
        platform = "Multiple platforms"
        duration = "3-5 minutes"
        audience = "General audience"
        audio_specs = "Stereo, 48kHz"
        
        # Adjust specs based on video type
        if video_type == "Social Media Short":
            resolution = "1080x1920 (9:16 vertical)"
            aspect_ratio = "9:16"
            duration = "15-60 seconds"
            platform = "Instagram, TikTok, YouTube Shorts"
        elif video_type == "YouTube/Tutorial":
            duration = "8-15 minutes"
            platform = "YouTube"
        elif video_type == "Commercial/Advertisement":
            duration = "15-60 seconds"
            frame_rate = "24fps or 30fps"
        elif video_type == "Film/Documentary":
            resolution = "3840x2160 (4K UHD)"
            frame_rate = "24fps"
            duration = "10+ minutes"
            audio_specs = "5.1 surround sound, 48kHz"
        
        # Override with context values if provided
        if "resolution" in context:
            resolution = context["resolution"]
        if "frame_rate" in context:
            frame_rate = context["frame_rate"]
        if "aspect_ratio" in context:
            aspect_ratio = context["aspect_ratio"]
        if "platform" in context:
            platform = context["platform"]
        if "duration" in context:
            duration = context["duration"]
        if "audience" in context:
            audience = context["audience"]
        if "audio_specs" in context:
            audio_specs = context["audio_specs"]
        
        return video_editing_template.format(
            video_type=video_type,
            platform=platform,
            duration=duration,
            audience=audience,
            editing_styles="\n".join(f"   - {style}" for style in editing_styles),
            resolution=resolution,
            frame_rate=frame_rate,
            aspect_ratio=aspect_ratio,
            audio_specs=audio_specs
        )
    
    def _load_content_types(self) -> Dict[str, Any]:
        """Load information about different content types."""
        return {
            "article": {
                "description": "an informative piece exploring a topic in depth",
                "default_length": "800-1200 words",
                "sections": ["Introduction", "Main Body", "Conclusion"],
                "complexity_range": [1, 5]
            },
            "blog post": {
                "description": "a conversational piece providing value on a specific topic",
                "default_length": "600-1000 words",
                "sections": ["Hook/Introduction", "Main Points", "Conclusion", "Call to Action"],
                "complexity_range": [1, 4]
            },
            "social media post": {
                "description": "a concise, engaging update designed for social platforms",
                "default_length": "50-280 characters (platform dependent)",
                "sections": ["Hook", "Core Message", "Call to Action"],
                "complexity_range": [1, 2]
            },
            "email": {
                "description": "a direct communication to a subscriber or customer",
                "default_length": "200-500 words",
                "sections": ["Subject Line", "Greeting", "Body", "Call to Action", "Signature"],
                "complexity_range": [1, 3]
            },
            "newsletter": {
                "description": "a regular update sent to subscribers with various content pieces",
                "default_length": "500-800 words",
                "sections": ["Header", "Main Story", "Secondary Points", "News Updates", "Call to Action"],
                "complexity_range": [2, 4]
            },
            "whitepaper": {
                "description": "an authoritative, detailed document on a specific topic",
                "default_length": "2000-5000 words",
                "sections": ["Executive Summary", "Introduction", "Problem Statement", "Methodology", "Findings", "Conclusion", "References"],
                "complexity_range": [3, 5]
            },
            "landing page": {
                "description": "a focused webpage designed to convert visitors",
                "default_length": "300-800 words",
                "sections": ["Headline", "Problem Statement", "Solution", "Benefits", "Social Proof", "Call to Action"],
                "complexity_range": [2, 4]
            },
            "press release": {
                "description": "an official statement distributed to news outlets",
                "default_length": "400-800 words",
                "sections": ["Headline", "Dateline", "Lead Paragraph", "Body", "Company Information", "Contact Information"],
                "complexity_range": [2, 4]
            },
            "product description": {
                "description": "compelling content that explains product benefits and features",
                "default_length": "200-400 words",
                "sections": ["Overview", "Key Benefits", "Features", "Specifications", "Call to Action"],
                "complexity_range": [1, 3]
            },
            "script": {
                "description": "a document outlining dialogue and actions for audio/video content",
                "default_length": "150-200 words per minute of content",
                "sections": ["Introduction", "Main Content", "Conclusion", "Call to Action"],
                "complexity_range": [2, 5]
            }
        }
    
    def _load_audience_considerations(self) -> Dict[str, Any]:
        """Load information about different audience types."""
        return {
            "general": {
                "characteristics": [
                    "Diverse background and knowledge levels",
                    "Various interests and needs",
                    "May have limited time for content consumption"
                ],
                "preferences": [
                    "Clear, straightforward language",
                    "Easily scannable content",
                    "Practical, useful information"
                ],
                "considerations": [
                    {"description": "Avoid industry jargon without explanation", "applies_to": ["all"]},
                    {"description": "Use examples that are broadly relatable", "applies_to": ["all"]},
                    {"description": "Balance depth with accessibility", "applies_to": ["article", "blog post", "whitepaper"]}
                ]
            },
            "technical": {
                "characteristics": [
                    "Specialized knowledge in their field",
                    "Often well-educated in specific domains",
                    "Looking for detailed, accurate information",
                    "Value precision over simplicity"
                ],
                "preferences": [
                    "In-depth technical details",
                    "Evidence-based content",
                    "Logical, structured presentation",
                    "Proper use of technical terminology"
                ],
                "considerations": [
                    {"description": "Use industry-specific terminology appropriately", "applies_to": ["all"]},
                    {"description": "Provide data and evidence to support claims", "applies_to": ["whitepaper", "article", "blog post"]},
                    {"description": "Focus on specificity rather than broad generalizations", "applies_to": ["all"]},
                    {"description": "Include technical specifications where relevant", "applies_to": ["product description", "whitepaper"]}
                ]
            },
            "executive": {
                "characteristics": [
                    "Time-constrained decision makers",
                    "Focus on business impact and outcomes",
                    "Need for high-level strategic information",
                    "Value insights that drive business decisions"
                ],
                "preferences": [
                    "Concise, to-the-point content",
                    "Clear business value and ROI information",
                    "Strategic implications highlighted",
                    "Easily scannable executive summaries"
                ],
                "considerations": [
                    {"description": "Start with key takeaways or executive summary", "applies_to": ["all"]},
                    {"description": "Focus on business impact and results", "applies_to": ["all"]},
                    {"description": "Use data visualizations to convey complex information quickly", "applies_to": ["whitepaper", "presentation"]},
                    {"description": "Avoid excessive technical details unless specifically requested", "applies_to": ["all"]}
                ]
            },
            "consumer": {
                "characteristics": [
                    "Interested in benefits over features",
                    "Emotionally driven purchasing decisions",
                    "Various levels of product knowledge",
                    "May be comparing multiple options"
                ],
                "preferences": [
                    "Benefit-focused messaging",
                    "Relatable, conversational tone",
                    "Visuals that demonstrate product use",
                    "Social proof and testimonials"
                ],
                "considerations": [
                    {"description": "Emphasize how the product/service improves their life", "applies_to": ["product description", "landing page", "email"]},
                    {"description": "Use emotional triggers appropriate to the product", "applies_to": ["all"]},
                    {"description": "Include social proof like reviews or testimonials", "applies_to": ["landing page", "product description"]},
                    {"description": "Address common questions and objections", "applies_to": ["all"]}
                ]
            },
            "academic": {
                "characteristics": [
                    "Highly educated in their field",
                    "Value rigorous research and methodology",
                    "Critical evaluation of evidence and claims",
                    "Interest in theoretical frameworks"
                ],
                "preferences": [
                    "Well-structured, logical argumentation",
                    "Proper citations and references",
                    "Comprehensive literature review",
                    "Methodological transparency"
                ],
                "considerations": [
                    {"description": "Use formal academic style appropriate to the discipline", "applies_to": ["all"]},
                    {"description": "Include comprehensive citations and references", "applies_to": ["whitepaper", "article"]},
                    {"description": "Acknowledge limitations and alternative viewpoints", "applies_to": ["whitepaper", "article"]},
                    {"description": "Maintain theoretical rigor throughout", "applies_to": ["all"]}
                ]
            }
        }
    
    def _load_tone_and_voice(self) -> Dict[str, Any]:
        """Load information about different tones and voices."""
        return {
            "professional": {
                "characteristics": [
                    "Polished and refined language",
                    "Authoritative without being pretentious",
                    "Clear, direct, and efficient communication",
                    "Appropriate level of formality"
                ],
                "dos": [
                    "Use industry terminology appropriately",
                    "Maintain consistent level of formality",
                    "Structure content logically",
                    "Be precise and accurate"
                ],
                "donts": [
                    "Avoid slang and overly casual expressions",
                    "Don't use excessive jargon",
                    "Avoid overly complex sentences",
                    "Don't use unprofessional or contentious examples"
                ]
            },
            "conversational": {
                "characteristics": [
                    "Natural, everyday language",
                    "Personable and approachable",
                    "Engaging and relatable",
                    "Slightly informal but still appropriate"
                ],
                "dos": [
                    "Write as if speaking directly to the reader",
                    "Use contractions (don't, you're, we'll)",
                    "Ask questions to engage the reader",
                    "Include personal anecdotes where appropriate"
                ],
                "donts": [
                    "Don't sacrifice clarity for casualness",
                    "Avoid overly informal expressions or slang",
                    "Don't ramble or use run-on sentences",
                    "Avoid inappropriate humor or examples"
                ]
            },
            "academic": {
                "characteristics": [
                    "Formal and objective language",
                    "Precise terminology and definitions",
                    "Evidence-based argumentation",
                    "Structured and methodical presentation"
                ],
                "dos": [
                    "Use discipline-specific terminology accurately",
                    "Cite sources properly",
                    "Present balanced viewpoints",
                    "Structure arguments logically and systematically"
                ],
                "donts": [
                    "Avoid first-person perspective (unless appropriate for the discipline)",
                    "Don't make claims without evidence",
                    "Avoid emotional or subjective language",
                    "Don't oversimplify complex concepts"
                ]
            },
            "persuasive": {
                "characteristics": [
                    "Compelling and influential language",
                    "Emotional appeals balanced with logic",
                    "Strong calls to action",
                    "Benefit-focused messaging"
                ],
                "dos": [
                    "Use powerful, active verbs",
                    "Include persuasive techniques like social proof",
                    "Address potential objections",
                    "Create a sense of urgency when appropriate"
                ],
                "donts": [
                    "Don't make false or unsubstantiated claims",
                    "Avoid manipulative language",
                    "Don't use high-pressure tactics",
                    "Avoid obvious exaggerations or hyperbole"
                ]
            },
            "friendly": {
                "characteristics": [
                    "Warm and welcoming language",
                    "Highly approachable and encouraging",
                    "Positive and supportive tone",
                    "Personal connection with reader"
                ],
                "dos": [
                    "Use inclusive language (we, us, together)",
                    "Be encouraging and supportive",
                    "Express genuine enthusiasm",
                    "Use light humor when appropriate"
                ],
                "donts": [
                    "Don't be overly familiar or presumptuous",
                    "Avoid forced friendliness or inauthenticity",
                    "Don't sacrifice professionalism for friendliness",
                    "Avoid potentially divisive topics"
                ]
            }
        }
    
    def _load_content_structures(self) -> Dict[str, Any]:
        """Load structure templates for different content types."""
        return {
            "article": {
                "sections": [
                    "Introduction/Hook",
                    "Background/Context",
                    "Main Point 1 with Evidence",
                    "Main Point 2 with Evidence",
                    "Main Point 3 with Evidence",
                    "Counterarguments/Limitations",
                    "Conclusion",
                    "Call to Action"
                ]
            },
            "blog post": {
                "sections": [
                    "Attention-Grabbing Hook",
                    "Introduction to Problem/Topic",
                    "Key Point 1 with Examples",
                    "Key Point 2 with Examples",
                    "Key Point 3 with Examples",
                    "Practical Applications",
                    "Conclusion",
                    "Call to Action"
                ]
            },
            "social media post": {
                "sections": [
                    "Hook/Attention Grabber",
                    "Core Message",
                    "Supporting Detail (if space allows)",
                    "Call to Action"
                ]
            },
            "email": {
                "sections": [
                    "Subject Line",
                    "Personalized Greeting",
                    "Opening Hook",
                    "Main Message",
                    "Clear Call to Action",
                    "Appropriate Sign-off",
                    "P.S. (optional but effective)"
                ]
            },
            "whitepaper": {
                "sections": [
                    "Executive Summary",
                    "Introduction/Problem Statement",
                    "Background/Industry Context",
                    "Methodology/Approach",
                    "Research Findings/Analysis",
                    "Practical Implications",
                    "Recommendations",
                    "Conclusion",
                    "References/Citations"
                ]
            },
            "landing page": {
                "sections": [
                    "Headline (Problem or Promise)",
                    "Subheadline (Expanding on Headline)",
                    "Problem Statement (Pain Points)",
                    "Solution Introduction",
                    "Key Benefits (3-5)",
                    "Features Explanation",
                    "Social Proof (Testimonials/Case Studies)",
                    "Objection Handling",
                    "Primary Call to Action",
                    "Secondary Call to Action"
                ]
            },
            "product description": {
                "sections": [
                    "Compelling Product Name/Title",
                    "Overview/Summary",
                    "Key Benefits (3-5)",
                    "Technical Specifications",
                    "Use Cases/Who It's For",
                    "Differentiators from Alternatives",
                    "Call to Action"
                ]
            }
        }
    
    def _load_seo_best_practices(self) -> Dict[str, Any]:
        """Load SEO best practices for content creation."""
        return {
            "Keyword Optimization": {
                "description": "Include target keywords in title, headings, and naturally throughout content",
                "min_complexity": 1
            },
            "Meta Description": {
                "description": "Craft a compelling meta description that includes keywords and encourages clicks",
                "min_complexity": 2
            },
            "Title Tag Optimization": {
                "description": "Create a unique, keyword-rich title under 60 characters",
                "min_complexity": 1
            },
            "Header Tag Hierarchy": {
                "description": "Use a logical H1-H6 structure with keywords in important headings",
                "min_complexity": 2
            },
            "Internal Linking": {
                "description": "Link to other relevant content on your site using descriptive anchor text",
                "min_complexity": 2
            },
            "External Linking": {
                "description": "Link to authoritative external sources to support your content",
                "min_complexity": 3
            },
            "Image Optimization": {
                "description": "Use descriptive filenames and alt text for all images",
                "min_complexity": 2
            },
            "URL Structure": {
                "description": "Create clean, keyword-rich URLs that describe the content",
                "min_complexity": 2
            },
            "Mobile Optimization": {
                "description": "Ensure content is easily readable on mobile devices",
                "min_complexity": 3
            },
            "Page Load Speed": {
                "description": "Optimize images and minimize code to improve page speed",
                "min_complexity": 4
            },
            "Semantic SEO": {
                "description": "Use related terms and concepts to build topical authority",
                "min_complexity": 4
            },
            "Featured Snippet Optimization": {
                "description": "Structure content to potentially appear in featured snippets (listicles, definitions, tables)",
                "min_complexity": 4
            },
            "LSI Keywords": {
                "description": "Include Latent Semantic Indexing keywords related to your main keyword",
                "min_complexity": 3
            }
        }


# Default instance for convenience
default_strategy = ContentCreationStrategy()


def populate_section(section: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Convenience function to populate a section using the default strategy.
    
    Args:
        section: Section definition
        context: Content generation context
        
    Returns:
        Generated content
    """
    return default_strategy.populate(section, context) 