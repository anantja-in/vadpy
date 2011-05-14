import io
import os
import math

from vadpy import common
from vadpy.labels import Frame, Labels
from vadpy.module import Module
from vadpy.options import  Option, bool_parser
from vadpy.element import Element, UNDEFINED

import logging 
log = logging.getLogger(__name__)

class ModSplit(Module):
    """Split elements' data and GT labels into one or more elements
    
    Additional formatting macros:
    {counter} - 1,2...length counter for splitted files 
                Counter should be used, as long as you don't want to overwrite the same file.'
    """

    out_source_path = Option('out-source-path', 
                             description = 'Optput files\' paths, to which the splitted data should be written')
    out_gt_path = Option('out-gt-path', description = 'Optput GT files\' path')
    length = Option(parser = int, description = 'The length of every data slice in seconds')
    split_gt = Option('gt', bool_parser, 'Split GT (yes/no)')
    split_source = Option('source', bool_parser, 'Split source data (yes/no)')
    overwrite = Option(parser = bool_parser, description = 'Overwrite splitted source data (yes/no)')

    def __init__(self, vadpy, options):
        super(ModSplit, self).__init__(vadpy, options)
        assert self.split_gt or self.split_source, 'Either GT or Source data should be splitted'

    def run(self):
        super(ModSplit, self).run()
        pipeline = self.vadpy.pipeline
        
        new_elements = []
        for element in pipeline:
            slices_count = self._get_slices_count(element)
            # create dummy elements
            split_elements = [Element(element.source_name, flags = element.flags) 
                              for i in range(0, slices_count)]

            if self.split_gt:
                labels = element.gt_labels                   
                frames_slice_count = int(round(self.length / labels.frame_len))
                for i in range(0, slices_count):
                    # a list of (start, end, decision) tuples
                    frames = labels[i * frames_slice_count : 
                                      min((i + 1) * frames_slice_count, len(labels))]

                    # 'start' position of first frame in the list
                    frame_start = frames[0][0]   
                    new_frames = [Frame(sec[0] - frame_start, 
                                            sec[1] - frame_start, 
                                            sec[2], 
                                            labels.frame_len)
                                    for sec in frames]
                    path = self.format_path(self.out_gt_path, 
                                            counter = i, 
                                            **element.format_args)
                    split_elements[i].gt_labels = Labels(new_frames, labels.frame_len)
                    split_elements[i].gt_path = path
                    
            if self.split_source:
                source_io = io.FileIO(element.source_path)
                for i in range(0, slices_count):
                    path = self.format_path(self.out_source_path, 
                                            counter = i, 
                                            **element.format_args)
                    split_elements[i].source_path = path
                    if os.path.exists(path) and not self.overwrite:
                        log.debug('File already exists: {0}'.format(path))
                        continue

                    common.makedirs(os.path.dirname(path))
                    out_io = io.FileIO(path, 'w')
                    log.debug('Writing to {0}'.format(path))
                    out_io.write(source_io.read(self.length * element.fs * element.bps / 8))
                    out_io.close()

                source_io.close()

            new_elements.extend(split_elements)
        self.vadpy.pipeline.flush()
        self.vadpy.pipeline.add(*new_elements)        


    def _get_slices_count(self, element):
        """Get an exact amount of slices (new elements count)"""
        if self.split_source:
            # file size is available
            slices_count = (os.path.getsize(element.source_path) /
                            (self.length * element.fs * element.bps / 8.0))
            return int(round(slices_count) + \
                       (slices_count - int(slices_count) <= 0.5 and 1 or 0))
        else:
            # only gt_labels are available
            return int(len(element.gt_labels) * element.gt_labels.frame_len / self.length + 1)


