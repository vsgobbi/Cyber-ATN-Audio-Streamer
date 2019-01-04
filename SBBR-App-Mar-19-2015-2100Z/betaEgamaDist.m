clc; clear all;

x = 0:0.5:30;

alpha = 3;
beta = 2;

gama = gampdf (x, alpha, beta);
beta = betapdf (x, alpha, beta);

figure (1);
title ("Distribuicao Gamma e Beta");

subplot(2,1,1);
pdf1 = plot (x, gama, 'r*-');
ylabel ('Distribuicao Gamma');
L1 = legend([pdf1], {'alpha = 3, beta = 2'}, 'Location', 'NorthEast');
hold on;
subplot (2,1,2);
pdf2 = plot (x, beta, 'k*-');
ylabel ('Distribuicao Beta');
L2 = legend([pdf2], {'alpha = 3, beta = 2'}, 'Location', 'NorthEast');

%print('betaGamaDistributions.png', '-dpng');

