clear all; close all; clc;

x = load('statsSBBR.txt');

CONTROLLER = 0;
PILOT = 1;
NOISE = -1;

nbins = 7; %Default = 7
xbins = 0:3:21;

%idx_controller = find(x(:,5)==CONTROLLER);

%%%Linha dos controladores

idx = find(x(:,5)==CONTROLLER);

figure (1); %hold on;
subplot(2,1,1); 
hist(x(idx,4),xbins, true); grid on;
title('Holding Time (ATC)')
xlabel('Time (sec)')
ylabel('Relative frequency %');

subplot(2,1,2)
hist(diff(x(idx,2)),nbins, true)
title('Interarrival Time (ATC)')
xlabel('Time (sec)')
ylabel('Relative frequency %');

grid on;
print ('histograms_ATC_xbins7.jpg', '-djpg');


%%%If you want to fit the gamma function to the histogram:
%hold on;
%x1 = 0:3:21;
%z = gampdf(x1,a,b);
%plot(x1,z,'r*--');
%histData2 = hist(z,nbins, true);
%hist(z,nbins, true);


figure (2)
%subplot(2,1,1)

a = 3; b = 2;

% Random number generator with gamma distribution
z=gamrnd(a,b,50e3,1); 

histData1 = hist(x(idx,4),xbins, true);
histData2 = hist(z,xbins, true);

%%% Mean Square Error (MSE)
mse = sum((histData1 - histData2).^2);
hold on;
hist(z,xbins, true); %"facecolor", 'g', "edgecolor","k"
hist(x(idx,4),xbins, true); %"facecolor", 'g', "edgecolor","b"
title(['Mean Square Error= ',num2str(mse)]);
xlabel('Time (sec)');
ylabel('Relative frequency %');

grid on;
print ('histogram_meanSquareError_ATC_xbins7.jpg', '-djpg');
%hold off;


x1 = 0:0.01:16;

%z = gampdf(x1,a,b);
%plot(x1,z,'r*--');

%histData2 = hist(z,nbins, true);
%hist(z,nbins, true);


%if false,


%%% Linha dos pilotos
idx = find(x(:,5)==PILOT);

figure (3)
xbins = 0:3:21;
subplot(2,1,1);
hist(x(idx,4),xbins, true)
grid on;
title('Holding Time (Pilots)')
xlabel('Time (sec)')
ylabel('Relative frequency %');


subplot(2,1,2)
hist(diff(x(idx,2)),xbins, true)
grid on;
title('Interarrival Time (Pilots)')
xlabel('Time (sec)')
ylabel('Relative frequency %');

print ('histograms_Pilots_xbins7.jpg', '-djpg');
%end;

figure (4)

a = 3; b = 1;

% Random number generator with gamma distribution
z=gamrnd(a,b,50e3,1); 

histData1 = hist(x(idx,4),xbins, true);
histData2 = hist(z,xbins, true);

%%% Mean Square Error (MSE)
mse = sum((histData1 - histData2).^2);
hold on;
hist(z,xbins, true); %"facecolor", 'g', "edgecolor","k"
hist(x(idx,4),xbins, true); %"facecolor", 'g', "edgecolor","b"
title(['Mean Square Error= ',num2str(mse)]);
xlabel('Time (sec)');
ylabel('Relative frequency %');

grid on;
print ('histogram_meanSquareError_Pilots_xbins7.jpg', '-djpg');


%%% Do the same to Noise
idx = find(x(:,5)==NOISE);

figure (5)

subplot(2,1,1);
hist(x(idx,4),xbins, true)
grid on;
title('Holding Time (Noise)')
xlabel('Time (sec)')
ylabel('Relative frequency %');


subplot(2,1,2)
hist(diff(x(idx,2)),nbins, true)
title('Interarrival Time (Noise)')
xlabel('Time (sec)')
ylabel('Relative frequency %');

grid on;
print ('histograms_Noise_xbins7.jpg', '-djpg');
%end;


figure (6)

a = 1; b = 1;

% Random number generator with gamma distribution
z=gamrnd(a,b,50e3,1); 

histData1 = hist(x(idx,4),xbins, true);
histData2 = hist(z,xbins, true);

%%% Mean Square Error (MSE)
mse = sum((histData1 - histData2).^2);
hold on;
hist(z,xbins, true); %"facecolor", 'g', "edgecolor","k"
hist(x(idx,4),xbins, true); %"facecolor", 'g', "edgecolor","b"
title(['Mean Square Error= ',num2str(mse)]);
xlabel('Time (sec)');
ylabel('Relative frequency %');

grid on;
print ('histogram_meanSquareError_Noise_xbins7.jpg', '-djpg');





