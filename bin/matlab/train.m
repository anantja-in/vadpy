function train(train_function, train_arguments, endianness, fread_len, ...
             input_paths, gt_paths, output_paths)
% Usage: vad(train_function, train_arguments, endianness, fread_len, input_paths, gt_paths, output_paths)
%
%
%Parameters:
%train_function	- matlab VAD function to use
%train_arguments  - additional arguments to be passed
%endianness       - files endianness ('b' for BIG ENDIAN; 'l' for LITTLE ENDIAN)
%fread_len        - amount of file (in seconds) to be read at a time
%input_paths      - input file(s') paths separated by ';'
%gt_paths         - corresponding GT paths separated by ';'
%output_paths     - corresponding VAD output's paths separated by ';'

% get paths are strings separated by ';'
input_paths = regexp(input_paths, ';', 'split');
output_paths = regexp(output_paths, ';', 'split');
gt_paths = regexp(gt_paths, ';', 'split');

FS = 8000;

if ~isempty(train_arguments)
    train_arguments = strcat(',', train_arguments);
end

fread_len_frames = str2double(fread_len) * FS;

for i = 1:length(input_paths)
    fin_name = char(input_paths(i));
    fid = fopen(fin_name, 'rb', endianness);
    gt_path = char(gt_paths(i));
	
    [s, count] = fread(fid, fread_len_frames, 'int16'); % input signal           
    seval = strcat('train_', train_function, '(s, FS, gt_path', train_arguments, ')');        
    model = eval(seval);
    
    model_file = strcat(char(output_paths(i)), '.mat');
    save(model_file, 'model');
    
    fclose(fid);
end

exit; % required by VADpy framework to return from matlab process

end % function train

