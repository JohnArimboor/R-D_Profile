%GNU Octave script for LCOS accelerated Aging analysis

%Project Description :- The liquid crystal on silicon(LCOS) devices degrade over when exposed to extrreme heat and high-intensity laser light
% during the stress and reliability tests. The design engineers are interested in knowing when exactly these devices will last before the
%the picture quality becomes unacceptable , which is defined as losing half the contrast ratio. Because testing a display until it naturally dies
%could take years. Here through this code we aim to run "accelerated aging " tests for a few months and use simple maths to predict the rest of its
% lifespan.

%How this code is aiming to achieve it:-
% This script is provided with raw contrast measurement data from a 4694-hour accelerated aging test
%1. First it plots and visualizes the raw data
%2. Next, it uses a mathematical tool called linear regression to cut through the given data and find the average rate at the which the
%display is dying
%3. Finally, it draws the treadline into the future to predict the exact hour where the constrast will drop below 50% failure mark.
% The code aims to provide a final graph showing both the real data and future prediction.

%Input data provided by the reliabiltiy team
time_hrs=[0,90,208,323,488,652,794,991,1058,1225,1345,1436,1603,1696,1768,1832,2089,2226,2419,2543,2662,2922,3133,3588,3996,4306,4694];
contrast=[314,285,293,307,319,320,324,324,316,302,275,280,291,271,276,269,264,291,264,275,287,278,280,280,272,283,275];

% Generate the graph of given data
figure(1);
plot(time_hrs, contrast, 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 6);
title('Figure 1:LCOS Given test data of contrast ratios');
xlabel('Reliability Test time(Hours)');
ylabel('Contrast Ratio');
grid on;
legend('Measured Data')


%Calculate the accelerated datda
% Perform a linear fit of degree 1 polynomical to find the rate of degration to the test
coeffs=polyfit(time_hrs,contrast,1); %SInce you have asked for a single line to go downward which is  y=mx+c , it gives you two values , the slope and y interecept which is m and c
%disp(coeffs); It gives you a list
degradation_slope=coeffs(1);
y_intercept=coeffs(2);

%Code for extrapolaing the linear trend fit to 20000 hours
time_extended= linspace(0,20000,500); % It exteneds the time_hours from 0 to 20000 , the xavlues with 500 points to be pointed
y_points=polyval(coeffs,time_extended)% It generated the y points of the extended time vector using degerdation slop, y intercept data

% Code to define the threshold for contrast which defines the industry standard
initial_contrast=contrast(1);
threshold=initial_contrast*0.5; %Industry standard sets the device is failed if the contrast is reduced to half

%Now since we know the y point where contrast could be halved, we need to define the time of point of failure, which is in x axis
%Calculatiuon for time to failure
%y=mx+c
%y is the threshold, m is the degradation_slope
% x is the time of failure
% c is the y intercept which is the contrast ration when time is zero
ttf = (threshold - y_intercept) / degradation_rate; %Equation to calculate the time to failure


% Plot for extrapolated line
figure (2);
hold on;
%Plot raw data
plot(time_hrs, contrast);
%Plot to fit the extrapolated line
plot(time_extended,y_points,'r--','Linewidth',2);

%Plot the 50% threshold limit of the device
plot([0,20000],[threshold,threshold],'k:','Linewidth',2)

%Code to mark the failure mark
if ~isnan(ttf)
    plot(ttf, threshold, 'rp', 'MarkerFaceColor', 'r', 'MarkerSize', 12);
    legend_ttf = sprintf('Predicted TTF: %.0f hrs', ttf);
else
    legend_ttf = 'No Failure Detected';
end %end the loop in GNU Octave

title('Figure 2: Extrapolated Accelerated Aging prediction');
xlabel('Accelerated Test time (Hours)');
ylabel('Contast Ratio');
grid on;

%Code to add legends for user friendly graph
legend('Measured Data', sprintf('Linear Fit (Rate: %.4f/hr)', degradation_rate),sprintf('50%% Threshold (%.1f)', threshold), legend_ttf);

hold off; %Enables over laying of multiple plots

%Printout for output command
fprintf('\n--- Accelerated Aging Analysis Results ---\n');
fprintf('Degradation Rate: %.4f contrast units per hour\n', degradation_rate);% Print 4 decimal places
fprintf('Failure Contrast Threshold of the device (50%% of initial): %.1f\n', threshold);
fprintf('Predicted Time-to-Failure (TTF): %.0f hours\n', ttf);% Print 0 decimal places


