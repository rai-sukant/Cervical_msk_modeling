# batch_dot2_Mtw


# ===============================================
# Xsens Dot (W4 + W5) → OpenSense MVN-style TXT
# BATCH VERSION
# ===============================================

import os
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R

# ------------------------------------------------
# MAIN CONVERSION FUNCTION (MODIFIED: OUTPUT PATH)
# ------------------------------------------------
def transformed_Xsens_dot_data_Realtime(filename, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    # Extract base filename
    base_name = os.path.splitext(os.path.basename(filename))[0]

    # Read CSV
    df = pd.read_csv(filename)

    # ------------------------------------------------
    # Common timing columns
    # ------------------------------------------------
    if "PacketCounter" in df.columns:
        PacketCounter = df["PacketCounter"]
    else:
        PacketCounter = pd.Series(range(len(df)))

    SampleTimeFine = df["sampleTimeFine"]

    # Empty UTC fields
    df_other = pd.DataFrame({
        'Year':[], 'Month':[], 'Day':[], 'Second':[],
        'UTC_Nano':[], 'UTC_Year':[], 'UTC_Month':[],
        'UTC_Day':[], 'UTC_Hour':[], 'UTC_Minute':[],
        'UTC_Second':[], 'UTC_Valid':[]
    })

    header_list = ["Mat[1][1]","Mat[2][1]","Mat[3][1]",
                   "Mat[1][2]","Mat[2][2]","Mat[3][2]",
                   "Mat[1][3]","Mat[2][3]","Mat[3][3]"]

    # =====================================================
    # ==================== W4 ==============================
    # =====================================================
    df_w4 = df[[col for col in df.columns if col.startswith("W4_")]]

    quat_w4 = df_w4[["W4_quat_w","W4_quat_x","W4_quat_y","W4_quat_z"]].values

    r_w4 = R.from_quat(quat_w4)
    matrix_w4 = r_w4.as_matrix().reshape(len(df_w4), 9)

    df_matrix_w4 = pd.DataFrame(matrix_w4, columns=header_list)

    Acc_w4 = df_w4[["W4_acc_x","W4_acc_y","W4_acc_z"]]
    Acc_w4.columns = ["Acc_X","Acc_Y","Acc_Z"]

    transformed_w4 = pd.concat(
        [PacketCounter, SampleTimeFine, df_other, Acc_w4, df_matrix_w4],
        axis=1
    )

    path_w4 = os.path.join(output_folder, "MT_012005D6_009-001_cerv7.txt")
    transformed_w4.to_csv(path_w4, index=False, sep="\t", float_format="%.6f")

    with open(path_w4, "r+") as f:
        content = f.read()
        f.seek(0,0)
        f.write("// Start Time: Unknown\n"
                "// Update Rate: 60.0Hz\n"
                "//Filter Profile: human (46.1)\n"
                "// Option Flags: AHS Disabled ICC Disabled\n"
                "// Firmware Version: 4.0.2\n" + content)

    # =====================================================
    # ==================== W5 ==============================
    # =====================================================
    df_w5 = df[[col for col in df.columns if col.startswith("W5_")]]

    quat_w5 = df_w5[["W5_quat_w","W5_quat_x","W5_quat_y","W5_quat_z"]].values

    r_w5 = R.from_quat(quat_w5)
    matrix_w5 = r_w5.as_matrix().reshape(len(df_w5), 9)

    df_matrix_w5 = pd.DataFrame(matrix_w5, columns=header_list)

    Acc_w5 = df_w5[["W5_acc_x","W5_acc_y","W5_acc_z"]]
    Acc_w5.columns = ["Acc_X","Acc_Y","Acc_Z"]

    transformed_w5 = pd.concat(
        [PacketCounter, SampleTimeFine, df_other, Acc_w5, df_matrix_w5],
        axis=1
    )

    path_w5 = os.path.join(output_folder, "MT_012005D6_009-001_skull.txt")
    transformed_w5.to_csv(path_w5, index=False, sep="\t", float_format="%.6f")

    with open(path_w5, "r+") as f:
        content = f.read()
        f.seek(0,0)
        f.write("// Start Time: Unknown\n"
                "// Update Rate: 60.0Hz\n"
                "//Filter Profile: human (46.1)\n"
                "// Option Flags: AHS Disabled ICC Disabled\n"
                "// Firmware Version: 4.0.2\n" + content)

    print(f"{base_name} → Done ✅")


# ------------------------------------------------
# BATCH PROCESS FUNCTION
# ------------------------------------------------
def batch_process(parent_folder):

    parent_folder = os.path.abspath(parent_folder)
    parent_name = os.path.basename(parent_folder)

    # Create processed folder
    processed_root = os.path.join(
        parent_folder,
        f"processed_{parent_name}"
    )
    os.makedirs(processed_root, exist_ok=True)

    # Loop through all CSV files
    for file in os.listdir(parent_folder):

        if not file.endswith(".csv"):
            continue

        if not file.startswith("xsens"):
            continue

        full_path = os.path.join(parent_folder, file)

        # Example: xsens_mithiran_3.csv
        parts = file.replace(".csv", "").split("_")

        if len(parts) < 3:
            print(f"Skipping malformed file: {file}")
            continue

        person = parts[1]
        trial = parts[2]

        # Create folder structure
        person_folder = os.path.join(processed_root, person)
        trial_folder = os.path.join(person_folder, f"{person}_{trial}")

        os.makedirs(trial_folder, exist_ok=True)

        print(f"\nProcessing: {file}")
        print(f"→ {trial_folder}")

        # Run conversion
        transformed_Xsens_dot_data_Realtime(full_path, trial_folder)

    print("\n🎃 Batch processing complete!")


# ------------------------------------------------
# RUN
# ------------------------------------------------

#parent_path = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\subject_data_24-3-26"
#parent_path = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\subject_data_27-3-26"

parent_path = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\subject_data_26_3-26"

batch_process(parent_path)