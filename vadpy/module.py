import os
import logging 
import subprocess

from .element import Element
from .error import VADpyError, MissingArgumentError
from .common import listdir
from .options import Option

log = logging.getLogger(__name__)


class ModuleMetaclass(type):
    def __new__(meta, classname, bases, class_dict):
        for item in class_dict:
            val = class_dict[item]
            if type(val) == Option: 
                val.module = classname.lower() # add module's name to option                
                if not val.name:
                    val.name = item

        return type.__new__(meta, classname, bases, class_dict)

    def __str__(cls):
        shelp = 'VADpy module ' + cls.__name__ + '\n' + str(cls.__doc__) + '\n'
        first_option = True
        for attr in dir(cls): 
            objattr = getattr(cls, attr)
            if type(objattr) == Option: # option found
                if first_option:
                    first_option = False
                    shelp += 'Options:\n' + 'Name'.ljust(20) + 'Description\n'
                shelp += objattr.name.ljust(20) + objattr.description + '\n'
        return shelp


class Module(object):
    __metaclass__ = ModuleMetaclass

    description = ''
    author = ''
    version = ''

    def __init__(self, vadpy, options):
        """\param options"""
        self.vadpy = vadpy
        self.settings = vadpy.settings
        self.name = self.__class__.__name__.lower()

        # == setup options == # 
        # get all options defined in class
        for attr in dir(self.__class__): # because we must iterate through all child classes
            objattr = getattr(self.__class__, attr)
            if type(objattr) == Option: # option found
                option = objattr
                name = option.name or attr
                if name in options:
                    setattr(self, attr, option.parse(options[name])) # replace Option object with value
                elif option.default != None:
                    setattr(self, attr, option.parse(option.default))
                else:
                    raise MissingArgumentError(option.module, name)

    def __del__(self):
        pass

    def run(self):
        log.info('Running {0}'.format(self.__class__.__name__))

    

class DBModule(Module):
    root = Option(description = 'Root directory of current database')
    source_dir = Option('source-dir', description = 'Source directory (relatively to root dir)')
    gt_dir = Option('gt-dir', description = 'Ground Truth directory (relatively to root dir)')

    def __init__(self, vadpy, options):
        super(DBModule, self).__init__(vadpy, options)
        self.source_dir = os.path.join(self.root, self.source_dir)
        self.gt_dir = os.path.join(self.root, self.gt_dir)


    def elements_from_dirs(self, source_name, source_dir, gt_dir, flags, *regexps):
        """Create elements by finding data files and corresponding gt files in given directories"""
        elements = []
        source_files = listdir(source_dir, *regexps)
        gt_files = set(listdir(gt_dir, *regexps))

        for source_file in source_files:
            source_file_path = os.path.join(source_dir, source_file)
            if os.path.isdir(source_file_path):
                continue
            if source_file in gt_files:
                elements.append(
                    Element(source_name,
                            source_file_path, 
                            os.path.join(gt_dir, source_file),
                            flags)
                    )                            
            else:
                raise VADpyError('Cannot find a GT file for corresponding source file {0}'.format(source_file))

        return elements


class IOModule(Module):
    action = Option()
    frame_len = Option('frame-len', parse_type = float)

    def __init__(self, vadpy, options):
        super(IOModule, self).__init__(vadpy, options)

    def run(self):
        if self.action == 'write':
            for element in self.vadpy.pipeline:                
                element.gt_data.frame_len = self.frame_len # this is crucial!                

    def read(self, path):
        log.debug(('Reading {0}').format(path))
        pass

    def write(self, data, path):
        log.debug('Writing to {0}'.format(path))
        pass


class VADModule(Module):
    """Base class for all types of VAD modules"""
    # 
    outdir = Option(parse_func = os.path.abspath, 
                    description = 'VAD\'s output directory') 
    outpath = Option(default = '{outdir}/{source}/{filename}',
                     description = 'Output path template: {{outdir}}; {{source}}; {{filename}};')
    # filename corresponds to source_path's filename (template)

    def __init__(self, vadpy, options):
        super(VADModule, self).__init__(vadpy, options)

    def _set_outfile_path(self, element):
        source_dir, source_file = os.path.split(element.source_path)
        element.vad_output_path = self.outpath.format(
            outdir = self.outdir, 
            source = element.source_name, 
            filename = source_file)
        # create directory (recursively)
        vad_output_dir = os.path.dirname(element.vad_output_path)
        if not os.path.exists(vad_output_dir):
            os.makedirs(vad_output_dir)

        
class SimpleVADModuleBase(VADModule):
    """Basic wrapper for VADModule

    SimpleCodecModule is a basic wrapper to standalone VAD executables (e.g. G.729, ARM)
    that require no training and can produce a single VAD output file by processing
    a single input file. 
    """    
    exec_path = Option('exec-path', parse_func = os.path.abspath)

    def __init__(self, vadpy, options):
        super(SimpleVADModule, self).__init__(vadpy, options)
        self._cmd = '{execpath} {vadoptions} {in_path} {out_path}' # command-line to run VAD

    def _get_exec_options(self, element):
        """Return VADModule-specific executable options to use before and after commmand-line arguments"""
        return [], []
      
    def run(self):
        super(SimpleVADModule, self).run() 

        for element in self.vadpy.pipeline:
            self._set_outfile_path(element)
            # execution options list
            options_before_args, options_after_args = self._get_exec_options(element)

            lstrun = [self.exec_path,]
            lstrun.extend(options_before_args)
            lstrun.append(element.source_path)
            lstrun.append(element.vad_output_path)
            lstrun.extend(options_after_args)

            log.debug('Starting the VAD as {0}'.format(lstrun))

            proc = subprocess.Popen(lstrun, 
                                    close_fds = True,
                                    stdin = subprocess.PIPE, 
                                    #stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE, 
                                    )
            stdoutdata, stderrdata = proc.communicate()
            assert not stderrdata, stderrdata



class MatlabVADModuleBase(VADModule):
    """MATLAB-based VADs wrapper for VADModule"""
    bin = Option(description = 'A path to matlab binary')
    mopts = Option(description = 'Matlab options and arguments')
    engine = Option(description = 'A path to VADpy-to-MATLAB engine\'s function name')
    scriptdir = Option(description = 'A directory in which VAD algorithms scripts are located; Matlab working directory')
    filecount = Option(description = 'Amount of files to be passed to Matlab engine at a time', 
                       parse_type = int)

    def __init__(self, vadpy, options):
        super(MatlabVADModuleBase, self).__init__(vadpy, options)
        assert self.filecount > 0, 'Filecount must be > 0'
        self._execargs = {'engine' : self.engine, 
                          '__bracket__' : '"',
                          }

        self._execlist = ['{engine}', 
                          "'{endianness}'", 
                          "'{in_paths}'",
                          "'{out_paths}'",
                          "'{gt_paths}'"
                          ]
    
    def run(self):
        super(MatlabVADModuleBase, self).run()
        pipeline = self.vadpy.pipeline

        self._execlist = ['-r', '{__bracket__}'] + self._execlist + [' {__bracket__}']

        # set internal flags for matlab engine
        endianness = pipeline.flags & LITTLE_ENDIAN and 'l' or 'b'

        self._execargs['endianness'] = endianness
        
        for elements in pipeline.slice(self.filecount):
            for element in elements:
                self._set_outfile_path(element)

            in_paths = ';'.join(elem.source_path for elem in elements)
            gt_paths = ';'.join(elem.gt_path for elem in elements)
            out_paths = ';'.join(elem.vad_output_path for elem in elements)

            self._execargs['in_paths'] = in_paths
            self._execargs['gt_paths'] = gt_paths
            self._execargs['out_paths'] = out_paths
            
            sexec = ' '.join(self._execlist)
            sexec = sexec.format(**self._execargs)

            lstrun = [self.bin, self.mopts, sexec]

            log.debug('Starting MATLAB-based codec:\t {0} {1} {2}'.format(self.bin, self.mopts, sexec))
            
            proc = subprocess.Popen(lstrun, 
                                    cwd = self.scriptdir, 
                                    close_fds = True,
                                    stdin = subprocess.PIPE, 
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE, 
                                    )
            stdoutdata, stderrdata = proc.communicate()
            assert not stderrdata, stderrdata
