import streamlit as st
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient
from components.story_card import display_all_stories

# Load environment variables
load_dotenv()

# Verify API keys loaded (for debugging)
if not os.getenv("ANTHROPIC_API_KEY"):
    st.warning("⚠️ Claude API key not found. Add ANTHROPIC_API_KEY to .env file when console is available.")

# Page config
st.set_page_config(
    page_title="AI PM Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        max-width: 1200px;
    }
    h1 {
        color: #007bff;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 AI PM Assistant")
st.markdown("**Automate your PM workflows with AI**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    feature = st.radio(
        "Select Feature:",
        [
            "📝 User Story Generator",
            "⏱️ Time Estimator",
            "📄 PRD Generator",
            "📋 Meeting Summarizer"
        ]
    )
    
    st.markdown("---")
    st.markdown("### 📊 Project Status")
    st.progress(0.15)
    st.caption("Sprint 0: Setup Complete ✅")
    st.caption("Sprint 1: In Progress 🚧")
    
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[GitHub](https://github.com/YOUR-USERNAME/ai-pm-assistant)")
    st.markdown("[Documentation](https://drive.google.com)")

# Main content
if feature == "📝 User Story Generator":


    st.header("📝 User Story Generator")
    st.markdown("Generate user stories from your project description using AI")
    
    # Input
    project_desc = st.text_area(
        "Project Description",
        placeholder="Describe your project in detail...\n\nExample: We're building a mobile app for fitness tracking that helps users log workouts, track nutrition, and connect with personal trainers.",
        height=150,
        help="Minimum 50 characters for best results"
    )
    
    # Optional: Document upload (coming soon)
    with st.expander("📎 Upload Reference Documents (Coming in Sprint 2)"):
        st.info("RAG feature will be added in Sprint 2 to use uploaded docs for context-aware generation")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("✨ Generate User Stories", type="primary")
    
    # Generation logic
    if generate_button:
        if not project_desc or len(project_desc) < 50:
            st.error("❌ Please enter at least 50 characters describing your project")
        else:
            try:
                # Initialize LLM client
                with st.spinner("🤖 Claude is analyzing your project and generating user stories..."):
                    client = LLMClient()
                    
                    # Generate stories
                    stories_response = client.generate_user_stories(project_desc)
                    
                st.success("✅ User stories generated successfully!")
                
                # Display stories using story cards
                st.markdown("### 📋 Generated User Stories")
                display_all_stories(stories_response)
                
                # Download button
                st.download_button(
                    label="📥 Download as Markdown",
                    data=stories_response,
                    file_name="user_stories.md",
                    mime="text/markdown"
                )
                
            except ValueError as e:
                st.error(f"⚠️ Configuration Error: {str(e)}")
                st.info("💡 Make sure your ANTHROPIC_API_KEY is set in the .env file")
                
            except Exception as e:
                st.error(f"❌ Error generating stories: {str(e)}")
                st.info("Please try again or check your API configuration")


elif feature == "⏱️ Time Estimator":
    st.header("⏱️ Time Estimator")
    st.markdown("Estimate project timeline using ML")
    
    st.info("🚧 **Coming in Sprint 2**\n\nThis feature will predict project duration based on complexity and features.")
    
    # Preview UI
    col1, col2 = st.columns(2)
    with col1:
        st.slider("Number of Features", 1, 50, 10, disabled=True)
    with col2:
        st.select_slider("Complexity", ["Low", "Medium", "High"], disabled=True)

elif feature == "📄 PRD Generator":
    st.header("📄 PRD Generator")
    st.markdown("Auto-generate Product Requirements Document")
    
    st.info("🚧 **Coming in Sprint 2**\n\nGenerate complete PRD templates from project descriptions.")
    
    st.text_area("Project Description", disabled=True, height=150)
    st.button("Generate PRD", disabled=True)

else:  # Meeting Summarizer
    st.header("📋 Meeting Summarizer")
    st.markdown("Extract action items and decisions from meeting notes")
    
    st.info("🚧 **Coming in Sprint 2**\n\nPaste meeting transcript to get summary + action items.")
    
    st.text_area("Meeting Transcript", disabled=True, height=200)
    st.button("Summarize Meeting", disabled=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🛠️ Built with Streamlit + LangChain + Claude")
with col2:
    st.caption("📍 Copenhagen, Denmark")
with col3:
    st.caption("© 2026 AI PM Assistant")