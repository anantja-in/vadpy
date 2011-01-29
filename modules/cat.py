import io
import os

from vadpy.labels import Section, Labels
from vadpy.module import Module
from vadpy.options import  Option
from vadpy.element import Element, UNDEFINED

import logging 
log = logging.getLogger(__name__)

class Cat(Module):
    """Concatenates all elements' data and GT into one element"""
    outdir = Option(description = 'Optput directory, to which the concatenated data should be written')
    name = Option(description = 'New element\'s name' )
    cat_gt = Option('gt', 'Concatenate GT', bool, default = True)
    cat_data = Option('data', 'Concatenate data', bool, default = True)

    def __init__(self, vadpy, options):
        super(Cat, self).__init__(vadpy, options)

    def run(self):
        super(Cat, self).run()
        pipeline = self.vadpy.pipeline
        # make sure that there are similar-by-flags elements in the pipeline
        assert pipeline.is_monotonic(), 'Pipeline contains elements with different flags'
        
        if not len(pipeline): # no need to proceed, if there are no elements in pipeline
            return 

        flags = pipeline[0].flags 
        sections = []
        previous_time_from = 0
        previous_time_to =   0        
        shift = 0

        outdata_path = os.path.join(self.outdir, self.name + '.data')
        outgt_path = os.path.join(self.outdir, self.name + '.gt')

        if self.cat_gt: # concatenate gt
            for element in pipeline:
                for section in element.gt_labels.sections:
                    section.start += shift
                    section.end += shift
                    sections.append(section)
                shift += element.length

        if self.cat_data: # concatenate data
            out_io = io.FileIO(outdata_path, 'w')
            for element in pipeline:
                data_io = io.FileIO(element.source_path)
                out_io.write(data_io.read())
            data_io.close()            

        new_elem = Element(self.name,             
                           outdata_path, 
                           outgt_path, 
                           flags)

        new_elem.gt_labels = Labels(sections)

        self.vadpy.pipeline.flush()
        self.vadpy.pipeline.add(new_elem)
