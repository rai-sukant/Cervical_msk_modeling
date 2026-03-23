%% xsens txt to csv
%% This script converts the quaternions Xsens mtw .txt file to a csv file


clc;
clear;
close all;

%% ---- USER DEFINED TIME STEP ----
dt = 0.01;   % seconds

%% ---- SELECT SENSOR 1 FILE ----
[file1, path1] = uigetfile('*.txt', 'Select TXT file for Sensor 1');
if isequal(file1,0)
    error('Sensor 1 file not selected');
end
fullfile1 =  fullfile(path1, file1);

%% ---- SELECT SENSOR 2 FILE ----
[file2, path2] = uigetfile('*.txt', 'Select TXT file for Sensor 2');
if isequal(file2,0)
    error('Sensor 2 file not selected');
end
fullfile2 = fullfile(path2, file2);

%% ---- READ FILES ----
data1 = readtable(fullfile1, 'FileType', 'text');
data2 = readtable(fullfile2, 'FileType', 'text');

%% ---- EXTRACT QUATERNIONS ONLY ----
quat1 = data1(:, {'Quat_q0','Quat_q1','Quat_q2','Quat_q3'});
quat2 = data2(:, {'Quat_q0','Quat_q1','Quat_q2','Quat_q3'});

%% ---- RENAME COLUMNS ----

quat1.Properties.VariableNames = { ...
    'AvantiSensor1_ORIENT_W1', ...
    'AvantiSensor1_ORIENT_X1', ...
    'AvantiSensor1_ORIENT_Y1', ...
    'AvantiSensor1_ORIENT_Z1'};

quat2.Properties.VariableNames = { ...
    'AvantiSensor2_ORIENT_W2', ...
    'AvantiSensor2_ORIENT_X2', ...
    'AvantiSensor2_ORIENT_Y2', ...
    'AvantiSensor2_ORIENT_Z2'};

%% ---- ENSURE SAME NUMBER OF SAMPLES ----

N1 = height(quat1);
N2 = height(quat2);
N = min(N1, N2);

quat1 = quat1(1:N, :);
quat2 = quat2(1:N, :);

%% ---- CREATE TIME COLUMN ----

Time_sec = (0:N-1)' * dt;

Time_table = table(Time_sec);

%% ---- COMBINE EVERYTHING ----

combined_table = [Time_table quat1 quat2];

%% ---- SAVE CSV ----

output_csv = fullfile(path1, 'combined_imus_quaternion_with_time.csv');

writetable(combined_table, output_csv);

disp('CSV successfully created with Time column:');
disp(output_csv);
