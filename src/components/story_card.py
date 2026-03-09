
"""
Streamlit component for displaying user stories as cards
"""

import streamlit as st
import re


def parse_user_stories(llm_response: str) -> list:
    """
    Parse LLM response to extract individual stories with story points
    
    Args:
        llm_response: Raw response from LLM
        
    Returns:
        List of dicts with 'number', 'points', 'story' keys
    """
    stories = []
    
    # Split by story number pattern
    story_pattern = r'\*\*Story (\d+)\*\* \(Story Points: (\d+)\)\s*\n(.*?)(?=\*\*Story \d+\*\*|$)'
    matches = re.finditer(story_pattern, llm_response, re.DOTALL)
    
    for match in matches:
        story_num = match.group(1)
        points = match.group(2)
        story_text = match.group(3).strip()
        
        stories.append({
            'number': int(story_num),
            'points': int(points),
            'story': story_text
        })
    
    return stories


def display_story_card(story_num: int, points: int, story_text: str):
    """
    Display a single user story as a styled card
    
    Args:
        story_num: Story number (1-5)
        points: Story points (1-13)
        story_text: The user story text
    """
    # Color coding by story points
    if points <= 3:
        color = "#10b981"  # Green - easy
        label = "Low Complexity"
    elif points <= 5:
        color = "#3b82f6"  # Blue - medium
        label = "Medium Complexity"
    elif points <= 8:
        color = "#f59e0b"  # Orange - high
        label = "High Complexity"
    else:
        color = "#ef4444"  # Red - very high
        label = "Very High Complexity"
    
    st.markdown(f"""
    <div style="
        border: 1px solid #e5e7eb;
        border-left: 4px solid {color};
        padding: 16px;
        margin: 12px 0;
        border-radius: 6px;
        background-color: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="
                background: {color};
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
            ">
                {points} Story Points • {label}
            </span>
            <span style="color: #6b7280; font-size: 14px;">
                Story {story_num}
            </span>
        </div>
        <p style="
            margin: 8px 0 0 0;
            font-size: 15px;
            line-height: 1.6;
            color: #1f2937;
        ">
            {story_text}
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_all_stories(llm_response: str):
    """
    Parse and display all user stories from LLM response
    
    Args:
        llm_response: Complete response from LLM with all stories
    """
    stories = parse_user_stories(llm_response)
    
    if not stories:
        st.error("Could not parse user stories from response. Please try again.")
        st.text_area("Raw Response:", llm_response, height=200)
        return
    
    # Display summary
    total_points = sum(s['points'] for s in stories)
    avg_points = total_points / len(stories) if stories else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Stories", len(stories))
    with col2:
        st.metric("Total Story Points", total_points)
    with col3:
        st.metric("Avg Points", f"{avg_points:.1f}")
    
    st.markdown("---")
    
    # Display each story
    for story in stories:
        display_story_card(
            story_num=story['number'],
            points=story['points'],
            story_text=story['story']
        )