function test()
Fs = 20;
data = load('test.csv');
figure
t = linspace(1/Fs, 200, length(data));
plot(t,data)
data = data./norm(data);
% data = data(end-Fs*15:end);
Y = fft(data);
Y = Y(2:floor(length(data)/2+1));

freq = Fs/length(data):Fs/length(data):Fs/2;
figure
plot(freq*60, abs(Y))
cutoff = 240;
ind = find(min(abs(freq - cutoff/60)) == abs(freq - cutoff/60));
cutoff2 = 70;
ind2 = find(min(abs(freq - cutoff2/60)) == abs(freq - cutoff2/60));
freq = freq(ind2:ind);
Y = Y(ind2:ind);
[Ys,I] = max(abs(Y));   
% fprintf('Maximum occurs at %3.2f Hz.\n',freq(I))
figure
plot(60*freq, abs(Y), 'Color', [0 63/255 92/255], 'LineWidth', 3)
hold on
plot(60*freq(I), abs(Y(I)),'.', 'MarkerSize', 32, 'Color', [188, 80, 144]/255);
plot([60*freq(I),60*freq(I)], [0, abs(Y(I))], 'g--', 'LineWidth',3, 'Color', [188, 80, 144]/255, 'HandleVisibility','off')
% disp("Max BPM: " + freq(I)*60) 
% xlabel("Frequency (BPM)")

Y1 = Y;
Y = abs(Y);

[x, l, ~, p] = findpeaks(Y);
[~, ind] = max(p);
fprintf('Maximum occurs at %3.2f Hz.\n',freq(l(ind)))
disp("Max BPM: " + freq(l(ind))*60)
I = l(ind);
plot(60*freq(I), abs(Y(I)),'.', 'MarkerSize', 32, 'Color', [243, 202, 64]/255);
plot([60*freq(I),60*freq(I)], [0, abs(Y(I))], 'g--', 'LineWidth',3, 'Color', [243, 202, 64]/255, 'HandleVisibility','off')
ylim([0, max(abs(Y))*1.1])
xlim([cutoff2,cutoff])
legend('FFT', 'Max Peak', 'Prominence', 'FontWeight','normal');
title('FFT Peak Detection')
set(gca,'FontSize',18)
set(gca,'fontname',"Palatino")
set(gca,'FontWeight','bold')

figure
yy = ifft(Y1);
x = 1:length(yy);
plot(x/Fs, abs(yy))
end