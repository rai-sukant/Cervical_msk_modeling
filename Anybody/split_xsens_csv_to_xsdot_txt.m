%% Function defition 



function split_xsens_csv_to_xsdot_txt(inputCsv, outputFolder)
% split_xsens_csv_to_xsdot_txt
%
% Converts combined Xsens CSV into 5 separate XSDot-style .txt files
% with correct header and naming.

arguments
    inputCsv (1,1) string
    outputFolder (1,1) string
end

if ~exist(outputFolder, 'dir')
    mkdir(outputFolder);
end

% Read CSV
T = readtable(inputCsv);

N = height(T);

PacketCounter = (1:N)';
SampleTimeFine = T.sampleTimeFine;

% Sensor name mapping
sensorNames = ["Pelvis", "RFemur", "LFemur", "RTibia", "LTibia"];

% File prefix
filePrefix = "XSDot_20210820_202113_";

% Fixed header text
headerText = [ "// General information: # Original fixed header", ...
"//  MT Manager version: 2022.2.0", ...
"//  XDA version: 2022.2.0 build 7381 rev 124627 built on 2023-07-19", ...
"// Device information:", ...
"//  DeviceId: B42D48", ...
"//  ProductCode: MTW2-3A7G6", ...
"//  Firmware Version: 4.4.0", ...
"//  Hardware Version: 1.1.0", ...
"// Device settings:", ...
"//  Filter Profile: human(46.1)", ...
"//  Option Flags: Orientation Smoother Disabled, Position/Velocity Smoother Disabled, Continuous Zero Rotation Update Disabled, AHS Disabled, ICC Disabled", ...
"// Coordinate system: ENU",...
];

for sensorID = 1:5

    % Extract quaternion columns
    qw = T.(sprintf('W%d_quat_w', sensorID));
    qx = T.(sprintf('W%d_quat_x', sensorID));
    qy = T.(sprintf('W%d_quat_y', sensorID));
    qz = T.(sprintf('W%d_quat_z', sensorID));

    % Output file name
    fileName = filePrefix + sensorNames(sensorID) + ".txt";
    outputFile = fullfile(outputFolder, fileName);

    fid = fopen(outputFile, 'w');

    % Write header
    for i = 1:length(headerText)
        fprintf(fid, '%s\n', headerText(i));
    end

    % Write column header
    fprintf(fid, 'PacketCounter\tSampleTimeFine\tQuat_q0\tQuat_q1\tQuat_q2\tQuat_q3\n');

    % Write data rows
    for i = 1:N
        fprintf(fid, '%d\t%d\t%.6f\t%.6f\t%.6f\t%.6f\n', ...
            PacketCounter(i), ...
            SampleTimeFine(i), ...
            qw(i), qx(i), qy(i), qz(i));
    end

    fclose(fid);

    fprintf("Written: %s\n", outputFile);

end

fprintf("\nAll XSDot files created successfully.\n");

end
