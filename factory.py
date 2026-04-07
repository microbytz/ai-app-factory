import os
from google import genai
from google.genai import types

# This grabs the keys safely from GitHub's memory
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def run_factory(app_description):
    print(f"🚀 Starting build for: {app_description}")
    
    # Ensure the model name is exactly this
    model_id = "gemini-1.5-flash" 
    
    architect_prompt = f"""
    You are a Senior Web Developer. Build a single-file HTML/JS app for: {app_description}.
    Use CDN links for Three.js. 
    IMPORTANT: Provide ONLY the code inside a triple backtick block.
    """
    
    response = client.models.generate_content(
        model=model_id,
        contents=architect_prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        )
    )
    
    # Extract code between backticks
    raw_text = response.text
    if "```" in raw_text:
        code = raw_text.split("```")[1]
        if code.startswith("html"): code = code[4:]
        if code.startswith("javascript"): code = code[10:]
    else:
        code = raw_text

    print("✅ Code generated. Saving to build/index.html")
    os.makedirs("build", exist_ok=True)
    with open("build/index.html", "w") as f:
        f.write(code.strip())

if __name__ == "__main__":
    # YOU CAN CHANGE THIS LINE ANYTIME TO BUILD SOMETHING ELSE
    description = "A 3D Blender-like editor with a cube and basic rotation controls"
    run_factory(description)
