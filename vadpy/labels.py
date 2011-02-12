import math

class Section(object):
    def __init__(self, start, end, voiced, frame_len):
        """Initialize Section object
        
        core     -- EvalCore object
        start    -- Section's start (in seconds)
        end      -- Section's end  (in seconds)
        voiced   -- Boolean VAD decision for the section (True / False)
        score    -- Soft VAD score
        """
        assert end - start >= 0, 'Error creating Section object: ' \
            'Section\'s start stamp is in ' \
            'future relatively to end stamp.\n' \
            'Section start: {0}; end: {1};'.format(start,end)
        self.start = start
        self.end = end
        self.voiced = voiced
        self.compress(frame_len) # sets self.count

    @property
    def duration(self):
        return self.end - self.start
   
    def __str__(self):
        return '{0} - {1} :{2}]'.format(self.start, self.end, self.voiced)

    def compress(self, frame_len):
        self.count = int(round(self.duration / frame_len))        


def extend_sections(element, sections, frame_len):
    """Extend sections list by two additional (first, last) sections if required

    The function adds two sections (at most) to the list, so that sections timestamps cover 
    0 .. file length competely
    """
    if sections:
        sec = sections[0]
        if sec.start != 0:
            if sec.start < frame_len: # just a small glitch, no need to insert a new section
                sec.start = 0
            else:                
                sections.insert(0, Section(0, sec.end, sec.voiced, frame_len))        

        sec = sections[-1]
        if sec.end != element.length:
            if abs(sec.end - element.length) < frame_len:
                sec.end = element.length
            else:
                sections.append(Section(sec.end, element.length, sec.voiced, frame_len))
    return sections

        
class Labels(object):
    """Labels store for GT or VAD labels"""
    def __init__(self, sections, frame_len = None):
        """Initialize Generic Labels object 
        
        sections  -- list of Section objects with GT/VAD labels
        frame_len -- length of every labels frame in seconds
        """
        assert sections, 'At least one section should be supplied to create Labels object'

        self._sections = sections
        self._count = sum(section.count for section in sections) 
        self._labels = []
        self._frame_len = 0
        self.frame_len = frame_len # property
            
    def __str__(self):
        return "Labels object. Sections count: {0}; Frame length: {1}".format(self._count, self._frame_len)
        
    def __len__(self):
        return self._labels and len(self._labels) or self._count

    def __iter__(self):
        return self._labels.__iter__()

    def next(self):
        return self.__next__()

    def __next__(self):        
        self._labels.next() # to be changed for Python3

    def __getitem__(self, index):
        try:
            return self._labels[index]
        except KeyError:
            raise Exception('Cannot return item by index because frame-len has not been set')

    def merge(self):
        """Sections merging by voiced value

        The method merges Sections objects if 
        two consecutive Section objects have same voiced values
        """
        sections = self._sections
        # first check, do we actually need to merge sections?
        merge_required = False
        prev_voiced = sections[0].voiced

        for section in sections[1:]:
            if section.voiced == prev_voiced: # yeap, merge is required
                merge_required = True 
                break;
            else:
                prev_voiced = section.voiced   # no, continue

        # Now merge.. 
        if not merge_required:
            return sections

        merged_sections = []
        prev_section = sections[0]
        prev_voiced = prev_section.voiced

        big_section_start = prev_section.start

        for section in sections[1:]:
            if section.voiced != prev_voiced:
                merged_sections.append(Section(big_section_start, 
                                               prev_section.end,
                                               prev_voiced,
                                               self._frame_len))
                big_section_start = section.start
            prev_section = section
            prev_voiced = section.voiced

        # last section
        merged_sections.append(Section(big_section_start, 
                                       prev_section.end,
                                       prev_voiced,
                                       self._frame_len))
        self._sections = merged_sections

    def compress_sections(self):
        """Frame dimension sections compressing according to frame_len option

        Returns: list of compressed Section objects

        The method is used to sum small sections with section.length < --frame-len
        and replace them with a single Section object
        """
        sections = self._sections
        # 'small' section - section which's len < frame_len
        frame_len = self._frame_len
        ret_sections = []  # list of sections that will be returned
        
        first_small_section = None
        small_sections_total_length = 0  # length is seconds
        small_sections_voiced = 0        # voiced frames counter
        small_sections_unvoiced = 0      # unvoiced frames counter

        for section in sections:
            section.compress(self._frame_len)
            if section.duration < frame_len:    # this is a small section
                if first_small_section:         # there was a small section before current
                    # update counters
                    small_sections_total_length += section.duration
                    small_sections_voiced +=  section.voiced
                    small_sections_unvoiced += (not section.voiced)
               
                if small_sections_total_length > frame_len: # let's create a Section object
                    new_section = Section(first_small_section.start,
                                          section.end,
                                          small_sections_voiced > small_sections_unvoiced, 
                                          self._frame_len)
                    # Reset counters
                    first_small_section = None
                    small_sections_total_length = 0
                    small_sections_voiced = 0
                    small_sections_unvoiced = 0

                    ret_sections.append(new_section)
                else:                       # this is the FIRST small section in current position
                    first_small_section = section

                # update counters
                small_sections_total_length += section.duration
                small_sections_voiced +=  section.voiced
                small_sections_unvoiced += (not section.voiced)
            else:                          # this is not a small section but..
                if first_small_section:     # ..there was a small section before
                    # update counters (!) - multiply current voiced to section.count
                    small_sections_total_length += section.duration
                    small_sections_voiced +=  section.voiced * section.count
                    small_sections_unvoiced += (not section.voiced) * section.count
                    
                    if small_sections_total_length > frame_len: # make a single Section
                        new_section = Section(first_small_section.start,
                                              section.end,
                                              small_sections_voiced > small_sections_unvoiced, 
                                              self._frame_len)
                        # Reset counters
                        first_small_section = None
                        small_sections_total_length = 0
                        small_sections_voiced = 0
                        small_sections_unvoiced = 0

                        ret_sections.append(new_section)
                else:                       # just append this section to the list
                    ret_sections.append(section)
        self._sections = ret_sections


    def create_labels(self):
        labels = []
        sections = self._sections    # section object 'shortcut'
        section = sections[0]        # current iteration gt and vad sections
        start_time = section.start    
        frame_counter = 0            # frame-len based loop counters
        section_id = 0               # sections loop counters

        while(True):
            if frame_counter == section.count: 
                frame_counter = 0
                section_id += 1
                try:
                    section = sections[section_id]                    
                except IndexError:
                    break
            
            labels.append( (start_time, 
                            start_time + self._frame_len, 
                            section.voiced) )
            frame_counter += 1
            start_time += self._frame_len 

        # add last section if necessary (could be required due to small frame-len)
        if abs(start_time - sections[-1].end) >= self._frame_len:
            labels.append((start_time, sections[-1].end, sections[-1].voiced))
        self._labels = labels

    @property
    def sections(self):
        return self._sections
      
    @property 
    def frame_len(self):
        return self._frame_len

    @frame_len.setter
    def frame_len(self, value):
        if value and self._frame_len != value:            
            self._frame_len = value 
            self.merge()
            self.compress_sections()
            self.create_labels()
