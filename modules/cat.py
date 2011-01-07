import io
import os

from vadpy.data import Section, Data
from vadpy.module import Module
from vadpy.options import  Option

import logging 
log = logging.getLogger(__name__)

class Cat(Module):
    """Concatenates all elements' data and GT into one element"""
    outdir = Option()
    name = Option()
    
    def __init__(self, vadpy, options):
        super(Cat, self).__init__(vadpy, options)

    def run(self):
        super(Cat, self).run()
        sections = []

        previous_time_from = 0
        previous_time_to =   0        
        shift = 0
        
        outdata_path = os.path.join(self.outdir, self.name + '.data')
        outgt_path = os.path.join(self.outdir, self.name + '.gt')

        if os.path.exists(outdata_path): os.remove(outdata_path)
        if os.path.exists(outgt_path): os.remove(outgt_path)
            
        for element in self.vadpy.pipeline:
            # concatenate gt
            for section in element.gt_data._sections:
                section.start += shift
                section.end += shift
            sections.append(element.gt_data._sections)

            shift += element.length

            
            # concatenate data                    
            # out_io = io.FileIO(outdata_path, 'a')
            # data_io = io.FileIO(element.data_path)            
            # out_io.write(data_io.read())
            # data_io.close()
        
        new_elem = Element(self.name, 
                           os.path.getsize(source_file_path) / (fs * (bps / 8.0)),
                           source_file_path, 
                           os.path.join(gt_dir, source_file), 
                           flags)
        
        
