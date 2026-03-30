import pandas as pd
import os
import glob

def convert_excel_to_jsonl():
    print("Converting Global PIQA Excel files to JSONL...")
    
    main_dir = "Global PIQA Dataset"
    
    # Find all Excel files recursively within the directory
    search_pattern = os.path.join(main_dir, "**", "*.xlsx")
    excel_files = glob.glob(search_pattern, recursive=True)
    
    if not excel_files:
        print("No Excel files found in Global PIQA Dataset folder.")
        return
        
    for excel_path in excel_files:
        # Define the corresponding jsonl path
        jsonl_path = excel_path.replace(".xlsx", ".jsonl")
        
        # Skip if already exists
        if os.path.exists(jsonl_path):
            print(f"Skipping {os.path.basename(excel_path)} (JSONL already exists)")
            continue
            
        print(f"Converting {os.path.basename(excel_path)} to JSONL...")
        try:
            # Read the Excel file
            df = pd.read_excel(excel_path, engine='openpyxl')
            
            # Save it to JSONL format
            # orient='records' creates a list of dicts, lines=True makes it JSON Lines format
            df.to_json(jsonl_path, orient='records', lines=True, force_ascii=False)
            
            print(f"  -> Saved {os.path.basename(jsonl_path)}")
        except Exception as e:
            print(f"  -> Error converting {excel_path}: {e}")

    print("\nAll Global PIQA conversions complete!")

if __name__ == "__main__":
    convert_excel_to_jsonl()
