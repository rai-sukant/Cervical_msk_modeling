# OpenSense–Hyoid IMU Pipeline (C7 + Skull)

This repository contains a set of MATLAB scripts and OpenSim/OpenSense setup files that were originally designed for the **Rajagopal full-body model**, and have been modified to work with a **Hyoid–Cervical model**. The current workflow places IMUs on the **Cervical 7 (C7)** and **Skull** geometry bodies in OpenSim and runs an OpenSense-based orientation tracking / inverse kinematics pipeline.

This codebase is functional for running calibration, IMU placement, and orientation tracking with the Hyoid model, but **the mapping between the IMU sensor frame and the OpenSim anatomical frame — and the definition of the “proper angles” — still needs to be finalized.**

---

## 📁 Repository Contents & Script Functions

### **1) `IMUDataConversion.m` — IMU Preprocessing**

**Purpose:**
Converts raw Xsens (or similar) IMU data into a format compatible with OpenSense.

**What it does:**

* Reads raw IMU CSV / TXT data.
* Extracts:

  * Orientation (quaternions or Euler angles)
  * Accelerometer data
  * Gyroscope data
* Reformats and resamples the data (if needed) to match OpenSim/OpenSense time structure.
* Outputs a standardized IMU data file that can be consumed by OpenSense.

**Role in the pipeline:**
This is the **entry point** of the workflow — all IMU data must pass through this conversion before being used in OpenSim.

---

### **2) `myIMUPlacer_Setup.xml` — Sensor Placement Definition**

**Purpose:**
Defines where and how the virtual IMUs are attached to the OpenSim model.

**What it does:**

* Specifies two IMU placement locations:

  * **Cervical 7 (C7)**
  * **Skull**
* Defines the parent bodies in the Hyoid model to which the sensors are rigidly attached.
* Contains initial orientation assumptions for each sensor relative to the body segment.

**Role in the pipeline:**
This file tells OpenSense **“where the sensors live” on the model.**

---

### **3) `myIMUMappings.xml` — IMU-to-Body Mapping**

**Purpose:**
Maps each physical (or virtual) IMU to a specific body segment in OpenSim.

**What it does:**

* Links:

  * IMU #1 → Cervical 7 body
  * IMU #2 → Skull body
* Ensures that the orientation data from each sensor is applied to the correct anatomical segment.

**Role in the pipeline:**
Acts as the bridge between sensor data and the biomechanical model.

---

### **4) `myIMUIK_Setup.xml` — IMU Inverse Kinematics Setup**

**Purpose:**
Configures the OpenSense IMU-based Inverse Kinematics (IK) problem.

**What it does:**

* Defines which coordinates (degrees of freedom) are:

  * Free to move
  * Locked or constrained
* Specifies weighting of IMU orientation tracking vs. model constraints.
* Sets up the solver that computes joint kinematics from IMU orientations.

**Role in the pipeline:**
This is the **core optimization step** where sensor data is translated into joint motion.

---

### **5) `OpenSense_CalibrateModel.m` — Model Calibration**

**Purpose:**
Calibrates the OpenSim model to the IMU data before motion tracking.

**What it does:**

* Aligns the model’s initial pose with the IMU data.
* Computes sensor-to-segment alignment parameters.
* Minimizes initial orientation errors between:

  * Measured IMU orientation
  * Model anatomical orientation

**Role in the pipeline:**
A **critical step** — poor calibration leads to bad kinematics later.

---

### **6) `OpenSense_OrientationTracking.m` — Main Tracking Script**

**Purpose:**
Runs the full OpenSense orientation tracking pipeline.

**What it does:**

1. Loads:

   * Hyoid OpenSim model
   * IMU placement file
   * IMU mapping file
   * IMU IK setup
2. Performs:

   * Model calibration
   * IMU-based inverse kinematics
3. Outputs:

   * Joint angles over time
   * Segment orientations
   * Tracked motion results

**Role in the pipeline:**
This is the **master script** that ties everything together and produces the final motion results.

---

## ✅ What Works Currently

* IMU data can be successfully:

  * Converted
  * Placed on C7 and Skull in the Hyoid model
  * Used to run OpenSense calibration
  * Used to run IMU-based inverse kinematics
* The pipeline runs end-to-end without crashing.

---

## 🚧 TO-DO / Next Development Stage

### **1) IMU Frame → OpenSim Frame Mapping (Major Remaining Work)**

We still need to rigorously determine:

* How the **IMU sensor coordinate frame** aligns with the **OpenSim anatomical coordinate frame** for:

  * C7
  * Skull

This includes:

* Defining a consistent rotation convention (e.g., XYZ, ZYX, etc.).
* Determining whether additional fixed rotation offsets are needed.
* Validating this mapping experimentally or against ground-truth motion capture.

---

### **2) Definition of “Proper Angles”**

Open questions that remain:

* What joint angle convention should be used for cervical motion?
* Should we extract:

  * Euler angles?
  * Joint coordinates from OpenSim?
  * Relative orientations between Skull and C7?

This needs to be standardized before using the results for scientific analysis.

---

### **3) Validation**

Future work should include:

* Comparing IMU-derived neck motion with:

  * Optical motion capture (if available), or
  * Published cervical kinematics datasets.

---

## Notes for Future Contributors

If you are picking up this work:

* Start by examining `OpenSense_OrientationTracking.m`.
* Understand how the IMU placement in `myIMUPlacer_Setup.xml` relates to the Hyoid model.
* Focus your effort on solving the **IMU-to-OpenSim frame alignment problem** — this is the key remaining challenge.

---
