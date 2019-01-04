%gamma distribution sample : Exemplo de plot de Gamma Probability Density Function 
%"Encaixe" para os histogramas de "Holding Time" e "Interarrival Time" dos Controladores de SBBR-APP
%y~gamma(alpha,beta) , onde alpha e beta > 0
%uso de distribuicao gamma: achar a prioridade para uma precisao... 
%formula: se alpha = 1 ==> P(y/alpha=1,beta)~e^-beta*y
%onde P = probabilidade, y = média de uma da variável
%neste caso y tem o peso ao gerar a parábola quando alpha >= 2, exemplo: se alpha = 2 ==>
%P(y/alpha=2,beta)~y*e^-P*y, onde y aumenta a parábola e gera pico. 
%quanto maior o valor de beta mais ponteaguda é a parábola, maior a queda da distribuicao para 0. 
% Instituto de Controle do Espaço Aéreo - Vitor Sgobbi, 2015
% Referencias:  http://www.statlect.com/gamma_distribution_plots.htm  

clear; close all; clc;

%configurar eixos x e y
x = 0:0.05:20;
xlimit = [0 20];
ylimit = [0 0.35];
xtick = [0 5 10 15 20];
ytick = [0 0.05 1 0.15 0.2 0.25 0.3 0.35];

%computa o pdf
n1 = 6; h1 = 3.5; a1=n1/2; b1=2*h1/n1;  %h = media e n = n grau %default n1= 6, h1 =3 
y1 = gampdf (x,a1,b1); %onde x são os limites do eixo x, a1 e b1 médias de h e n

%cria o plano para o plot
h = plot(x,y1,'LineWidth',4,'color','white');
set(gca, 'XLim', xlimit, 'XTick', xtick, 'YLim', ylimit, 'YTick', ytick, 'FontSize', 10,'FontName', 'Arial'); 			% altera posicoes do grafico para os limites dados

%plotar as grades para o eixo X (vertical)
for j=xtick
	line ('xData',[j j], 'yData', ylimit, 'color', [0.75 0.75 0.75], 'LineWidth', 0.5)
end

%plotar as grades para o eixo Y (horizontal)
for j=ytick
	line ('xData', xlimit, 'yData', [j j], 'color', [0.75 0.75 0.75], 'LineWidth', 0.5)
end

%plotar os eixos
line('xData', [0 0], 'yData', ylimit, 'LineWidth', 1, 'color', [0 0 0], 'LineWidth', 0.5)
line('xData', xlimit, 'yData', [0 0], 'LineWidth', 1, 'color', [0 0 0], 'LineWidth', 0.5)

%plotar o pdf finalmente
h1 = line(x,y1, 'LineWidth', 4, 'color', 'red');
%line([3-0.02 3-0.02],[0 gampdf(3,a1,b1)], 'LineWidth', 2, 'color', 'red') %barra correspondente a media

%legenda e titulo
L = legend([h1 ], {'n = 6 , h = 3.5'}, 'Location', 'NorthEast');
title ('Gamma Distribution')

%salvar como imagem
print('exemplo1GammaDistribution10.png','-dpng')



