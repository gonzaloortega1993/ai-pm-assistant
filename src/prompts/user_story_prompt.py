"""
Prompts for user story generation
"""

USER_STORY_PROMPT = """You are an expert Product Manager with 10+ years of experience writing user stories.

Given a project description, generate exactly 5 user stories that follow best practices.

Project Description:
{project_description}

{context_section}

For each user story:
1. Follow the format: "As a [specific role], I want [specific feature], so that [specific benefit]"
2. Be specific and actionable
3. Focus on user value, not technical implementation
4. Estimate story points using Fibonacci scale (1, 2, 3, 5, 8, 13)
5. Consider complexity, uncertainty, and effort

Format each story EXACTLY as:
**Story [number]** (Story Points: [X])
As a [role], I want [feature], so that [benefit]

Generate exactly 5 user stories now:"""


def get_user_story_prompt(project_description: str, context: str = "") -> str:
    """
    Build the complete user story generation prompt
    
    Args:
        project_description: The project description from user
        context: Optional RAG context from uploaded documents
        
    Returns:
        Complete formatted prompt ready for LLM
    """
    context_section = ""
    if context:
        context_section = f"\nReference Context (use this to make stories more specific):\n{context}\n"
    
    return USER_STORY_PROMPT.format(
        project_description=project_description,
        context_section=context_section
    )