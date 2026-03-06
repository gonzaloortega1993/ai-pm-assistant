import streamlit as st
from dotenv import load_dotenv
import os

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
    st.markdown("Generate user stories from your project description using AI + RAG")
    
    # Input
    project_desc = st.text_area(
        "Project Description",
        placeholder="Describe your project in detail...\n\nExample: We're building a mobile app for fitness tracking that helps users log workouts, track nutrition, and connect with personal trainers.",
        height=150,
        help="Min 50 characters for best results"
    )
    
    # Optional: Document upload (coming soon)
    with st.expander("📎 Upload Reference Documents (Optional - Coming Soon)"):
        st.info("Feature in development: Upload PDFs/docs for context-aware story generation")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Generate User Stories", type="primary"):
            if project_desc and len(project_desc) >= 50:
                with st.spinner("🤖 AI is generating user stories..."):
                    # Placeholder - will implement in Sprint 1
                    import time
                    time.sleep(2)
                    
                    st.success("✅ User stories generated!")
                    
                    # Mock output
                    st.markdown("### Generated User Stories:")
                    for i in range(1, 6):
                        with st.container():
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                                <span style="background: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">
                                    {i*2} Story Points
                                </span>
                                <p style="margin-top: 10px; font-size: 16px;">
                                    <strong>Story {i}:</strong> As a [user], I want to [feature], so that [benefit]
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.info("🚧 This is a demo. Real AI generation coming in Sprint 1!")
            else:
                st.error("❌ Please enter at least 50 characters")

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