% Find the best value for alpha and beta for the gamma pdf

% Call function as: $ [a b mse] = fitdata('statsSBBR.txt', 0)
% filestr: filename 
% TYPE: 0 - Controller
%       1 - Pilot

function [retA, retB retMSE] = fitdata( filestr, TYPE );

x   = load(filestr);
idx = find(x(:,5)==TYPE);

% Measurement Data
X = x(idx,4);

A = 1:1:10;
B = 1:1:10;

xbins = 0:3:21;

% All combinations of AxB
for i=1:length(A),
	for j=1:length(B),
		a = A(i);
		b = B(j);
		Z = gamrnd(a,b,50e3,1); 

		% Mean Square Error
		histData1 = hist(X,xbins, true);
		histData2 = hist(Z,xbins, true);
		mse(i,j) = sum((histData1 - histData2).^2)./length(histData1);

	end
end

% Min value of a matrix
minValue = min(min(mse));

% Finding the minimun error
[i,j] = find( mse <= minValue );

%disp(['A = ', num2str(A(i))]);
%disp(['B = ', num2str(B(j))]);

retA = A(i);
retB = B(j);
retMSE = minValue;

% Plot error with color (X,Y)
figure;
imagesc(A,B,mse'); colorbar;


hold on;
plt = plot(retA,retB,'ow');
%Legend
xlabel('alpha')
ylabel('beta')
%L1 = legend([plt], {'alpha = A', 'beta = ?' }, 'Location', 'NorthEast'); % warning: legend ignoring extra labels
title (['alpha= ', num2str(retA),' beta= ',num2str(retB)])
hold off


%save the image to current folder
%print ('alphaBeta_.jpg','-djpg');
