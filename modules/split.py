import io
import os

from vadpy.labels import Section, Labels
from vadpy.module import Module
from vadpy.options import  Option, bool_parser
from vadpy.element import Element, UNDEFINED

import logging 
log = logging.getLogger(__name__)

class ModSplit(Module):
    """Split elements' data and GT labels into one or more elements"""

    outpath = Option(description = 'Optput directory, to which the splitted data should be written. ' \
                         'Module/Path formatting is available.')
    length = Option(parser = int, description = 'The length of every data slice in seconds')
    split_gt = Option('gt', bool_parser, 'Split GT (bool)')

    def __init__(self, vadpy, options):
        super(ModSplit, self).__init__(vadpy, options)

    def run(self):
        super(ModSplit, self).run()
        pipeline = self.vadpy.pipeline
        # make sure that there are similar-by-flags elements in the pipeline
        assert pipeline.is_monotonic(), 'Pipeline contains elements with different flags'
        
        if not len(pipeline): # no need to proceed, if there are no elements in pipeline
            return 

        flags = pipeline[0].flags 
        sections = []
        previous_time_from = 0
        previous_time_to =   0        

        outsource_path = ''
        gt_labels = None    

        # split GT        
        for element in pipeline.slice(slice_size):            
            labels = element.gt_labels
            i = 0
            shift = 0
            # check, that lengths has at most log10(frame_len) signs after decimal period 
            length = round(self.length, int(abs(math.log10(labels.frame_len))))
            if length != self.length:
                log.warning('The split length is: {0}'.format(length))
        
            try: 
                sections = labels[i : i + length] # list of tuples
                section_start = sections[0][0]    # 'start' position of first section in the list
                new_sections = (Section(sec[0] - section_start, 
                                        sec[1] - section_start, 
                                        sec[2], 
                                        labels.frame_len)
                                for sec in sections)
                
                section = Section(i * frame_len,
                                  (i + 1) * frame_len,
                                  decision, 
                                  self.frame_len)
                
                
                section.start += shift
                section.end += shift
                sections.append(section)
            shift += len(element)
        gt_labels = Labels(sections)

        # split data
        outsource_path = self.format_path(self.outpath)
        out_io = io.FileIO(outsource_path, 'w')
        for element in pipeline:
            source_io = io.FileIO(element.source_path)
            out_io.write(source_io.read())
        source_io.close()            
        
        new_elem = Element(self.source_name, outsource_path, '', flags, self.cat_source)
        new_elem.gt_labels = gt_labels
        self.vadpy.pipeline.flush()
        self.vadpy.pipeline.add(new_elem)
