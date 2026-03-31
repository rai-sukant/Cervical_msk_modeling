
"""
The purpose of this code is to convert Xsens Dot data into Xsens MVN data, 
and then into OpenSim readable data for human modeling Xsens MVN output data includes:
header timestamp acceleration data rotation matrix and UT Time Xsens Dot outputs only
the quaternion of the free acceleration of the header or euler Angle. Therefore, it is
necessary to convert the quaternion in Xsens Dot to the rotation matrix, and convert the 
header of the acceleration data to supplement UT Time and other information.
Xsens will be shown below Dot and Xsens MVN data and differences, and finally the 
corresponding transformation
"""


"""

The purpose of this script is to convert the xsens dot exported .csv file to opensense friendly .txt file format.  

"""



# ===============================================
# Xsens Dot (W4 + W5) → OpenSense MVN-style TXT
# ===============================================

"""This script converts the .csv data (only quaternion data) from 2 
    xsens DOT sensors.
    
    Hardcoded for W4 & W5 sensors"""

"""
Xsens Dot CSV → OpenSense MVN-style TXT converter
Supports multiple sensors automatically (W1, W2, W3, W4, W5, etc.)

Each sensor gets its own MVN-compatible TXT file.
"""

import os
import pandas as pd
from scipy.spatial.transform import Rotation as R

# ------------------------------------------------
# OUTPUT FOLDER
# ------------------------------------------------
path_cwd = os.getcwd()
output_folder = "Transformed_XsensDot_Data_Realtime"
path_new_file = os.path.join(path_cwd, output_folder)
os.makedirs(path_new_file, exist_ok=True)

# ------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------
def transformed_Xsens_dot_data_Realtime(filename):

    print("\nReading file:", filename)

    base_name = os.path.splitext(os.path.basename(filename))[0]

    df = pd.read_csv(filename)

    total_rows = len(df)

    print(f"Total rows: {total_rows}")

    # ------------------------------------------------
    # Detect sensors automatically
    # ------------------------------------------------
    sensor_prefixes = sorted(
        set(col.split("_")[0] for col in df.columns if "_quat_" in col)
    )

    print("Detected sensors:", sensor_prefixes)

    # ------------------------------------------------
    # Common columns
    # ------------------------------------------------
    if "PacketCounter" in df.columns:
        PacketCounter = df["PacketCounter"]
    else:
        PacketCounter = pd.Series(range(total_rows))

    SampleTimeFine = df["sampleTimeFine"]

    # Empty UTC structure
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

    # Rotation matrix headers
    header_list = [
        "Mat[1][1]","Mat[2][1]","Mat[3][1]",
        "Mat[1][2]","Mat[2][2]","Mat[3][2]",
        "Mat[1][3]","Mat[2][3]","Mat[3][3]"
    ]

    # ------------------------------------------------
    # Process each sensor dynamically
    # ------------------------------------------------
    for sensor in sensor_prefixes:

        print(f"\nProcessing sensor: {sensor}")

        acc_cols = [f"{sensor}_acc_x",
                    f"{sensor}_acc_y",
                    f"{sensor}_acc_z"]

        quat_cols = [f"{sensor}_quat_w",
                     f"{sensor}_quat_x",
                     f"{sensor}_quat_y",
                     f"{sensor}_quat_z"]

        # Check columns exist
        if not all(col in df.columns for col in quat_cols):
            print(f"Skipping {sensor} (missing quaternion data)")
            continue

        # ------------------------------------------------
        # Quaternion → Rotation Matrix
        # ------------------------------------------------
        quat = df[quat_cols].values

        print(f"Converting {len(quat)} quaternions...")

        rotation = R.from_quat(quat)

        matrix = rotation.as_matrix().reshape(total_rows, 9)

        df_matrix = pd.DataFrame(matrix, columns=header_list)

        # ------------------------------------------------
        # Acceleration
        # ------------------------------------------------
        Acc = df[acc_cols].copy()
        Acc.columns = ["Acc_X","Acc_Y","Acc_Z"]

        # ------------------------------------------------
        # Combine all
        # ------------------------------------------------
        transformed_df = pd.concat(
            [PacketCounter,
             SampleTimeFine,
             df_other,
             Acc,
             df_matrix],
            axis=1
        )

        # ------------------------------------------------
        # Save file
        # ------------------------------------------------
        output_filename = f"XSDot_{sensor}_{base_name}.txt"

        output_path = os.path.join(path_new_file, output_filename)

        transformed_df.to_csv(
            output_path,
            index=False,
            sep="\t",
            float_format="%.6f"
        )

        # Add MVN header
        with open(output_path, "r+") as f:

            content = f.read()

            f.seek(0,0)

            f.write(
                "// Start Time: Unknown\n"
                "// Update Rate: 20.0Hz\n"
                "// Filter Profile: human (46.1)\n"
                "// Option Flags: AHS Disabled ICC Disabled\n"
                "// Firmware Version: 4.0.2\n"
                + content
            )

        print(f"Saved: {output_filename}")

    print("\nAll sensors converted successfully.")

# ------------------------------------------------
# RUN
# ------------------------------------------------

""" Why time so short ? only 6 seconds  """

#Dynamic 
input_file = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\Original_XsensDot_Data_Realtime\5_sec_pause_15_sec_walk.csv"

#Static 
#input_file = r"E:\local_git\Cervical_msk_modeling\XsensDot2Mtw4OpenSense\Original_XsensDot_Data_Realtime\15_sec_pause.csv"


transformed_Xsens_dot_data_Realtime(input_file)



""" !!!!!!!!!!!!!!Make a separate python script that maps the sensors to their name needed for opensim !!!!!!!!!!!!!!"""