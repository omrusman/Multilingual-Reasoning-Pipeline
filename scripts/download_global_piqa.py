import pandas as pd
from datasets import load_dataset
import os

def download_european_global_piqa():
    print("Fetching European languages for Global PIQA...")
    
    # Selected European language configs from the Global PIQA dataset
    european_configs = [
        'als_latn', 'bel_cyrl', 'bos_latn', 'bul_cyrl', 'cat_latn', 
        'ces_latn', 'deu_latn', 'ekk_latn', 'ell_grek', 'eng_latn', 
        'fao_latn', 'fin_latn', 'fra_latn_fran', 'glg_latn', 'hrv_latn', 
        'hun_latn', 'isl_latn', 'ita_latn', 'lit_latn', 'mkd_cyrl', 
        'nld_latn', 'nno_latn', 'nob_latn', 'pol_latn', 'por_latn_port', 
        'ron_latn', 'rus_cyrl', 'slk_latn', 'slv_latn', 'spa_latn_spai', 
        'srp_cyrl', 'srp_latn', 'swe_latn', 'ukr_cyrl'
    ]
    
    # Direct the download path 1 level up into the structured data folder
    main_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "Global PIQA Dataset")
    os.makedirs(main_dir, exist_ok=True)
    
    for config in european_configs:
        lang_dir = os.path.join(main_dir, config)
        os.makedirs(lang_dir, exist_ok=True)
        
        print(f"Downloading {config}...")
        try:
            # The dataset only has one split "test" for non-parallel version
            dataset = load_dataset('mrlbenchmarks/global-piqa-nonparallel', config)
            eval_split = dataset['test']
            
            # Convert directly to pandas dataframe
            df = eval_split.to_pandas()
            
            # Save format
            excel_name = f"global_piqa_{config}.xlsx"
            excel_path = os.path.join(lang_dir, excel_name)
            
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"  -> Saved {excel_name}")
            
        except Exception as e:
            print(f"  -> Failed to download/convert {config}: {e}")

    print("\nGlobal PIQA European download complete!")

if __name__ == "__main__":
    download_european_global_piqa()
