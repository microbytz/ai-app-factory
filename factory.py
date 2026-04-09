import os
from google import genai
from google.genai import types

# This grabs the keys safely from GitHub's memory
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def run_factory(app_description):
    print(f"🚀 Starting build for: {app_description}")
    
    architect_prompt = f"""
    You are a Senior Web Developer. Build a single-file HTML/JS app for: {app_description}.
    Use CDN links for Three.js. 
    IMPORTANT: Provide ONLY the code inside a triple backtick block.
    """

    # We use the direct generate_content method which bypasses the 'models' sub-client
    try:
        response = client.generate_content(
            model="gemini-1.5-flash",
            contents=architect_prompt
        )
        raw_text = response.text
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return

    # Extract code between backticks
    if "```" in raw_text:
        parts = raw_text.split("```")
        code = parts[1]
        # Clean up language labels
        for label in ["html", "javascript", "js"]:
            if code.lower().startswith(label):
                code = code[len(label):]
    else:
        code = raw_text

    print("✅ Code generated. Saving to build/index.html")
    os.makedirs("build", exist_ok=True)
    with open("build/index.html", "w") as f:
        f.write(code.strip())
