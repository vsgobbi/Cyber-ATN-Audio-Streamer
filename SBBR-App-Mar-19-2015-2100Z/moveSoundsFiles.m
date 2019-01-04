%Cyber range ATN Testbed
%Created by Vitor Sgobbi, 2015
%Brazilian Airspace Traffic Control Institute (ICEA)
%segment and move files to specific folders


clear all; close all; clc;

x = load('statsSBBR.txt');

CONTROLLER = 0;
PILOT = 1;
NOISE = -1;

%%mkdir('/opt/crat/core/sounds')

%1 = Armazenar os arquivos .mp3 da pasta atual através de um struct array
%2 = Armazenar cada arquivo numa celula em forma de matrizes
%3 = Atribuir cada id para ao arquivo .mp3
%3 = Mover todos os arquivos para a pasta desejada

%%%Funcao dos controladores
% ATC sounds separete and copy function
%idx = find(x(:,5)==CONTROLLER);

%dirATC = '/opt/crat/core/home/sounds/ATC/';
%mkdir (dirATC);

dirData = dir(fullfile('*.mp3'));
fileNames = {dirData.name};

%for i = 1:length(dirData)
	%mvIdx = idx(i)
	%idxATC= idx+'*';
	
	%[~, f] = fileparts(dirData(i).name);
	%num = str2double(f);
		
	%newName = strcat('atc', fileNames(i),sprintf('%d', i)); %create new name for each file
	%idxFiles = {idx.name};
	
		
%newRunFilesATC = cellstr(num2str(idx(:),'atc_%d.mp3'));
%newRunFiles = strtrim(newRunFiles);	
	%fileNames = num2str(idx,'atc_%d.mp3');	
		
	%if ~isnan(num)
%copyfile(fileNames(idx), dirATC,'f');
	%movefile(newRunFiles(i),fileNames);
	%end
%end

%%%Doing the same for Pilots sounds
%Linha dos pilotos
idx = find(x(:,5)==PILOT);
dirP = ('/opt/crat/core/home/sounds/PILOTS/');
mkdir (dirP)

%for i = 1:length(dirData)
	%fileNames = fileNames(idx);
	%fileNames = num2str(idx);	
	%idx = length(idx - 1);	
	%newRunFilesPilots = cellstr(num2str(idx(:),'pilots_%d.mp3'));
	%copyfile(fileNames(idx), dirP, 'f');
	%movefile('idx*', '/opt/crat/core/home/sounds/PILOTS/')
%end


%%%And again doing the same for Noise sounds
%Linha de ruido
idx = find(x(:,5)==NOISE);
dirR = ('/opt/crat/core/home/sounds/NOISE/');
mkdir (dirR);

%loop through each file
for i = 1:length(dirData)
	
	%get the filename minus the extension
	%[~, f] = fileparts(dirData(i).name);

	
	%fileNames = fileNames(idx);
	%newRunFilesNoise = cellstr(num2str(idx(:),'noise_%d.mp3'));	
	%for fileNames(idx) = length(dirData)	
	%newfileNames = fileNames(num2str(idx(:),'noise_%d.mp3'));
	
	newRunFilesNoise = cellstr(num2str(idx(:),'noise_%d.mp3'));
	newRunFiles = strtrim(newRunFilesNoise);	
	
	%create new name for each file	
	%newName = strcat('noise', fileNames(i),sprintf('%d', i)); 
	
	%copyfile(newfileNames, dirR, 'f');
	%movefile('idx*','/opt/crat/core/home/sounds/NOISE/')
	
	for j = 1:(idx)
		copyfile(fileNames(idx), dirR, 'f');
	end
end





