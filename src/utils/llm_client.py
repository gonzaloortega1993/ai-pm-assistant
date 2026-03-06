"""
LLM Client wrapper for Claude/OpenAI
Handles API calls and prompt formatting
"""

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts.user_story_prompt import get_user_story_prompt

load_dotenv()


class LLMClient:
    """
    LLM wrapper supporting Claude and OpenAI
    Switch provider via LLM_PROVIDER in .env
    """
    
    def __init__(self, model_name=None, temperature=0.7):
        """
        Initialize LLM client
        
        Args:
            model_name: Model to use (auto-detected from .env)
            temperature: 0-1, higher = more creative
        """
        provider = os.getenv("LLM_PROVIDER", "claude")
        
        if provider == "claude":
            self.provider = "claude"
            self.model_name = model_name or os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
            
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in .env file")
                
            self.llm = ChatAnthropic(
                model=self.model_name,
                temperature=temperature,
                api_key=api_key,
                max_tokens=4096
            )
            
        elif provider == "openai":
            self.provider = "openai"
            self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-4o-mini")
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in .env file")
                
            self.llm = ChatOpenAI(
                model=self.model_name,
                temperature=temperature,
                api_key=api_key,
                max_tokens=2000
            )
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    def generate_user_stories(self, project_description: str, context: str = "") -> str:
        """
        Generate 5 user stories from project description
        
        Args:
            project_description: Project description text
            context: Optional RAG context from uploaded docs
            
        Returns:
            str: Generated user stories (markdown formatted)
        """
        # Build prompt using our template
        prompt = get_user_story_prompt(project_description, context)
        
        # Call LLM
        try:
            response = self.llm.invoke(prompt)
            
            # Extract content based on provider
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")
    
    def test_connection(self):
        """Test API connection"""
        try:
            response = self.llm.invoke("Reply with 'Connected!' if you receive this.")
            
            if hasattr(response, 'content'):
                return True, response.content
            else:
                return True, str(response)
                
        except Exception as e:
            return False, str(e)


# Test when run directly
if __name__ == "__main__":
    print("=" * 60)
    print("LLM CLIENT TEST")
    print("=" * 60)
    
    print(f"\nProvider: {os.getenv('LLM_PROVIDER', 'claude')}")
    
    try:
        # Initialize client
        print("\n1. Initializing client...")
        client = LLMClient()
        print(f"   ✓ Using: {client.provider} / {client.model_name}")
        
        # Test connection
        print("\n2. Testing connection...")
        success, message = client.test_connection()
        
        if success:
            print(f"   ✓ Connected: {message}")
        else:
            print(f"   ✗ Connection failed: {message}")
            sys.exit(1)
        
        # Test user story generation
        print("\n3. Testing user story generation...")
        
        test_description = """
        We're building a fitness tracking mobile app that helps users:
        - Log daily workouts with exercise types and duration
        - Track nutrition and calorie intake
        - Set fitness goals and monitor progress
        - Connect with personal trainers for guidance
        """
        
        print("   Generating stories (this may take 10-15 seconds)...")
        stories = client.generate_user_stories(test_description)
        
        print("\n" + "=" * 60)
        print("GENERATED USER STORIES:")
        print("=" * 60)
        print(stories)
        print("=" * 60)
        
        print("\n✅ ALL TESTS PASSED!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)