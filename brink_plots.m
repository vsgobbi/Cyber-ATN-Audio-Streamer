Brincando/Aprendendo com diferentes plots no octave

figure 999 
plot(2,1,1) %(row, cols, index)
hist(S(idx,4),nbins, true) %default = x
title('Holding Time')
xlabel('Length (sec)')
ylabel('Amount of Speeches');

figure 4
plot(2,2,2) %(row, cols, index)
hist(S(idx,4),nbins, true) %default = x
title('Holding Time')
xlabel('Length (sec)')
ylabel('Amount of Speeches');

subplot(3,2,2) %(row, cols, index)
hist(S(idx,4),nbins, true) %default = x
title('Holding Time')
xlabel('Length (sec)')
ylabel('Amount of Speeches');

