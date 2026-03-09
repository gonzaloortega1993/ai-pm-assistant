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
    # Example templates
    st.markdown("**Need inspiration?** Try one of these example projects:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 Fitness App", use_container_width=True):
            st.session_state.example_text = """We're building a fitness tracking mobile app that helps users:
- Log daily workouts with exercise types and duration
- Track nutrition and calorie intake
- Set fitness goals and monitor progress
- Connect with personal trainers for guidance
- View progress reports and achievement badges"""
    
    with col2:
        if st.button("🛒 E-commerce", use_container_width=True):
            st.session_state.example_text = """We're creating an e-commerce platform for handmade crafts where:
- Artisans can set up online stores with custom branding
- Customers can browse by category, search, and filter products
- Secure payment processing with multiple payment methods
- Order tracking and shipping notifications
- Review and rating system for products and sellers"""
    
    with col3:
        if st.button("🏥 Telemedicine", use_container_width=True):
            st.session_state.example_text = """We're developing a telemedicine platform that enables:
- Virtual consultations via video call with licensed doctors
- Secure medical record storage and sharing
- Prescription management and pharmacy integration
- Appointment scheduling with calendar sync
- Health monitoring with wearable device integration"""
    
    st.markdown("---")
    # Input
# Initialize session state
    if 'example_text' not in st.session_state:
        st.session_state.example_text = ""
    
    project_desc = st.text_area(
        "Project Description",
        value=st.session_state.example_text,
        placeholder="Describe your project in detail...\n\nExample: We're building a mobile app for fitness tracking that helps users log workouts, track nutrition, and connect with personal trainers.",
        height=150,
        help="Minimum 50 characters for best results"
    )
    
    # Clear example after use
    if project_desc and st.session_state.example_text:
        st.session_state.example_text = ""
    
    # Future feature notice
    with st.expander("🔮 Coming Soon: Document Upload (RAG)", expanded=False):
        st.info("""
        **Planned for Sprint 2:**
        
        Upload reference documents (PDFs, specs, requirements) and the AI will use them as context 
        to generate more specific, context-aware user stories.
        
        This feature uses Retrieval Augmented Generation (RAG) with vector embeddings.
        """)
    
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
                
                with st.expander("🔧 How to fix this"):
                    st.markdown("""
                    **Missing API Key?**
                    
                    1. Make sure you have a `.env` file in your project root
                    2. Add this line: `ANTHROPIC_API_KEY=your-key-here`
                    3. Get your API key from: https://console.anthropic.com/
                    4. Restart the Streamlit app
                    
                    **Still having issues?** Check that:
                    - Your API key is valid
                    - You have credits in your Anthropic account
                    - LLM_PROVIDER is set to 'claude' in .env
                    """)
                    
            except Exception as e:
                st.error(f"❌ Error generating stories: {str(e)}")
                
                with st.expander("💡 Troubleshooting tips"):
                    st.markdown("""
                    **Common issues:**
                    
                    - **API Error:** Check your Anthropic account has credits
                    - **Timeout:** Try a shorter project description
                    - **Rate limit:** Wait a minute and try again
                    
                    **Need help?** The error above might give more details.
                    """)
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
st.markdown("### 💡 About This App")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Built with:**
    - 🤖 Claude Sonnet 4 (AI)
    - 🎨 Streamlit (UI)
    - 🔗 LangChain (Orchestration)
    - 🐍 Python
    """)

with col2:
    st.markdown("""
    **Created by:** Gonzalo Ortega\n
    **Location:** Copenhagen, Denmark\n
    **GitHub:** [https://github.com/gonzaloortega1993/ai-pm-assistant]\n
    **Sprint:** 1 (MVP Complete)
    """)

st.caption("AI PM Assistant © 2026 | Built following Scrum methodology")