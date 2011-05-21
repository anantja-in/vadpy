function decisions = vad_energy(signal, fs, varargin)

%  SIPU
%  University of Joensuu
%  Rahim Saeidi
%  June 2, 2009
%
%  Processing part edited by Zaur Nasibov for vad.py framework
%  Nov 14, 2009
%
% Description
% This function provide annotation of database which its path specified
% in the dataset_path variable for Voice Activity Detection purpose. In other
% words this function will produce a text file in target_path (for each file exists in 
% databse - with same name) by .Energy.VAD extension which
% includes duration and energy based decision regarding if it is voiced or
% not. 
%
% The format of output .Energy.VAD file is as follows:
%    Start time (in seconds)     End time (in seconds)    Label (1 means voiced)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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

function indic = VoiceActivityDetector(Frames)
% New VAD developed by Hanwu:
%
%   1. Divide signal into 30ms frames, 10ms overlap
%   2. Obtain frame standard deviation in dB
%   3. Find max. value of std over the whole signal (max1)
%   4. Select frames for which std>max1-30 and std>-55.
%      The 30 dB threshold is considered 'general' SNR of the files.

S = 20*log10(std(Frames') + eps);
max1 = max(S);
indic = (S>max1-30) & (S>-55);
