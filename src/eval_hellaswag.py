import os
import time
import pandas as pd
from config import MODELS, HELLASWAG_LANGS, MAX_SAMPLES
from llm_client import ensure_credits, evaluate_model, parse_answer
from utils import save_incremental_results, print_summary

def run_hellaswag(specific_lang=None):
    print("\n--- RUNNING HELLASWAG EVALUATION ---")
    
    langs_to_run = HELLASWAG_LANGS if specific_lang is None else {specific_lang: HELLASWAG_LANGS[specific_lang]}
    
    for lang, info in langs_to_run.items():
        print(f"\n[STARTING] 'Hellaswag - {lang}'")
        ensure_credits()
            
        filepath = os.path.join("Hellaswag Dataset", info['dir'], f"{info['prefix']}_validation.jsonl")
        
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
            
        print(f"Loading {lang} Hellaswag...")
        df = pd.read_json(filepath, lines=True).head(MAX_SAMPLES)
        
        results = []
        for model in MODELS:
            print(f"  Evaluating {model}...")
            correct = 0
            
            for _, row in df.iterrows():
                ctx = row['ctx']
                endings = row['endings']
                true_label = int(row['label'])
                
                prompt = (
                    "Choose the most logical ending for the following context. "
                    "Reply with ONLY the number corresponding to the correct ending.\n\n"
                    f"Context: {ctx}\n"
                    f"0: {endings[0]}\n"
                    f"1: {endings[1]}\n"
                    f"2: {endings[2]}\n"
                    f"3: {endings[3]}\n"
                    "Answer:"
                )
                
                response_text = evaluate_model(model, prompt)
                predicted_label = parse_answer(response_text, ["0", "1", "2", "3"])
                
                # Collect detailed row info for the Excel sheet
                results.append({
                    "Dataset": "Hellaswag", 
                    "Language": lang, 
                    "Model": model, 
                    "Context": ctx,
                    "Ending_0": endings[0],
                    "Ending_1": endings[1],
                    "Ending_2": endings[2],
                    "Ending_3": endings[3],
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
        print(f"Saved incremental results for Hellaswag {lang}.")

    print_summary("Hellaswag")
    return True
