%{ This script uses the .csv file exported from the delsys sensor
%containing quaternion data from 2 sensors and uses it to calculate the range of motion
%between the two sensors 
%}

close all;
clc;
clear all;

% Sampling frequency
Fs = 60; % Hz

% Add necessary paths
data_path = "E:\local_git\Cervical_range_of_motion";
genpath('Figures');
addpath("FunctionsFiles")

results_path = "Results - Validation";
mkdir(results_path)

% Choose raw data file of validation
[fileName, filePath] = uigetfile(fullfile(data_path,"*.*"), ...
    "Select a file");
fullfilename_validate = fullfile(filePath, fileName);

% Only Sagittal plane
chosen_plane = 'Sagital';
disp('Sagittal plane selected.');

% Extract angles (ONLY zyz, axis 2)
segments = {'zyz', 2};
nsegments = size(segments,1);

movement_angle_segs = cell(nsegments,1);

for iseg = 1:nsegments
    seg = segments(iseg,:);
    movement_angle_segs{iseg,1} = ...
        extract_angle(fullfilename_validate, chosen_plane, seg);
end

% Plot angle vs TIME
fig = figure('WindowState','maximized');

for iseg = 1:nsegments
    angle_data = movement_angle_segs{iseg,1};

    %Time vector
    N = length(angle_data);
    time = (0:N-1)' / Fs;  % seconds

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

% ===== SAVE Time vs Angle to CSV =====

%Create output filename
[fileBase,~,~] = fileparts(fileName);
csv_filename = fullfile(filePath, fileBase + "_angle.csv");

%Combine time and angle into table
angle_table = table(time, angle_data, ...
    'VariableNames', {'Time_sec', 'Angle_deg'});

%Write to CSV
writetable(angle_table, csv_filename);

disp("Time–Angle CSV saved to:");
disp(csv_filename)
