%beta distribution sample : Exemplo de plot de Beta Probability Density Function 
%"Encaixe" para os histogramas de "Holding Time" e "Interarrival Time" dos Controladores de SBBR-APP
%A distribuicao beta geralmente é utilizada em conjunção com a distribuição binominal, particularmente em modelos Bayesianos onde possui
%um papel importante como distribuição prévia de p
%Instituto de Controle do Espaço Aéreo - Vitor Sgobbi, 2015
%Referencias: http://www.unc.edu/courses/2008fall/ecol/563/001/docs/lectures/lecture3.htm

%For each element of X, compute the probability density function (PDF) at X of the Beta distribution with parameters A (alpha) and B (beta).


clear; close all; clc;


%configurar eixos x e y para o histograma "Holding Time (Controladores"
x = 0:0.05:20;
xlimit = [0 20];
ylimit = [0 0.35];
xtick = [0 5 10 15 20];
ytick = [0 0.05 1 0.15 0.2 0.25 0.3 0.35];

%computa o betapdf
%x = linspace(0,1,100); %espacamento? default: (0,1,100)
y = betapdf(x, 3, 3); %valor default para beta a=3 e b=3 gera uma funçao pico


%cria o plato para o plot
figure (1)
h = plot(x,y,'LineWidth',4,'color','white');
set(gca, 'XLim', xlimit, 'XTick', xtick, 'YLim', ylimit, 'YTick', ytick, 'FontSize', 10,'FontName', 'Arial'); 	

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
h1 = line(x,y, 'LineWidth', 4, 'color', 'red');
%line([3-0.02 3-0.02],[0 gampdf(3,a1,b1)], 'LineWidth', 2, 'color', 'red') %barra correspondente a media

%legendas e titulo
L = legend([h1], {'n = ?, h = ?'}, 'Location', 'NorthEast');
xlabel('Theta')
ylabel('pdf')
title ('Beta Distribution');



%figure (1);
%plot(x,y,'r*','LineWidth',3)
%set(h,'Position',[1000 150 900 900])
%title ("Distribuição Beta")









%segundo plot para comparacao:

x = linspace(0,1,60); %espacamento? default: (0,1,100)

y = betapdf(x,3.5,2); %valor beta 3 e 3 gera funçao pico

h = figure (2);
plot(x,y,'LineWidth',3)
xlabel('Theta')
ylabel('pdf')
set(h,'Position',[1000 150 900 900])



%terceiro plot para comparacao:

x = linspace(0.6,0.1,20); %espacamento? default: (0,1,100)

%valor beta 3 e 3 gera funçao pico
y = betapdf(x,3,3);  z = betacdf (x,3,3); 
y2 = betapdf(x,3,2); z2 = betacdf (x,3,2);
y3 = betapdf(x,2,2); z3 = betacdf (x,2,2);
y4 = betapdf(x,2,1); z4 = betacdf (x,2,1);
y5 = betapdf(x,1,1); z5 = betacdf (x,1,1);
h = figure (3);
subplot (1,2,1);
plot(y,'r*',y2,'g*',y3,'k*',y4,'b*',y5,'y*','LineWidth',4)
subplot (1,2,2);
plot(z,'r*',z2,'g*',z3,'k*',z4,'b*',z5,'y*','LineWidth',4)

%xlabel('Theta')
%ylabel('pdf')

y2 = betapdf(x,5,3);
plot(x,y2,'r*')

set(h,'Position',[1000 150 900 900])

