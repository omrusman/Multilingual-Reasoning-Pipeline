import time
import requests
from openai import OpenAI
from config import OPENROUTER_API_KEY

# Initialize the OpenAI Client pointing to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def evaluate_model(model_name, prompt, max_retries=10):
    """Sends a prompt to OpenRouter and returns the text response with retry logic for rate limits."""
    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0, # Greedy decoding for reproducible eval
                max_tokens=5, # We only want a single number (0, 1, 2, or 3)
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "Rate limit" in error_str:
                sleep_time = min(15, 2 * (retries + 1))
                print(f"      [Rate limited] Waiting {sleep_time} seconds before retrying {model_name}...")
                time.sleep(sleep_time)
                retries += 1
            elif "402" in error_str or "insufficient_quota" in error_str.lower() or "credit" in error_str.lower():
                print(f"\n      [CRITICAL ERROR] Out of credits during evaluation of {model_name}!")
                while not check_credit_balance():
                    print("      -> Execution PAUSED mid-loop. Please add more credits to OpenRouter to resume.")
                    input("      -> Press ENTER *after* you have purchased more credits... ")
                print("      -> Credits detected! Resuming evaluation...")
                # We do not increment retries here, we just continue the loop to try the exact same question again
                continue
            else:
                print(f"API Error for model {model_name}: {e}")
                return "-1"
                
    print(f"      -> Max retries exceeded for {model_name}.")
    return "-1"

def parse_answer(response_text, valid_options):
    """Fuzzy extracts the predicted answer index from the LLM output."""
    if not response_text:
        return -1
    for char in response_text:
        if char in valid_options:
            return int(char)
    return -1

def check_credit_balance():
    """Checks OpenRouter API for remaining credits. Returns True if > 0, False if $0 or error."""
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
        )
        if response.status_code == 200:
            data = response.json().get('data', {})
            limit = data.get('limit')
            usage = data.get('usage')
            if limit is not None and usage is not None:
                remaining = limit - usage
                if remaining <= 0.01: # Buffer for inflight requests
                    print(f"\n[CRITICAL ERROR] You are OUT OF CREDITS! (${usage:.4f} / ${limit:.4f})")
                    return False
                print(f"  (Credits remaining: ${remaining:.4f})")
                return True
        return True # Default true if unknown
    except Exception:
        return True # Default true if network fails silently

def ensure_credits():
    """Forces a blocking credit check loop until OpenRouter funds are confirmed."""
    has_credits = check_credit_balance()
    while not has_credits:
        print("  -> Execution PAUSED. Please add more credits to OpenRouter.")
        input("  -> Press ENTER *after* you have purchased more credits to check again... ")
        has_credits = check_credit_balance()
    return True
