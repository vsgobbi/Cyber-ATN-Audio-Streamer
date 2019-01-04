clear all;
close all;

S = load('statsSBBR.txt');

controllers = 0;
pilots = 1;

nbins = 7;

idx_controller = find(x(:,5)==controllers);

% Linha dos controladores
idx = find(x(:,5)==controllers);

figure (1)
subplot(2,1,1) %(row, cols, index)
hist(S(idx,4),nbins, true) %default = x
title('Holding Time')
xlabel('Length (sec)')
ylabel('Amount of Speeches');


subplot(2,1,2)
hist(diff(S(idx,2)),nbins, true)
title('Interrarival time')
xlabel('Lenght (sec)')
ylabel('Number of calls');



% Linha dos pilotos
idx = find(x(:,5)==PILOT);

figure (2)
subplot(2,1,1)
hist(S(idx,4),nbins, true)
title('Holding Time')
xlabel('Tempo (sec)')
ylabel('Quantidade de chamadas');


subplot(2,1,2)
hist(diff(S(idx,2)),nbins, true)
title('Interrarival time')
xlabel('Tempo (sec)')
%ylabel('Quantidade de chamadas');
