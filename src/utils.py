import os
import pandas as pd

def save_incremental_results(new_results, filename="evaluation_results.xlsx"):
    """Appends new results to an existing Excel file without overwriting."""
    if not new_results:
        return
        
    df_new = pd.DataFrame(new_results)
    
    if os.path.exists(filename):
        df_existing = pd.read_excel(filename, engine='openpyxl')
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
        
    while True:
        try:
            df_combined.to_excel(filename, index=False, engine='openpyxl')
            break
        except PermissionError:
            print(f"\n[ERROR] Cannot save to '{filename}'. Is it currently open in Excel?")
            input("Please close the Excel file and press ENTER to try saving again...")

def print_summary(dataset_name, filename="evaluation_results.xlsx"):
    """Reads the Excel file and prints an accuracy summary grouped by language and model."""
    if not os.path.exists(filename):
        return
    print(f"\n=== {dataset_name.upper()} OVERALL SUMMARY ===")
    try:
        df = pd.read_excel(filename, engine='openpyxl')
        df_ds = df[df['Dataset'] == dataset_name]
        if not df_ds.empty:
            summary = df_ds.groupby(['Language', 'Model'])['Correct'].mean().reset_index()
            summary.rename(columns={'Correct': 'Accuracy'}, inplace=True)
            summary['Accuracy'] = (summary['Accuracy'] * 100).map("{:.2f}%".format)
            print(summary.to_string(index=False))
            print("\n")
    except Exception as e:
        print(f"Failed to load summary: {e}")
