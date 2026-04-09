import os
from google import genai

# Safety Check: Ensure keys exist
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ CRITICAL: GEMINI_API_KEY is missing from environment!")

client = genai.Client(api_key=GEMINI_API_KEY)

def run_factory(app_description):
    print(f"🚀 Starting build for: {app_description}")
    
    # Using the most current stable model for April 2026
    model_id = "gemini-2.0-flash" 

    prompt = f"Write a single-file HTML/JS app: {app_description}. Use CDN for Three.js. Return ONLY the code."

    try:
        response = client.models.generate_content(model=model_id, contents=prompt)
        raw_text = response.text
        
        # DEBUG: Print the first 100 characters so we can see it in GitHub logs
        print(f"📡 AI Response Preview: {raw_text[:100]}...")

        if "```" in raw_text:
            code = raw_text.split("```")[1]
            for label in ["html", "javascript", "js", "web"]:
                if code.lower().startswith(label):
                    code = code[len(label):]
        else:
            code = raw_text
            
        final_code = code.strip()
        
        # If the AI returned nothing, trigger the safety catch
        if len(final_code) < 10:
            raise ValueError("AI returned empty or too-short code.")

        print("✅ Success: Code is valid.")
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        final_code = f"<html><body><h1>Build Failed</h1><p>Error: {e}</p></body></html>"

    os.makedirs("build", exist_ok=True)
    with open("build/index.html", "w") as f:
        f.write(final_code)
    print("📂 File saved to build/index.html")

if __name__ == "__main__":
    description = "A 3D Blender-like editor with a cube and basic rotation controls"
    run_factory(description)
