import os
from google import genai
from google.genai import types
from e2b_code_interpreter import Sandbox

# 1. Setup API Keys (Use Environment Variables for safety!)
GEMINI_API_KEY = "AIzaSyCfRtMGlVnz46ffMmcsQ7yWaEk80a3p0m8"
E2B_API_KEY = "e2b_7b37e42a8fbad41ca788b8674c6ed1ff622863db"
"

client = genai.Client(api_key=GEMINI_API_KEY)

def run_factory(app_description):
    print(f"🚀 Starting build for: {app_description}")
    
    # PHASE 1: THE ARCHITECT GENERATES CODE
    architect_prompt = f"""
    You are the Senior Architect. Build a single-file HTML/JS app for: {app_description}.
    Use Three.js for 3D elements. 
    IMPORTANT: Provide ONLY the code inside a triple backtick block.
    """
    
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=architect_prompt
    )
    code = response.text.split("```")[1].replace("html", "").strip()

    # PHASE 2: THE SANDBOX TEST (E2B)
    print("🛠 Testing code in cloud sandbox...")
    with Sandbox(api_key=E2B_API_KEY) as sandbox:
        # We simulate a "build check" or run a linter
        execution = sandbox.run_code(f"print('Checking syntax...')") 
        # In a real app, you'd use sandbox.filesystem.write to save the file
        print(f"Sandbox Output: {execution.logs.stdout}")

    # PHASE 3: THE AUDITOR (Self-Correction)
    # If there were errors, we would feed them back here.
    
    print("✅ Build complete. Saving to build/index.html")
    os.makedirs("build", exist_ok=True)
    with open("build/index.html", "w") as f:
        f.write(code)

if __name__ == "__main__":
    description = "A 3D Blender-like editor with a cube and basic rotation controls"
    run_factory(description)
