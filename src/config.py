import os

# Set your API Key here or as an environment variable
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "ENTER YOUR API KEY HERE")

MODELS = [
    # Top Open Source (7B - 14B Range)
    "meta-llama/llama-3.1-8b-instruct",
    "google/gemma-3-12b-it",
    "mistralai/mistral-7b-instruct-v0.1",
    "qwen/qwen-2.5-7b-instruct",
    
    # State-of-the-Art Commercial Models (Requires OpenRouter Credits)
    "openai/gpt-4o",
    "anthropic/claude-opus-4.6",
    "qwen/qwen-max",
    
    # Replacement for unstable 3.1 preview
    "google/gemini-2.5-flash"
]

# Map languages to their Hellaswag directories and identifiers
HELLASWAG_LANGS = {
    "English": {"dir": "Original_EN", "prefix": "original_hellaswag"},
    "German": {"dir": "DE", "prefix": "hellaswag_DE"},
    "French": {"dir": "FR", "prefix": "hellaswag_FR"},
    "Polish": {"dir": "PL", "prefix": "hellaswag_PL"},
    "Romanian": {"dir": "RO", "prefix": "hellaswag_RO"},
    "Hungarian": {"dir": "HU", "prefix": "hellaswag_HU"}
}

# Map languages to their Global PIQA identifiers
GLOBAL_PIQA_LANGS = {
    "English": "eng_latn",
    "German": "deu_latn",
    "French": "fra_latn_fran",
    "Polish": "pol_latn",
    "Romanian": "ron_latn",
    "Hungarian": "hun_latn"
}

# Evaluates exactly 100 samples per dataset
MAX_SAMPLES = 100
