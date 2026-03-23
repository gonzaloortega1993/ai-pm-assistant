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
    st.markdown("**💡 Need inspiration? Copy and paste one of these:**")
    
    fitness_example = """We're building a fitness tracking mobile app that helps users log daily workouts with exercise types and duration, track nutrition and calorie intake, set fitness goals and monitor progress, connect with personal trainers for guidance, and view progress reports with achievement badges."""
    
    ecommerce_example = """We're creating an e-commerce platform for handmade crafts where artisans can set up online stores with custom branding, customers can browse by category and search products, process secure payments with multiple payment methods, track orders with shipping notifications, and leave reviews and ratings for products and sellers."""
    
    telemedicine_example = """We're developing a telemedicine platform that enables virtual consultations via video call with licensed doctors, secure medical record storage and sharing, prescription management with pharmacy integration, appointment scheduling with calendar sync, and health monitoring with wearable device integration."""
    
    # Show examples in expandable sections
    with st.expander("📱 Fitness App Example"):
        st.code(fitness_example, language=None)
        if st.button("📋 Copy to clipboard", key="copy_fitness"):
            st.info("💡 Copy the text above and paste into the description box below")
    
    with st.expander("🛒 E-commerce Example"):
        st.code(ecommerce_example, language=None)
        if st.button("📋 Copy to clipboard", key="copy_ecommerce"):
            st.info("💡 Copy the text above and paste into the description box below")
    
    with st.expander("🏥 Telemedicine Example"):
        st.code(telemedicine_example, language=None)
        if st.button("📋 Copy to clipboard", key="copy_telemedicine"):
            st.info("💡 Copy the text above and paste into the description box below")
    
    st.markdown("---")
    
    # Input text area
    project_desc = st.text_area(
        "Project Description",
        placeholder="Describe your project in detail (minimum 50 characters)...",
        height=150,
        help="Describe what you're building - the more detail, the better the stories!"
    )
    
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
        generate_button = st.button("✨ Generate User Stories", type="primary", use_container_width=True)
    
    # Generation logic
    if generate_button:
        if not project_desc or len(project_desc.strip()) < 50:
            st.error("❌ Please enter at least 50 characters describing your project")
            st.info("💡 Tip: Copy one of the examples above to get started, or write your own detailed description")
        else:
            try:
                with st.spinner("🤖 Claude is analyzing your project and generating user stories..."):
                    client = LLMClient()
                    stories_response = client.generate_user_stories(project_desc)
                    
                st.success("✅ User stories generated successfully!")
                
                st.markdown("### 📋 Generated User Stories")
                display_all_stories(stories_response)
                
                st.download_button(
                    label="📥 Download as Markdown",
                    data=stories_response,
                    file_name="user_stories.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except ValueError as ve:
                st.error(f"⚠️ Configuration Error: {str(ve)}")
                with st.expander("🔧 How to fix this", expanded=True):
                    st.markdown("""
                    **Missing API Key?**
                    
                    1. Make sure you have a `.env` file in your project root
                    2. Add this line: `ANTHROPIC_API_KEY=your-key-here`
                    3. Get your API key from: https://console.anthropic.com/
                    4. Restart the Streamlit app
                    
                    **Still having issues?**
                    - Verify your API key is valid
                    - Check you have credits in your Anthropic account
                    - Ensure `LLM_PROVIDER=claude` in .env
                    """)
                    
            except ConnectionError as ce:
                st.error("❌ Connection Error: Unable to reach Claude API")
                with st.expander("💡 Troubleshooting", expanded=True):
                    st.markdown("""
                    **Check your internet connection**
                    - Verify you're online
                    - Try visiting https://www.anthropic.com in your browser
                    
                    **If you're behind a firewall:**
                    - Claude API may be blocked
                    - Try from a different network
                    """)
                    
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                with st.expander("💡 Troubleshooting", expanded=True):
                    st.markdown("""
                    **Common issues:**
                    
                    - **Rate limit:** Wait 1-2 minutes and try again
                    - **Timeout:** Try a shorter project description
                    - **Invalid response:** Check API status at status.anthropic.com
                    
                    **Still stuck?**
                    - Copy the error message above
                    - Check Anthropic's documentation
                    - Verify all dependencies are installed
                    """)
                st.caption(f"Error details: {type(e).__name__}")

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