from config import HELLASWAG_LANGS, GLOBAL_PIQA_LANGS, MAX_SAMPLES
from eval_hellaswag import run_hellaswag
from eval_piqa import run_global_piqa

def main():
    print("Starting LLM Multi-Lingual Evaluation via OpenRouter...")
    print(f"Configured to process {MAX_SAMPLES} samples per language dataset.")
    
    options = []
    for lang in HELLASWAG_LANGS.keys():
        options.append(("Hellaswag", lang))
    for lang in GLOBAL_PIQA_LANGS.keys():
        options.append(("Global PIQA", lang))
        
    while True:
        print("\n" + "="*40)
        print("EVALUATION MENU")
        print("="*40)
        for i, (ds, lang) in enumerate(options, 1):
            print(f"{i:2d}. {ds.ljust(15)} - {lang}")
        
        run_all_idx = len(options) + 1
        print("-" * 40)
        print(f"{run_all_idx:2d}. Run ALL Missing/Remaining Datasets")
        print(" q. Quit")
        print("="*40)
        
        choice = input(f"Select an option (1-{run_all_idx}, or q): ").strip().lower()
        
        if choice == 'q':
            print("\nScript execution finished. All saved progress is in 'evaluation_results.xlsx'.")
            break
            
        try:
            choice_idx = int(choice)
            if 1 <= choice_idx <= len(options):
                ds, lang = options[choice_idx - 1]
                if ds == "Hellaswag":
                    run_hellaswag(specific_lang=lang)
                else:
                    run_global_piqa(specific_lang=lang)
            elif choice_idx == run_all_idx:
                run_hellaswag()
                run_global_piqa()
            else:
                print("Invalid option number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

if __name__ == "__main__":
    main()
