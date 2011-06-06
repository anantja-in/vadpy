function decisions = vad_entropy(signal, fs, varargin)

% Parameters
Fs = fs;
s = signal;

FrameLen = 240;
FrameShift = FrameLen / 3;
W = hamming(FrameLen);

% VAD
s = s / max(abs(s));
Frames = enframe(s, W, FrameShift);
Vindic = VoiceActivityDetector(Frames);

decisions = Vindic;

function indic = VoiceActivityDetector(frames)
NFFT = 512;

nframes = size(frames, 1);
spec = fft(frames, NFFT, 2);
H = zeros(nframes, 1);

for i = 1:nframes
	spec_frame = spec(i,:);
	p_sum = sum(abs(spec_frame));
	p = abs(spec_frame).^2 / p_sum;
	h = -sum(p.*log(p));
	H(i) = h;	
end
%H = H / max(H);
min1 = min(H(H > 0));
H(H <= 0) = min1;

%max1 = max(H);
std1 = std(H);
mean1 = mean(H);
indic = (H > 0.4) & (H > min1 + abs(mean1 - std1)); 
echo
