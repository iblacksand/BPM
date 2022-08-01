function bpm()
    %% PARAMETERS

    PORT = 'com4'; % port being used by arduino (string)
    BOARD_TYPE = 'uno'; % type of arduino board (string)
    CYCLE_TIME = 5; % length of one cycle (integer; seconds)
    TOTAL_TIME = 60; % total time to measure (integer; seconds)
    ACQUISITION_RATE = 40; % frequency of sensor (integer; Hz)
    SAVE_DATA = false; % should the data be saved (boolean)

    %% ACQUISITION PHASE

    f = waitbar(0,'Please wait...');
    a = arduino(PORT, ); % Change com4 to the port that is being used by the arduino
    c = ceil(TOTAL_TIME/CYCLE_TIME); % total number of cycles 
    for i = 1:c
        data = [];
        for j = 1:ceil(CYCLE_TIME*ACQUISITION_RATE)
            v = readVoltage(a, 'A0'); % read data from port
            waitbar((i*j)/(TOTAL_TIME*ACQUISITION_RATE),f,"LIVE VOLTAGE: " + v); % display data
            data = [data, v]; % add to array
            java.lang.Thread.sleep(1000/ACQUISITION_RATE); % sleep for the set period of time
        end
        calculate(data, ACQUISITION_RATE, TOTAL_TIME); % calculate BPM
    end
end

function calculate(data, Fs, TOTAL_TIME)
    figure
    t = linspace(1/Fs, TOTAL_TIME, length(data)); % get time domain
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
    set(gca,'fontname',"Inter")
    set(gca,'FontWeight','bold')
end