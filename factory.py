import os
from google import genai

# Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def run_factory(app_description):
    print(f"🚀 Starting build for: {app_description}")
    
    # We use 2.0-flash - the 1.5 versions are retired!
    model_id = "gemini-2.0-flash" 

    architect_prompt = f"Build a single-file HTML/JS app for: {app_description}. Use CDN links for Three.js. Provide ONLY code in backticks."

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=architect_prompt
        )
        # Extracting the code block
        raw_text = response.text
        code = raw_text.split("```")[1].replace("html", "").replace("javascript", "").strip() if "```" in raw_text else raw_text
        
        print("✅ Code generated successfully.")
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        code = "<html><body><h1>Build Failed</h1><p>Check logs for API errors.</p></body></html>"

    # CRITICAL: Always create the directory so the Deploy Action doesn't crash
    os.makedirs("build", exist_ok=True)
    with open("build/index.html", "w") as f:
        f.write(code)
    print("📂 File saved to build/index.html")

if __name__ == "__main__":
    description = "A 3D Blender-like editor with a cube and basic rotation controls"
    run_factory(description)
