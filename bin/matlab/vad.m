function vad(vad_function, vad_arguments, endianness, ...
             input_paths, output_paths)
% Usage: vad(vad_function, vad_arguments, endianness, input_paths, output_paths)
%
%
%Parameters:
%vad_function	- matlab VAD function to use
%vad_arguments  - additional arguments to be passed
%endianness     - files endianness ('b' for BIG ENDIAN; 'l' for LITTLE ENDIAN)
%input_paths    - input file(s') paths separated by ';'
%output_paths   - corresponding VAD output's paths separated by ';'

% get paths are strings separated by ';'
input_paths = regexp(input_paths, ';', 'split');
output_paths = regexp(output_paths, ';', 'split');

FS = 8000;

if length(vad_arguments) > 0
    vad_arguments = strcat(',', vad_arguments);
end

fread_len = 1200; % seconds
fread_len_frames = fread_len * FS; % samples

for i = 1:length(input_paths)
    fin_name = char(input_paths(i));
    fid = fopen(fin_name, 'rb', endianness);

    % output results
    fout_name = char(output_paths(i));
    fido = fopen(fout_name, 'wt'); % opened for appending
    
    while(true)
        [s, count] = fread(fid, fread_len_frames, 'int16'); % input signal

        if count == 0
            break;
        end
        
        % create an 'eval' call
        seval = strcat('vad_', vad_function, '(s, FS', vad_arguments, ')');
        
        hd = eval(seval);
        
		if size(hd, 1) > 1
            hd = hd';
		end        
        
        % output
		if ~isempty(hd)
            fprintf(fido, '%i', hd);
		end
    end

    fclose(fid);
    fclose(fido);
end

exit; % required by VAD.py framework to return from matlab process

end % function vad

