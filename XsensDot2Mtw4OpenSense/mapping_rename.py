import os

# Target directory
folder_path = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\Transformed_XsensDot_Data_RealTime"

# Target filenames
w4_name = "MT_012005D6_009-001_cerv7.txt"
w5_name = "MT_012005D6_009-001_skull.txt"

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        old_path = os.path.join(folder_path, filename)

        if "W4" in filename:
            new_path = os.path.join(folder_path, w4_name)
            print(f"Renaming {filename} → {w4_name}")
            os.rename(old_path, new_path)

        elif "W5" in filename:
            new_path = os.path.join(folder_path, w5_name)
            print(f"Renaming {filename} → {w5_name}")
            os.rename(old_path, new_path)

            