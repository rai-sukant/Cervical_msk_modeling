%% Converts the IMU degree data to anybody friendly radian format

% -------- USER INPUT --------
input_csv = "E:\local_git\Cervical_ROM\_subject_data_17-3-26\_angle.csv"; 
output_csv = "E:\local_git\Cervical_ROM\_subject_data_17-3-26\Aadith_radians_angle.csv" ; 


dt = 0.01;                             % desired time step (10 ms)
% -----------------------------------

% Read the original CSV
data = readtable(input_csv);

% Extract columns
angle_deg = data.Angle_deg;   % keep angles as-is for now
N = height(data);             % number of samples

% ---- CREATE NEW TIME VECTOR (0, 0.01, 0.02, ...) ----
new_time = (0:N-1)' * dt;

% ---- CONVERT ANGLES FROM DEG → RAD ----
angle_rad = deg2rad(angle_deg);

% ---- CREATE NEW TABLE ----
new_table = table(new_time, angle_rad, ...
    'VariableNames', {'Time_sec', 'Angle_rad'});

% ---- SAVE TO CSV ----
writetable(new_table, output_csv);

disp("Modified file saved to:");
disp(output_csv);