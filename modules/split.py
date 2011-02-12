import io
import os
import math

from vadpy import common
from vadpy.labels import Section, Labels
from vadpy.module import Module
from vadpy.options import  Option, bool_parser
from vadpy.element import Element, UNDEFINED

import logging 
log = logging.getLogger(__name__)

class ModSplit(Module):
    """Split elements' data and GT labels into one or more elements
    
    Additional formatting arguments:
    {{counter}} - 1,2...length counter for splitted files 
                  Counter should be used, as long as you don't want to overwrite the same file.'
    """

    outpath = Option(description = 'Optput directory, to which the splitted data should be written. ' \
                         'Module/Path formatting is available.')
    length = Option(parser = int, description = 'The length of every data slice in seconds')
    split_gt = Option('gt', bool_parser, 'Split GT (bool)')
    split_source = Option('source', bool_parser, 'Split source data (bool)')

    def __init__(self, vadpy, options):
        super(ModSplit, self).__init__(vadpy, options)
        assert self.split_gt or self.split_source, 'Either GT or Source data should be splitted'

    def run(self):
        super(ModSplit, self).run()
        pipeline = self.vadpy.pipeline
        
        if not len(pipeline): # no need to proceed, if there are no elements in pipeline
            return 

        new_elements = []
        for element in pipeline:
            length = self.length
            slices_count = 0

            if self.split_gt:
                labels = element.gt_labels
                slices_count = int(len(labels) * labels.frame_len / length + 1)
                # create dummy elements
                split_elements = [Element(element.source_name, flags = element.flags) 
                                  for i in range(0, slices_count)]

                sections_slice_count = int(round(length / labels.frame_len))
                for i in range(0, slices_count):
                    # a list of (start, end, decision) tuples
                    sections = labels[i * sections_slice_count : 
                                      min((i + 1) * sections_slice_count, len(labels))]

                    # 'start' position of first section in the list
                    section_start = sections[0][0]   
                    new_sections = [Section(sec[0] - section_start, 
                                            sec[1] - section_start, 
                                            sec[2], 
                                            labels.frame_len)
                                    for sec in sections]
                    split_elements[i].gt_labels = Labels(new_sections, labels.frame_len)
                    
            if self.split_source:
                if not slices_count: #  not self.split_gt
                    slices_count = (os.path.getsize(element.source_path) /
                                    (self.length * element.fs * element.bps / 8.0))
                    slices_count = int(round(slices_count) + \
                                       (slices_count - int(slices_count) <= 0.5 and 1 or 0))
                    split_elements = [Element(element.source_name) 
                                      for i in range(0, slices_count)]

                source_io = io.FileIO(element.source_path)
                for i in range(0, slices_count):
                    outsource_path = self.format_path(self.outpath, 
                                                      counter = i, 
                                                      **element.format_args)
                    common.makedirs( os.path.dirname(outsource_path) )
                    out_io = io.FileIO(outsource_path, 'w')
                    out_io.write(source_io.read(length*element.fs * element.bps / 8))
                    split_elements[i].source_path = outsource_path
                    out_io.close()
                source_io.close()

            new_elements.extend(split_elements)
        self.vadpy.pipeline.flush()
        self.vadpy.pipeline.add(*new_elements)


        
