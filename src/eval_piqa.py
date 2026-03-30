import os
import time
import pandas as pd
from config import MODELS, GLOBAL_PIQA_LANGS, MAX_SAMPLES
from llm_client import ensure_credits, evaluate_model, parse_answer
from utils import save_incremental_results, print_summary

def run_global_piqa(specific_lang=None):
    print("\n--- RUNNING GLOBAL PIQA EVALUATION ---")
    
    langs_to_run = GLOBAL_PIQA_LANGS if specific_lang is None else {specific_lang: GLOBAL_PIQA_LANGS[specific_lang]}
    
    for lang, code in langs_to_run.items():
        print(f"\n[STARTING] 'Global PIQA - {lang}'")
        ensure_credits()
            
        filepath = os.path.join("Global PIQA Dataset", code, f"global_piqa_{code}.jsonl")
        
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
            
        print(f"Loading {lang} Global PIQA...")
        df = pd.read_json(filepath, lines=True).head(MAX_SAMPLES)
        
        results = []
        for model in MODELS:
            print(f"  Evaluating {model}...")
            correct = 0
            
            for _, row in df.iterrows():
                goal = row['prompt']
                sol1 = row['solution0']
                sol2 = row['solution1']
                true_label = int(row['label']) 
                
                prompt = (
                    "Given the following goal, choose the most sensible solution. "
                    "Reply with ONLY the number corresponding to the correct solution.\n\n"
                    f"Goal: {goal}\n"
                    f"0: {sol1}\n"
                    f"1: {sol2}\n"
                    "Answer:"
                )
                
                response_text = evaluate_model(model, prompt)
                predicted_label = parse_answer(response_text, ["0", "1"])
                
                # Collect detailed row info for the Excel sheet
                results.append({
                    "Dataset": "Global PIQA", 
                    "Language": lang, 
                    "Model": model, 
                    "Context (Goal)": goal,
                    "Ending_0": sol1,
                    "Ending_1": sol2,
                    "Ending_2": "",
                    "Ending_3": "",
                    "True_Label": true_label,
                    "Predicted_Label": predicted_label,
                    "Correct": int(predicted_label == true_label)
                })
                
                if predicted_label == true_label:
                    correct += 1
                    
                time.sleep(0.5)
                
            accuracy = correct / len(df)
            print(f"    Accuracy: {accuracy:.2f}")

        # Save after every language completes
        save_incremental_results(results)
        print(f"Saved incremental results for Global PIQA {lang}.")

    print_summary("Global PIQA")
    return True
