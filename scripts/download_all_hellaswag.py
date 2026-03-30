import pandas as pd
import requests
import os
import shutil

def download_all_hellaswag_languages():
    print("Downloading all 20 European languages for Hellaswagx...")
    
    base_url = "https://huggingface.co/datasets/Eurolingua/hellaswagx/resolve/main/"
    
    # All 20 languages listed in the dataset repo
    languages = [
        'BG', 'CS', 'DA', 'DE', 'EL', 'ES', 'ET', 'FI', 'FR', 'HU', 
        'IT', 'LT', 'LV', 'NL', 'PL', 'PT-PT', 'RO', 'SK', 'SL', 'SV'
    ]
    splits = ['train', 'validation']
    
    # Direct the download path 1 level up into the structured data folder
    main_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "Hellaswag Dataset")
    os.makedirs(main_dir, exist_ok=True)
    
    # First, let's move the previously downloaded ones (DE, ES, FR, IT and original) into their subfolders
    print("Organizing previously downloaded files...")
    
    # Organize Original
    orig_dir = os.path.join(main_dir, "Original_EN")
    os.makedirs(orig_dir, exist_ok=True)
    for f in os.listdir(main_dir):
        if f.startswith("original_") and os.path.isfile(os.path.join(main_dir, f)):
            shutil.move(os.path.join(main_dir, f), os.path.join(orig_dir, f))
            
    # Organize existing languages
    for lang in ['DE', 'ES', 'FR', 'IT']:
        lang_dir = os.path.join(main_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        for f in os.listdir(main_dir):
            if f.startswith(f"hellaswag_{lang}_") and os.path.isfile(os.path.join(main_dir, f)):
                shutil.move(os.path.join(main_dir, f), os.path.join(lang_dir, f))
    
    # Now loop through all 20 to download the missing ones
    for lang in languages:
        lang_dir = os.path.join(main_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        for split in splits:
            filename = f"hellaswag_{lang}_{split}.jsonl"
            excel_name = f"hellaswag_{lang}_{split}.xlsx"
            
            jsonl_path = os.path.join(lang_dir, filename)
            excel_path = os.path.join(lang_dir, excel_name)
            
            # Skip if already exists
            if os.path.exists(jsonl_path) and os.path.exists(excel_path):
                print(f"Skipping {lang} {split} (Already exists)")
                continue
                
            url = base_url + filename
            print(f"Downloading {filename}...")
            
            try:
                resp = requests.get(url, allow_redirects=True)
                if resp.status_code == 200:
                    with open(jsonl_path, "wb") as f:
                        f.write(resp.content)
                    print(f"  -> Saved {filename}")
                    
                    # Convert to Excel
                    print(f"  -> Converting to {excel_name}...")
                    try:
                        df = pd.read_json(jsonl_path, lines=True)
                        df.to_excel(excel_path, index=False, engine='openpyxl')
                        print(f"  -> Saved {excel_name}")
                    except Exception as e:
                        print(f"  -> Failed to convert {filename}: {e}")
                        
                else:
                    print(f"Failed to download {filename}. HTTP Status: {resp.status_code}")
            except Exception as e:
                print(f"Download error on {filename}: {e}")

    print("\nHellaswag full 20-language download and conversion complete!")

if __name__ == "__main__":
    download_all_hellaswag_languages()
