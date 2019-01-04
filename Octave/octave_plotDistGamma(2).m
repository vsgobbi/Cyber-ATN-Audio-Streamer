%----------- outro exemplo de plot gampdf ---------------
% Instituto de Controle do Espaço Aéreo - Vitor Sgobbi, 2015
% Referencias: 

clear; close all; clc;

alpha = 2;
beta = 1;
theta = 1/beta;

v_x = 0:0.001:100; %mesmo que a funcao linspace
v_y = gampdf(v_x,alpha,theta); % gamma probability density function

mean = (1/sum(v_y))*sum(v_x*v_y); %
figure (1)
plot (v_x,v_y,"r*",1)
xlabel('Theta')
ylabel('PDF')
set(h,'Position',[1000 150 900 900])
title ("Distribuição Gamma")



%x = linspace(0,1,100); %espacamento? default: (0,1,100)
%y = betapdf(x,2.8,2); %valor default para beta a=3 e b=3. Gera uma função pico!

%h = figure (1);
%plot(x,y,'LineWidth',3)
%xlabel('Theta')
%ylabel('pdf')
%set(h,'Position',[1000 150 900 900])
