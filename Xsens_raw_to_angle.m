%%Xsens_raw_to_angle
%{
This script uses the .csv file exported from the Xsens DOT sensors
containing quaternion data from 2 sensors:
W4 (neck) & W5 (back of head)

It computes range of motion between the two sensors
%}

close all;
clc;
clear;

%% Sampling frequency
Fs = 60; % Hz

%% Paths
data_path = "E:\local_git\Cervical_range_of_motion";
addpath("FunctionsFiles")

results_path = "Results - Validation";
mkdir(results_path)

% Select file
[fileName, filePath] = uigetfile(fullfile(data_path,"*.csv"), ...
    "Select Xsens CSV file");

fullfilename = fullfile(filePath, fileName);
%% ===== STEP 1: READ XSENS CSV =====
T = readtable(fullfilename);



%% ===== STEP 4: RUN YOUR ORIGINAL PIPELINE =====

chosen_plane = 'Sagital';
disp('Sagittal plane selected.');

segments = {'zyz', 2};
nsegments = size(segments,1);

movement_angle_segs = cell(nsegments,1);

for iseg = 1:nsegments
    seg = segments(iseg,:);
    movement_angle_segs{iseg,1} = ...
    extract_angle(fullfilename, chosen_plane, seg);
end

%% ===== STEP 5: PLOT =====

fig = figure('WindowState','maximized');

for iseg = 1:nsegments
    angle_data = movement_angle_segs{iseg,1};

    N = length(angle_data);
    time = (0:N-1)' / Fs;

    subplot(1,nsegments,iseg)
    plot(time, angle_data, 'b', 'LineWidth', 1.5);
    grid on;

    xlabel('Time [s]')
    ylabel('Angle [degree]')
    title({
        "Segment = " + upper(segments{iseg,1})
        "Movement axis = " + segments{iseg,2}
    })
end

sgtitle("Sagittal Plane – Angle vs Time")

%% ===== STEP 6: SAVE CSV =====

[fileBase,~,~] = fileparts(fileName);
csv_filename = fullfile(filePath, fileBase + "_angle.csv");

angle_table = table(time, angle_data, ...
    'VariableNames', {'Time_sec', 'Angle_deg'});

writetable(angle_table, csv_filename);

disp("Time–Angle CSV saved to:");
disp(csv_filename);