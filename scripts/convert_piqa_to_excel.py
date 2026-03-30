import pandas as pd
import os

def convert_to_excel():
    print("Converting PIQA dataset to Excel format...")
    
    # Paths
    base_dir = "piqa_dataset/physicaliqa-train-dev"
    train_jsonl = os.path.join(base_dir, "train.jsonl")
    train_labels = os.path.join(base_dir, "train-labels.lst")
    
    dev_jsonl = os.path.join(base_dir, "dev.jsonl")
    dev_labels = os.path.join(base_dir, "dev-labels.lst")
    
    test_jsonl = "piqa_dataset/tests.jsonl"
    # Load Train Data
    print("Loading train data...")
    train_df = pd.read_json(train_jsonl, lines=True)
    with open(train_labels, "r") as f:
        train_df['label'] = [int(line.strip()) for line in f.readlines()]
        
    # Load Dev Data
    print("Loading dev data...")
    dev_df = pd.read_json(dev_jsonl, lines=True)
    with open(dev_labels, "r") as f:
        dev_df['label'] = [int(line.strip()) for line in f.readlines()]
    
    # Load Test Data
    print("Loading test data...")
    test_df = pd.read_json(test_jsonl, lines=True)
    # Note: tests.jsonl doesn't have a corresponding labels file in the public download
    # Save to Excel
    out_dir = "piqa_excel"
    os.makedirs(out_dir, exist_ok=True)
    
    train_out = os.path.join(out_dir, "piqa_train.xlsx")
    dev_out = os.path.join(out_dir, "piqa_dev.xlsx")
    test_out = os.path.join(out_dir, "piqa_test.xlsx")
    
    print(f"Saving train data to {train_out}...")
    train_df.to_excel(train_out, index=False, engine='openpyxl')
    
    print(f"Saving dev data to {dev_out}...")
    dev_df.to_excel(dev_out, index=False, engine='openpyxl')
    
    print(f"Saving test data to {test_out}...")
    test_df.to_excel(test_out, index=False, engine='openpyxl')
    
    print("Conversion complete!")

if __name__ == "__main__":
    convert_to_excel()
