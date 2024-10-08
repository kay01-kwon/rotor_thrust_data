function [load_cell, actual_rpm, cmd_raw] = data_arrange(dir, idx)
%DATA_ARRANGE 이 함수의 요약 설명 위치
%   자세한 설명 위치
load(dir);


load_cell_size = length(dict_array{1}.load_cell_moment);
actual_rpm_size = length(dict_array{2}.actual_rpm);
cmd_raw_size = length(dict_array{3}.cmd_raw_data);

load_cell = zeros(load_cell_size, 2);
actual_rpm = zeros(actual_rpm_size, 5);
cmd_raw = zeros(cmd_raw_size, 5);

% Put load cell data
load_cell(:,1) = dict_array{1}.load_cell_secs... 
    + dict_array{1}.load_cell_nsecs/1e9;

load_cell(:,2) = dict_array{1}.load_cell_moment;

% Put actual rpm data
actual_rpm(:,1) = dict_array{2}.actual_rpm_secs...
    + dict_array{2}.actual_rpm_nsecs/1e9;

actual_rpm(:,2:5) = dict_array{2}.actual_rpm;

% Put cmd raw data
cmd_raw(:,1) = dict_array{3}.cmd_raw_secs...
    + dict_array{3}.cmd_raw_nsecs/1e9;

cmd_raw(:,2:5) = dict_array{3}.cmd_raw_data;

end

