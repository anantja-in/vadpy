import io
import os

from vadpy.labels import Section, Labels
from vadpy.module import Module
from vadpy.options import  Option, bool_parser
from vadpy.element import Element, UNDEFINED

import logging 
log = logging.getLogger(__name__)

class ModCat(Module):
    """Concatenates all elements' source data and GT labels into one element

    "outpath" option formatting fields:
    {root etc.}      - Module/Settings formatting arguments
    """
    outpath = Option(description = 'Optput directory, to which the concatenated data should be written. Module/Path formatting is available.')
    name = Option(description = 'New element\'s name' )
    cat_gt = Option('gt', bool_parser, 'Concatenate GT')
    cat_source = Option('source', bool_parser, 'Concatenate source data')

    def __init__(self, vadpy, options):
        super(ModCat, self).__init__(vadpy, options)

    def run(self):
        super(ModCat, self).run()
        pipeline = self.vadpy.pipeline
        # make sure that there are similar-by-flags elements in the pipeline
        assert pipeline.monotonic, 'Pipeline contains elements with different flags'
        
        if not len(pipeline): # no need to proceed, if there are no elements in pipeline
            return 

        flags = pipeline[0].flags 
        sections = []
        previous_time_from = 0
        previous_time_to =   0        
        shift = 0

        outsource_path = os.path.abspath(self.outpath.format(**self.format_args))

        if self.cat_gt: # concatenate gt
            for element in pipeline:
                for section in element.gt_labels.sections:
                    section.start += shift
                    section.end += shift
                    sections.append(section)
                shift += element.length

        if self.cat_source: # concatenate source
            out_io = io.FileIO(outsource_path, 'w')
            for element in pipeline:
                source_io = io.FileIO(element.source_path)
                out_io.write(source_io.read())
            source_io.close()            

        new_elem = Element(self.name,             
                           outsource_path, 
                           '',
                           flags)
        new_elem.gt_labels = Labels(sections)
        self.vadpy.pipeline.flush()
        self.vadpy.pipeline.add(new_elem)
