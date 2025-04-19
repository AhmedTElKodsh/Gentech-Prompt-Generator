"""
Advanced prompting techniques for the AI Prompt Generator.

This module implements more sophisticated prompting techniques
beyond the basic ones in the library module.
"""

from typing import Dict, List, Any, Optional
from .library import PromptTechnique


class TreeOfThoughtsTechnique(PromptTechnique):
    """
    Tree of Thoughts technique extends Chain of Thought by considering multiple reasoning paths.
    
    This technique helps LLMs explore different approaches to a problem and select
    the most promising path.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply tree of thoughts reasoning to the prompt."""
        context = context or {}
        num_paths = context.get("num_paths", 3)
        evaluation_criteria = context.get("evaluation_criteria", "correctness, efficiency, and simplicity")
        
        tot_prefix = (
            f"For this task, explore {num_paths} different approaches before determining the best solution.\n\n"
            "For each approach:\n"
            "1. Describe the approach\n"
            "2. Reason step-by-step through the execution\n"
            "3. Evaluate the pros and cons\n\n"
        )
        
        tot_suffix = (
            f"\n\nAfter exploring these approaches, select the best one based on {evaluation_criteria}. "
            "Explain why you chose this approach, then implement the full solution using the chosen approach."
        )
        
        return f"{tot_prefix}{prompt_content}{tot_suffix}"


class ReActTechnique(PromptTechnique):
    """
    ReAct (Reasoning + Acting) technique combines reasoning with simulated actions.
    
    This technique is particularly useful for tasks that involve both thinking and doing,
    such as information gathering, tool use, or multi-step processes.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply ReAct pattern to the prompt."""
        context = context or {}
        available_actions = context.get("available_actions", ["Search", "Analyze", "Calculate", "Decide"])
        
        react_prefix = (
            "Solve this problem by alternating between Reasoning and Acting.\n\n"
            "For each step:\n"
            "1. Think: Reason about the current state and what to do next\n"
            "2. Act: Choose one of these actions: " + ", ".join(available_actions) + "\n"
            "3. Observe: Consider the result of your action\n\n"
            "Continue this process until you reach a solution.\n\n"
        )
        
        react_example = (
            "Example of the format:\n"
            "Think: I need to understand what data is available.\n"
            "Act: Search for relevant information\n"
            "Observe: I found X, Y, and Z.\n"
            "Think: Now I need to analyze this information...\n\n"
        )
        
        return f"{react_prefix}{react_example}Problem:\n{prompt_content}\n\nSolution:"


class SelfConsistencyTechnique(PromptTechnique):
    """
    Self-consistency technique generates multiple solutions and selects the most consistent one.
    
    This technique improves reliability by having the LLM generate multiple reasoning paths
    and taking the most common answer.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply self-consistency technique to the prompt."""
        context = context or {}
        num_solutions = context.get("num_solutions", 3)
        
        consistency_prefix = (
            f"Generate {num_solutions} different solutions to this problem. For each solution:\n"
            "1. Use a different approach or perspective\n"
            "2. Reason step-by-step to reach your answer\n"
            "3. Clearly state your final answer\n\n"
            "After generating all solutions, compare them and select the most consistent answer. "
            "If the answers differ, explain why you believe your final selection is correct.\n\n"
        )
        
        return f"{consistency_prefix}Problem:\n{prompt_content}"


class ReflexionTechnique(PromptTechnique):
    """
    Reflexion technique incorporates self-reflection into the reasoning process.
    
    This technique helps the LLM evaluate and improve its own responses by critiquing
    them and making refinements.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply reflexion technique to the prompt."""
        context = context or {}
        reflection_points = context.get("reflection_points", ["accuracy", "completeness", "clarity"])
        
        reflexion_prefix = (
            "Approach this task in three phases:\n\n"
            "Phase 1: Generate an initial response to the problem\n"
            f"Phase 2: Reflect on your initial response, evaluating it for {', '.join(reflection_points)}\n"
            "Phase 3: Provide an improved response based on your reflection\n\n"
        )
        
        return f"{reflexion_prefix}Problem:\n{prompt_content}"


class GenerateKnowledgeTechnique(PromptTechnique):
    """
    Generate Knowledge technique has the LLM first generate relevant knowledge before answering.
    
    This technique improves responses by having the LLM explicitly retrieve or generate
    relevant information before attempting to solve the problem.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply generate knowledge technique to the prompt."""
        context = context or {}
        knowledge_type = context.get("knowledge_type", "facts, concepts, and principles")
        
        knowledge_prefix = (
            f"Before answering this question, first identify the relevant {knowledge_type} you'll need.\n\n"
            "Step 1: List the key information needed to answer this question\n"
            "Step 2: For each item, provide the relevant knowledge\n"
            "Step 3: Use this knowledge to formulate your answer\n\n"
        )
        
        return f"{knowledge_prefix}Question:\n{prompt_content}"


class PrefillResponseTechnique(PromptTechnique):
    """
    Prefill Response technique provides a partial response structure for the LLM to complete.
    
    This technique guides the structure and format of the LLM's response by providing
    a template or beginning that it should continue.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply prefill response technique to the prompt."""
        context = context or {}
        response_template = context.get("response_template", "")
        
        if not response_template:
            # Create a generic template based on the prompt
            if "analyze" in prompt_content.lower() or "review" in prompt_content.lower():
                response_template = (
                    "Analysis:\n"
                    "1. Key Points:\n"
                    "2. Strengths:\n"
                    "3. Areas for Improvement:\n"
                    "4. Recommendations:\n"
                )
            elif "steps" in prompt_content.lower() or "how to" in prompt_content.lower():
                response_template = (
                    "Step-by-Step Guide:\n"
                    "Step 1: \n"
                    "Step 2: \n"
                    "Step 3: \n"
                    "Additional Tips:\n"
                )
            else:
                response_template = "Here's my response:\n\n"
        
        prefill_instruction = (
            f"Please complete the following response template:\n\n{response_template}\n\n"
            "Feel free to add more sections or details as necessary, but maintain this basic structure."
        )
        
        return f"{prompt_content}\n\n{prefill_instruction}"


class DirectionalStimulusTechnique(PromptTechnique):
    """
    Directional Stimulus technique provides specific guidance to influence the direction of the response.
    
    This technique uses targeted prompts to guide the LLM's thinking in a particular direction
    without fully constraining it.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply directional stimulus technique to the prompt."""
        context = context or {}
        direction = context.get("direction", "")
        stimulus = context.get("stimulus", "")
        
        if not direction or not stimulus:
            return prompt_content
        
        directional_prefix = f"When approaching this task, consider the {direction} perspective: {stimulus}\n\n"
        
        return f"{directional_prefix}{prompt_content}"


class PromptChainingTechnique(PromptTechnique):
    """
    Prompt Chaining technique breaks complex tasks into a sequence of simpler prompts.
    
    This technique improves complex task performance by having the LLM solve a series
    of smaller, more manageable steps.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply prompt chaining technique to the prompt."""
        context = context or {}
        steps = context.get("steps", [])
        
        if not steps:
            # Create generic steps based on the prompt
            steps = [
                "Understand the problem and identify key requirements",
                "Break down the problem into manageable components",
                "Address each component in sequence",
                "Integrate the solutions to each component",
                "Review and refine the integrated solution"
            ]
        
        chaining_prefix = (
            "This task will be solved in a series of steps. For each step:\n"
            "1. Focus only on that specific step\n"
            "2. Use the outputs from previous steps as inputs\n"
            "3. Clearly indicate the output of each step\n\n"
            "Steps to follow:\n"
        )
        
        steps_text = "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
        
        return f"{chaining_prefix}{steps_text}\n\nTask:\n{prompt_content}\n\nBegin with step 1:"


class GraphPromptingTechnique(PromptTechnique):
    """
    Graph Prompting technique represents knowledge and reasoning as a connected graph.
    
    This technique helps the LLM organize complex relationships between concepts and
    reason about interconnected information.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply graph prompting technique to the prompt."""
        context = context or {}
        node_types = context.get("node_types", ["Concepts", "Requirements", "Components", "Constraints"])
        
        graph_prefix = (
            "Approach this problem by creating a knowledge graph:\n\n"
            f"1. Identify key {', '.join(node_types)} as nodes in the graph\n"
            "2. Establish relationships between these nodes\n"
            "3. Analyze the graph to identify important patterns or insights\n"
            "4. Use these insights to develop your solution\n\n"
            "Create your graph by listing each node and its relationships to other nodes.\n\n"
        )
        
        return f"{graph_prefix}Problem:\n{prompt_content}"


class MetaPromptingTechnique(PromptTechnique):
    """
    Meta Prompting technique asks the LLM to generate an effective prompt before solving.
    
    This technique improves results by having the LLM first design an optimal prompt
    for the task, then respond to that prompt.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply meta prompting technique to the prompt."""
        context = context or {}
        objective = context.get("objective", "comprehensive, accurate, and clear")
        
        meta_prefix = (
            f"To generate a {objective} response, follow these steps:\n\n"
            "1. First, create the ideal prompt that would lead to the best possible answer for this question\n"
            "2. Then, respond to that improved prompt\n\n"
            "Make sure your improved prompt considers all relevant aspects of the question and "
            "guides your thinking toward the most effective response.\n\n"
        )
        
        return f"{meta_prefix}Original question:\n{prompt_content}"


class ActivePromptTechnique(PromptTechnique):
    """
    Active-Prompt technique iteratively refines the prompt based on feedback.
    
    This technique simulates an iterative refinement process where the LLM
    evaluates and improves its initial approach.
    """
    
    def apply(self, prompt_content: str, context: Dict[str, Any] = None) -> str:
        """Apply active prompt technique to the prompt."""
        context = context or {}
        iterations = context.get("iterations", 2)
        evaluation_criteria = context.get("evaluation_criteria", "accuracy, completeness, and clarity")
        
        active_prefix = (
            f"Approach this task through {iterations} iterations of improvement:\n\n"
            "Iteration 1:\n"
            "- Generate an initial response to the question\n"
            f"- Evaluate this response against these criteria: {evaluation_criteria}\n"
            "- Identify specific improvements needed\n\n"
            "Iteration 2:\n"
            "- Create an improved response addressing the identified issues\n"
            "- Evaluate the new response against the same criteria\n"
            "- Note any remaining improvements\n\n"
        )
        
        if iterations > 2:
            active_prefix += (
                "Iteration 3:\n"
                "- Create a final response incorporating all improvements\n"
                "- Provide a final evaluation\n\n"
            )
        
        return f"{active_prefix}Question:\n{prompt_content}"


# Register these techniques with the global library
from .library import default_library

def register_advanced_techniques():
    """Register all advanced techniques with the default library."""
    techniques = [
        TreeOfThoughtsTechnique(
            name="tree_of_thoughts",
            description="Explores multiple reasoning paths before selecting the best approach",
            template="",  # Using custom apply method
            applicability=["complex_problems", "decision_making", "creative_tasks"],
            compatibility=["role_prompting"]
        ),
        ReActTechnique(
            name="react",
            description="Alternates between reasoning and acting steps for complex tasks",
            template="",  # Using custom apply method
            applicability=["multi_step_tasks", "information_gathering", "tool_use"],
            compatibility=["chain_of_thought", "role_prompting"]
        ),
        SelfConsistencyTechnique(
            name="self_consistency",
            description="Generates multiple solutions and selects the most consistent one",
            template="",  # Using custom apply method
            applicability=["reasoning", "math", "decision_making"],
            compatibility=["chain_of_thought"]
        ),
        ReflexionTechnique(
            name="reflexion",
            description="Incorporates self-reflection to evaluate and improve responses",
            template="",  # Using custom apply method
            applicability=["all"],
            compatibility=["chain_of_thought", "few_shot"]
        ),
        GenerateKnowledgeTechnique(
            name="generate_knowledge",
            description="Explicitly generates relevant knowledge before answering",
            template="",  # Using custom apply method
            applicability=["knowledge_intensive", "research", "analysis"],
            compatibility=["chain_of_thought", "role_prompting"]
        ),
        PrefillResponseTechnique(
            name="prefill_response",
            description="Provides a partial response structure for completion",
            template="",  # Using custom apply method
            applicability=["structured_output", "reports", "analysis"],
            compatibility=["role_prompting", "xml_tagging"]
        ),
        DirectionalStimulusTechnique(
            name="directional_stimulus",
            description="Guides thinking in a specific direction with targeted prompts",
            template="",  # Using custom apply method
            applicability=["creative_tasks", "brainstorming", "perspective_taking"],
            compatibility=["role_prompting", "chain_of_thought"]
        ),
        PromptChainingTechnique(
            name="prompt_chaining",
            description="Breaks complex tasks into a sequence of simpler steps",
            template="",  # Using custom apply method
            applicability=["complex_tasks", "multi_step_processes", "software_dev"],
            compatibility=["chain_of_thought", "role_prompting"]
        ),
        GraphPromptingTechnique(
            name="graph_prompting",
            description="Represents knowledge and reasoning as a connected graph",
            template="",  # Using custom apply method
            applicability=["complex_relationships", "system_design", "analysis"],
            compatibility=["chain_of_thought"]
        ),
        MetaPromptingTechnique(
            name="meta_prompting",
            description="Asks the LLM to generate an effective prompt before solving",
            template="",  # Using custom apply method
            applicability=["all"],
            compatibility=["role_prompting", "chain_of_thought"]
        ),
        ActivePromptTechnique(
            name="active_prompt",
            description="Iteratively refines the prompt based on feedback",
            template="",  # Using custom apply method
            applicability=["complex_problems", "critical_tasks", "creative_work"],
            compatibility=["reflexion", "chain_of_thought"]
        )
    ]
    
    for technique in techniques:
        default_library.register(technique)


# Initialize the advanced techniques
register_advanced_techniques() 