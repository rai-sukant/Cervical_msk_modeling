# ===============================================
# Xsens Dot (W4 + W5) → OpenSense MVN-style TXT
# ===============================================

"""This script converts the .csv data (only quaternion data) from 2 
    xsens DOT sensors.
    
    Hardcoded for W4 & W5 sensors"""


import os
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
# ------------------------------------------------
# OUTPUT FOLDER
# ------------------------------------------------
path_cwd = os.getcwd()
new_file = "Transformed_XsensDot_Data_Realtime"
path_new_file = os.path.join(path_cwd, new_file)
os.makedirs(path_new_file, exist_ok=True)

# ------------------------------------------------
# MAIN CONVERSION FUNCTION
# ------------------------------------------------
def transformed_Xsens_dot_data_Realtime(filename):

    # Extract base filename (without .csv)
    base_name = os.path.splitext(os.path.basename(filename))[0]

    # Read the full CSV (both sensors together)
    df = pd.read_csv(filename)

    # ------------------------------------------------
    # Common timing columns
    # ------------------------------------------------
    if "PacketCounter" in df.columns:
        PacketCounter = df["PacketCounter"]
    else:
        PacketCounter = pd.Series(range(len(df)))

    SampleTimeFine = df["sampleTimeFine"]

    # Empty UTC fields (same structure as MVN)
    df_other = pd.DataFrame({
        'Year':[],
        'Month':[],
        'Day':[],
        'Second':[],
        'UTC_Nano':[],
        'UTC_Year':[],
        'UTC_Month':[],
        'UTC_Day':[],
        'UTC_Hour':[],
        'UTC_Minute':[],
        'UTC_Second':[],
        'UTC_Valid':[]
    })

    # Rotation matrix column names (MVN format)
    header_list = ["Mat[1][1]","Mat[2][1]","Mat[3][1]",
                   "Mat[1][2]","Mat[2][2]","Mat[3][2]",
                   "Mat[1][3]","Mat[2][3]","Mat[3][3]"]

    # =====================================================
    # =============== PROCESS SENSOR W4 ===================
    # =====================================================

    df_w4 = df[[col for col in df.columns if col.startswith("W4_")]]

    # Extract quaternion (W4)
    quat_w4 = df_w4[["W4_quat_w",
                     "W4_quat_x",
                     "W4_quat_y",
                     "W4_quat_z"]].values

    print(df_w4[df_w4[["W4_quat_w","W4_quat_x","W4_quat_y","W4_quat_z"]].isna().any(axis=1)])

    # Convert quaternion → rotation matrix
    r_w4 = R.from_quat(quat_w4)
    matrix_w4 = r_w4.as_matrix().reshape(len(df_w4), 9)

    df_matrix_w4 = pd.DataFrame(matrix_w4, columns=header_list)

    # Acceleration (rename to MVN format)
    Acc_w4 = df_w4[["W4_acc_x","W4_acc_y","W4_acc_z"]]
    Acc_w4.columns = ["Acc_X","Acc_Y","Acc_Z"]

    # Combine all columns
    transformed_w4 = pd.concat(
        [PacketCounter, SampleTimeFine, df_other, Acc_w4, df_matrix_w4],
        axis=1
    )

    
    # Save W4 file
    w4_filename = "MT_012005D6_009-001_cerv7.txt"
    path_w4 = os.path.join(path_new_file, w4_filename)

    transformed_w4.to_csv(path_w4, index=False, sep="\t", float_format="%.6f")

    # Add MVN-style header
    with open(path_w4, "r+") as f:
        content = f.read()
        f.seek(0,0)
        f.write("// Start Time: Unknown\n"
                "// Update Rate: 60.0Hz\n"
                "//Filter Profile: human (46.1)\n"
                "// Option Flags: AHS Disabled ICC Disabled\n"
                "// Firmware Version: 4.0.2\n" + content)

    print(w4_filename, "Done ✅")

    # =====================================================
    # =============== PROCESS SENSOR W5 ===================
    # =====================================================

    df_w5 = df[[col for col in df.columns if col.startswith("W5_")]]

    # Extract quaternion (W5)
    quat_w5 = df_w5[["W5_quat_w",
                     "W5_quat_x",
                     "W5_quat_y",
                     "W5_quat_z"]].values

    # Convert quaternion → rotation matrix
    r_w5 = R.from_quat(quat_w5)
    matrix_w5 = r_w5.as_matrix().reshape(len(df_w5), 9)

    df_matrix_w5 = pd.DataFrame(matrix_w5, columns=header_list)

    # Acceleration (rename to MVN format)
    Acc_w5 = df_w5[["W5_acc_x","W5_acc_y","W5_acc_z"]]
    Acc_w5.columns = ["Acc_X","Acc_Y","Acc_Z"]

    # Combine all columns
    transformed_w5 = pd.concat(
        [PacketCounter, SampleTimeFine, df_other, Acc_w5, df_matrix_w5],
        axis=1
    )

    # Save W5 file
    w5_filename = "MT_012005D6_009-001_skull.txt"
    path_w5 = os.path.join(path_new_file, w5_filename)

    transformed_w5.to_csv(path_w5, index=False, sep="\t", float_format="%.6f")

    # Add MVN-style header
    with open(path_w5, "r+") as f:
        content = f.read()
        f.seek(0,0)
        f.write("// Start Time: Unknown\n"
                "// Update Rate: 60.0Hz\n"
                "//Filter Profile: human (46.1)\n"
                "// Option Flags: AHS Disabled ICC Disabled\n"
                "// Firmware Version: 4.0.2\n" + content)
        

    print(w5_filename, "Done ✅")

# ------------------------------------------------
# RUN THE CONVERSION ON YOUR FILE
# ------------------------------------------------

# ------------------------ NEW DATA -------------------------------------

#"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\_subject_data_17-3-26\xsens_Ruchir_static.csv"

transformed_Xsens_dot_data_Realtime(input_file)
print("🎃 All sensors converted (W4 + W5)!")

