function test()
    Fs = 20; % Frequency of Measurement
    data = load('test.csv'); % Data has to be loaded from test.csv
    figure
    t = linspace(1/Fs, 20, length(data)); % get time domain
    plot(t,data) % plot data vs. time
    data = data./norm(data); % normalize data
    Y = fft(data); % get fft
    Y = Y(2:floor(length(data)/2+1)); % get only hte first half

    freq = Fs/length(data):Fs/length(data):Fs/2; % get frequency domain

    % find cut off points at 240 and 70 BPM
    cutoff = 240;
    ind = find(min(abs(freq - cutoff/60)) == abs(freq - cutoff/60));
    cutoff2 = 70;
    ind2 = find(min(abs(freq - cutoff2/60)) == abs(freq - cutoff2/60));

    % cut off freq and Y
    freq = freq(ind2:ind);
    Y = Y(ind2:ind);

    [Ys,I] = max(abs(Y));  % find max point
    
    % plot max point
    figure
    plot(60*freq, abs(Y), 'Color', [0 63/255 92/255], 'LineWidth', 3)
    hold on
    plot(60*freq(I), abs(Y(I)),'.', 'MarkerSize', 32, 'Color', [188, 80, 144]/255);
    plot([60*freq(I),60*freq(I)], [0, abs(Y(I))], 'g--', 'LineWidth',3, 'Color', [188, 80, 144]/255, 'HandleVisibility','off')
    % disp("Max BPM: " + freq(I)*60) 
    % xlabel("Frequency (BPM)")

    % Save fft
    Y1 = Y;
    Y = abs(Y);

    [x, l, ~, p] = findpeaks(Y); % find peaks of the fft
    [~, ind] = max(p); % find the highest prominence
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