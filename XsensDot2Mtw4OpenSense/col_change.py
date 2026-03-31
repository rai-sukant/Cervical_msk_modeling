import os
import pandas as pd

# Your device mapping
DEVICE_NAME_MAP = {
    "D4:22:CD:00:A9:12": "W4",
    "D4:22:CD:00:A1:93": "W5",
}

def rename_columns(columns):
    new_cols = []
    
    for col in columns:
        new_col = col
        
        for device_id, name in DEVICE_NAME_MAP.items():
            if device_id in col:
                new_col = col.replace(device_id, name)
                break  # Stop after first match
        
        new_cols.append(new_col)
    
    return new_cols


def process_csv_file(file_path):
    try:
        # Read CSV
        df = pd.read_csv(file_path)

        # Rename columns
        df.columns = rename_columns(df.columns)

        # Overwrite same file
        df.to_csv(file_path, index=False)

        print(f"✔ Processed: {file_path}")

    except Exception as e:
        print(f"✖ Error processing {file_path}: {e}")


def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            process_csv_file(file_path)


if __name__ == "__main__":
    #folder_path = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\subject_data_24-3-26"
    #folder_path = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\subject_data_26_3-26"
    
    folder_path = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\subject_data_27-3-26"
    process_folder(folder_path)