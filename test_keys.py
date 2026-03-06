from dotenv import load_dotenv
import os

load_dotenv()

print("=" * 50)
print("API KEYS VERIFICATION")
print("=" * 50)

# Claude
claude_key = os.getenv("CLAUDE_API_KEY")
if claude_key and claude_key.startswith("sk-"):
    print(f"✓ Claude: {claude_key[:25]}...")
else:
    print("✗ Claude: MISSING or INVALID")

# Pinecone
pinecone_key = os.getenv("PINECONE_API_KEY")
if pinecone_key and pinecone_key.startswith("pcsk_"):
    print(f"✓ Pinecone: {pinecone_key[:20]}...")
else:
    print("✗ Pinecone: MISSING or INVALID")

print("=" * 50)

if claude_key and pinecone_key:
    print("✅ ALL KEYS LOADED - READY TO CODE!")
else:
    print("⚠️ MISSING KEYS - Check .env file")