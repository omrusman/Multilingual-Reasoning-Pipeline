import os
import requests
from openai import OpenAI

def test_openrouter():
    # 1. Get the API Key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY environment variable is not set!")
        print("   Run: $env:OPENROUTER_API_KEY='your-key-here' in PowerShell first.")
        return

    print("[SUCCESS] API Key found in environment variables.")

    # 2. Check Credit Balance
    print("\nChecking your OpenRouter credit balance...")
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            limit = data.get('limit')
            usage = data.get('usage')
            is_free_tier = data.get('is_free_tier')
            
            if limit is not None and usage is not None:
                remaining = limit - usage
                print(f"[SUCCESS] Credits checked successfully!")
                print(f"   Usage: ${usage:.4f} / ${limit:.4f}")
                print(f"   Remaining Limit: ${remaining:.4f}")
                if is_free_tier:
                    print("   [WARNING] This key is currently marked as a FREE TIER key!")
                    print("   You will still hit strict rate limits and cannot access paid models.")
            else:
                 print("[SUCCESS] Check successful, but specific credit limit data was not returned.")
        else:
             print(f"[ERROR] Failed to fetch credits. Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] Network error while checking credits: {e}")

    # 3. Test a quick, cheap API call on ALL models
    print("\nTesting API response across all configured models...")
    from config import MODELS
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        success_count = 0
        for model in MODELS:
            print(f"  -> Testing {model}...", end=" ")
            try:
                test_response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Reply exactly with the word 'PONG'."}],
                    max_tokens=10
                )
                content = test_response.choices[0].message.content
                reply = content.strip() if content else "[Safety Refusal/Empty]"
                print(f"[SUCCESS] Pass! (Replied: '{reply}')")
                success_count += 1
            except Exception as e:
                print(f"[ERROR] Failed! Error: {e}")
                
        print(f"\n[DONE] Test complete! {success_count}/{len(MODELS)} models are fully working and ready to evaluate.")
        
    except Exception as e:
        print(f"[ERROR] API Client failed to initialize or experienced a fatal error: {e}")

if __name__ == "__main__":
    test_openrouter()
