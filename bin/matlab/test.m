% sound_path = '/home/zaur/Documents/Study/vadpy2/output/zaur/split/Aurora2/TRAIN_1_C_60/N1_SNRC.0';
% gt_path = '/home/zaur/Documents/Study/vadpy2/output/zaur/split/Aurora2/TRAIN_1_C_60/GT/N1_SNRC.0';
% model_path = '/home/zaur/Documents/Study/vadpy2/output/zaur/matlab/svm_train/AN1_60.mat';
% out_path = '/home/zaur/Documents/Study/vadpy2/output/zaur/split/Aurora2/TRAIN/GT/N1_SNRC.0.out';

%sound_path = '/home/zaur/Documents/Study/thesis/experiments/workdir/data/FAK_1B.10';
sound_path = '/home/zaur/Documents/Study/thesis/experiments/workdir/data/jamjB';

%sound_path = '/home/zaur/Documents/Study/vadpy2/databases/AURORA2/TRAIN/DATA/N1_SNR5'; 
%gt_path =    '/home/zaur/Documents/Study/vadpy2/databases/AURORA2/TRAIN/GT/N1_SNR5';
% model_path = '/home/zaur/Documents/Study/vadpy2/output/zaur/matlab/svm_train/Aurora2/TRAIN/N1_SNR5.mat';
out_path = '/home/zaur/Documents/Study/vadpy2/output/zaur/tmp.out';
% 
% sound_path = '/home/zaur/Documents/Study/vadpy2/databases/TESTDB/DATA/jamjB.0'; 
% gt_path =    '/home/zaur/Documents/Study/vadpy2/databases/TESTDB/GT/jamjB.0';

% gt_id = fopen(gt_path, 'rb');
% gt_labels = fgetl(gt_id);
% gt_labels = gt_labels - '0';          % a dirty trick to convert a string into vector
% gt_labels = gt_labels';               % turn into column-vector
% 
% for i=2:length(gt_labels) - 2
%     gt_labels(i) = single(round(mean([gt_labels(i-1), gt_labels(i), gt_labels(i+1)])));
% end
% 
% % subplot(2, 1, 1);
% plot_vad(gt_labels, 8000, 0.008);
% hold on; 
% 
% fin_id = fopen(sound_path, 'rb');
% [s, count] = fread(fin_id, 'int16', 'b'); % input signal
% s = s / max(abs(s));
% plot(s);

%vad('entropy', '1', 'b', sound_path, out_path);
vad('entropy', '1', 'l', sound_path, out_path);

%svm ('train', 'b', '0.008', sound_path, gt_path, model_path); 
%svm ('test', 'b', '0.01', sound_path, model_path, gt_path); 
