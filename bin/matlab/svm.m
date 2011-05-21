function svm(svm_function, endianness, frame_len, ...
             input_paths, gt_paths, output_paths)
% Usage: svm(svm_function, endianness, frame_len, input_paths, gt_paths ,output_paths)
%
%
%Parameters:
%svm_function     - matlab VAD function to use
%endianness       - files endianness ('b' for BIG ENDIAN; 'l' for LITTLE ENDIAN)
%frame_len        - GT frame length
%input_paths      - input file(s') paths separated by ';'
%gt_paths         - corresponding GT paths separated by ';'
%output_paths     - corresponding VAD output's paths separated by ';'

input_paths = regexp(input_paths, ';', 'split');
output_paths = regexp(output_paths, ';', 'split');
gt_paths = regexp(gt_paths, ';', 'split');
frame_len = str2num(frame_len);

FS = 8000;
BPS = 16;

for i = 1:length(input_paths)
    in_path = char(input_paths(i));
    fin_id = fopen(in_path, 'rb', endianness);
    
    [s, count] = fread(fin_id, 'int16', endianness); % input signal
    s = s / max(abs(s));
		
	MFCCParam.TargetFs      = 8000; % Sampling rate
	MFCCParam.NumFilters    = 24;   % Number of mel filters
	MFCCParam.NumCoeffs     = 12;   % Number of cepstral coefficients
	MFCCParam.NFFT          = 512;  % FFT size
	MFCCParam.FMinHz        = 0;    % Min frequency (Hz) of the MFCC filterbank
	MFCCParam.FMaxHz        = 4000; % Max frequency (Hz) of the MFCC filterbank
	MFCCParam.SpecFun       = 'hamming';    % 'thomson', 'multipeak', 'SWCE2', 'multisine'
	MFCCParam.NumTapers     = 12; % takes effect only for the multitaper methods
	Frames = enframe(s, boxcar(240), 120);
	c = MFCCExtract(Frames, MFCCParam, ones(length(Frames), 1), false);    
   c = c - repmat(mean(c), size(c,1), 1); % normalization
    gt_path = char(gt_paths(i));
    
    if strcmp(svm_function, 'train') 
        gt_id = fopen(gt_path, 'rb');
        gt_labels = fgetl(gt_id);
        gt_labels = gt_labels - '0';          % a dirty trick to convert a string into vector

		  % gt_labels = resample(gt_labels, size(mfc, 1), length(s) / ...
        %                      FS / frame_len);
        
        gt_labels = gt_labels(1: min(size(c, 1), length(gt_labels)));
        c = c(1: min(size(c, 1), length(gt_labels)), :);
        gt_labels = round(gt_labels);
        gt_labels(gt_labels == 0) = -1; % prepare labels for SVM
        gt_labels = gt_labels';               % turn into column-vector
        fclose(gt_id);
        
        model = svm_train(c, gt_labels);
        model_path = char(output_paths(i));
        save(model_path, 'model');
    end
    
    if strcmp(svm_function, 'test')
        labels = svm_test(c, gt_path);
        labels(labels == -1) = 0; % prepare labels for VADpy
        
        % labels = resample(labels, length(s) / FS / frame_len , size(mfc, 1));
        labels = round(labels);
        labels = labels(1: min(size(c, 1), length(s) / FS / frame_len));

        fout_path = char(output_paths(i));
        fout_id = fopen(fout_path, 'wt'); 
        fprintf(fout_id, '%i', labels);
        fclose(fout_id);
    end    
    
    fclose(fin_id);
end

exit; % required by VADpy framework to return from matlab process

end % function train   
