clear all
close all

mat_file_names = dir(fullfile(pwd,'*.mat'));

num_of_files = length(mat_file_names);

loadcell_avg = zeros(1, num_of_files);
rpm_avg = zeros(1, num_of_files);
cmd_raw_avg = zeros(1, num_of_files);

for i = 1:num_of_files

    dir = mat_file_names(i).name;
    
    [loadcell_data, rpm_data, cmd_raw_data] = data_arrange(dir);
    
    loadcell{i} = loadcell_data;
    loadcell_avg(1,i) = sum(loadcell_data(:,2))/length(loadcell_data(:,2));

    rpm{i} = rpm_data;
    rpm_avg(1,i) = sum(rpm_data(:,2))/length(rpm_data(:,2));

    cmd_raw{i} = cmd_raw_data;
    cmd_raw_avg(1,i) = sum(cmd_raw_data(:,2))/length(cmd_raw_data(:,2));

    clear loadcell_data
    clear rpm_data
    clear cmd_raw_data;

end

p_cmd_raw = polyfit(cmd_raw_avg, loadcell_avg, 2);
p_rpm = polyfit(rpm_avg, loadcell_avg, 2);

cmd_domain = 1000:10:6687;
rpm_domain = 1000:10:8000;
moment_pred = p_cmd_raw(1)*cmd_domain.^2 + p_cmd_raw(2)*cmd_domain + p_cmd_raw(3);
moment_pred_rpm = p_rpm(1)*rpm_domain.^2 + p_rpm(2)*rpm_domain + p_rpm(3);

figure(1)
subplot(121)
plot(cmd_raw_avg, loadcell_avg, '*','MarkerSize',10)
hold on
plot(cmd_domain, moment_pred, 'LineWidth', 2)
title('moment - cmd raw value','Interpreter','latex','FontSize',18)
xlabel('cmd raw value','Interpreter','latex','FontSize',14)
ylabel('moment $(N\cdot m)$','Interpreter','latex','FontSize',14)
grid on;

subplot(122)
plot(rpm_avg, loadcell_avg, '*','MarkerSize',10)
hold on
plot(rpm_domain, moment_pred_rpm, 'LineWidth',2)
title('moment - rotor speed','Interpreter','latex','FontSize',18)
xlabel('rotor speed (rpm)','Interpreter','latex','FontSize',14)
ylabel('moment $(N\cdot m)$','Interpreter','latex','FontSize',14)
grid on

set(gcf, 'position', [100, 100, 800, 300])

exportgraphics(gcf, 'moment_data.png','Resolution',600)