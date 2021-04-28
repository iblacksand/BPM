function test()
Fs = 20;
data = load('test.csv');
figure
t = linspace(1/Fs, 200, length(data));
plot(t,data)
data = data./norm(data);
% data = data(end-Fs*15:end);
Y = fft(data);
Y = Y(2:length(data)/2+1);
figure
freq = Fs/length(data):Fs/length(data):Fs/2;

cutoff = 240;
ind = find(min(abs(freq - cutoff/60)) == abs(freq - cutoff/60));
cutoff2 = 55;
ind2 = find(min(abs(freq - cutoff2/60)) == abs(freq - cutoff2/60));
freq = freq(ind2:ind);
Y = Y(ind2:ind);
[Ys,I] = max(abs(Y));   
fprintf('Maximum occurs at %3.2f Hz.\n',freq(I))
plot(60*freq, abs(Y))
disp("Max BPM: " + freq(I)*60) 
xlabel("Frequency (BPM)")
end