%% This is the original scrip that took quaternion data from the .csv files and output ROM values 

%% This software is for non-commercial use only.
%% Commercial use requires a separate license.

close all;
clc;
clear all;

% Add necessary paths.
data_path = "E:\local_git\Cervical_range_of_motion";
genpath('Figures');
addpath("FunctionsFiles")
results_path = "Results - Validation";
mkdir(results_path)

%% Choose raw data file of validation
[fileName, filePath] = uigetfile(fullfile(data_path,"*.*"), "Select a file");
fullfilename_validate = fullfile(filePath, fileName);

options = {'Sagital', 'Frontal', 'Horizontal'};
is_contained = cellfun(@(x) contains(lower(fileName),lower(x)),options);

if any(is_contained)
    chosen_plane = options{is_contained};
else
    % Display the menu and get the user's choice
    chosen_plane = questdlg('Select recorded plane:', 'Menu', options{:}, options{1});
end

%% Extract the angles over time
switch chosen_plane
    case 'Sagital'
        segments = {'zyz',2};
        disp('You selected Sagittal plane.');
    case 'Frontal'
        segments = {'xyz',3;'zyx',1;'zyz',1;'zyz',3};
        disp('You selected Frontal.');
    case 'Horizontal'
        segments = {'xyz';'zyx';'zyz'};
        disp('You selected Horizontal.');
    otherwise
        disp('Invalid choice. Please select a valid option.');
end

nsegments = size(segments,1);
movement_angle_segs = cell(nsegments,1);

for iseg = 1:nsegments
    seg=segments(iseg,:);
    movement_angle_segs{iseg,1} = extract_angle(fullfilename_validate,chosen_plane,seg);
end

%%   Plot the angle over time
fig = figure('WindowState','maximized');
for iseg = 1:nsegments    
    subplot(1,nsegments,iseg)    
    plot(movement_angle_segs{iseg,1},'Color','b');hold on;
    xlabel('Sample')
    ylabel('Angle [degree]')
    if strcmp(chosen_plane,'Horizontal')
        title({"Segment = "+ segments{iseg,1}});
    else
        title({"Segment = "+ upper(segments{iseg,1}); ...
                "Movement axis = " + segments{iseg,2}})
    end
end
sgtitle({"Select 12 datacursors (hold Shift while clicking)"})
%%  Cursors to select manualy the angles.


%%n_cursors = 12;

n_cursors = 20 ;
cursor_info = manual_cursor(fig,n_cursors);

%% Extract angle-to-basline
if length(cursor_info)==n_cursors
    angle_to_baseline = extract_angle_validate(cursor_info,n_cursors);
else
    errordlg('Check the cursors')
end

%% Save angle to csv file
angles_to_csv(angle_to_baseline, fullfilename_validate, results_path)