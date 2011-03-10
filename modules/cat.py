import io
import os

from vadpy.labels import Frame, Labels
from vadpy.module import Module
from vadpy.options import  Option, bool_parser
from vadpy.element import Element, UNDEFINED

import logging 
log = logging.getLogger(__name__)

class ModCat(Module):
    """Concatenates all elements' source data and GT labels into one element

    Additional macros: 
    {srcname} - source-name option's value
    """
    out_source_path = Option('out-source-path',
                             description = 'Optput source file\'s path, to which the concatenated data should be written')
    out_gt_path = Option('out-gt-path',
                         description = 'Optput GT file\'s path')
    source_name = Option('source-name', description = 'New element\'s source name' )
    cat_gt = Option('gt', bool_parser, 'Concatenate GT (yes/no)')
    cat_source = Option('source', bool_parser, 'Concatenate source data (yes/no)')

    def __init__(self, vadpy, options):
        super(ModCat, self).__init__(vadpy, options)
        assert self.cat_gt or self.cat_source, 'Either GT or Source data should be concatenated'

    def run(self):
        super(ModCat, self).run()
        pipeline = self.vadpy.pipeline
        # make sure that there are similar-by-flags elements in the pipeline
        assert pipeline.is_monotonic(), 'Pipeline contains elements with different flags'
        
        if not len(pipeline): # no need to proceed, if there are no elements in pipeline
            return 

        flags = pipeline[0].flags 
        frames = []
        previous_time_from = 0
        previous_time_to =   0        
        shift = 0

        outsource_path = ''
        gt_labels = None
        
        if self.cat_gt: # concatenate gt
            for element in pipeline:
                for frame in element.gt_labels.frames:
                    frame.start += shift
                    frame.end += shift
                    frames.append(frame)
                shift += element.length
            gt_labels = Labels(frames)

        if self.cat_source: # concatenate source
            out_source_path = self.format_path(self.out_source_path)
            out_gt_path = self.format_path(self.out_gt_path)
            out_io = io.FileIO(out_source_path, 'w')
            for element in pipeline:
                source_io = io.FileIO(element.source_path)
                out_io.write(source_io.read())
            source_io.close()            
        
        new_elem = Element(self.source_name, out_source_path, out_gt_path, flags)
        new_elem.gt_labels = gt_labels
        self.vadpy.pipeline.flush()
        self.vadpy.pipeline.add(new_elem)
