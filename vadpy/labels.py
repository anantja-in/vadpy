import math

class Frame(object):
    def __init__(self, start, end, voiced, frame_len):
        """Initialize Frame object
        
        core     -- EvalCore object
        start    -- Frame's start (in seconds)
        end      -- Frame's end  (in seconds)
        voiced   -- Boolean VAD decision for the frame (True / False)
        score    -- Soft VAD score
        """
        assert end - start >= 0, 'Error creating Frame object: ' \
            'Frame\'s start stamp is in ' \
            'future relatively to end stamp.\n' \
            'A possible reason is incorrect labels\' frame length\n' \
            'Frame start: {0}; end: {1};'.format(start,end)
        self.start = start
        self.end = end
        self.voiced = bool(voiced)
        self.compute_count(frame_len) # sets self.count

    @property
    def duration(self):
        return self.end - self.start
   
    def __str__(self):
        return '{0} - {1} :{2}]'.format(self.start, self.end, self.voiced)

    def compute_count(self, frame_len):
        self.count = int(round(self.duration / frame_len))        

    

def extend_frames(element, frames, frame_len):
    """Extend frames list by two additional (first, last) frames if required

    The function adds two frames (at most) to the list, so that frames timestamps cover 
    0 .. file length competely
    """
    if frames:
        sec = frames[0]
        if sec.start != 0:
            if sec.start < frame_len: # just a small glitch, no need to insert a new frame
                sec.start = 0
            else:                
                frames.insert(0, Frame(0, sec.end, sec.voiced, frame_len))

        sec = frames[-1]
        if element.length:
            if sec.end != element.length:
                if abs(sec.end - element.length) < frame_len:
                    sec.end = element.length
                else:
                    frames.append(Frame(sec.end, element.length, sec.voiced, frame_len))
    else: # No frames, we assume that element is completely unvoiced
        frames = [ Frame(0, element.length, False, frame_len) ]

    return frames

        
class Labels(object):
    """Labels store for GT or VAD labels"""
    def __init__(self, frames, frame_len = None):
        """Initialize Generic Labels object 
        
        frames  -- list of Frame objects with GT/VAD labels
        frame_len -- length of every labels frame in seconds
        """
        assert frames, 'At least one frame should be supplied to create Labels object'

        self._frames = frames
        self._labels = []
        self._frame_len = 0
        self._compute_count()      # compute self._count
        self.frame_len = frame_len # property
            
    def __str__(self):
        return "Labels object. Frames count: {0}; Frame length: {1}".format(self._count, self._frame_len)
        
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

    def _compute_count(self):
        self._count = sum(frame.count for frame in self.frames)

    def merge(self):
        """Frames merging by voiced value

        The method merges Frames objects if 
        two consecutive Frame objects have same voiced values
        """
        frames = self._frames
        # first check, do we actually need to merge frames?
        merge_required = False
        prev_voiced = frames[0].voiced
        for frame in frames[1:]:
            if frame.voiced == prev_voiced: # yeap, merge is required
                merge_required = True 
                break;
            else:
                prev_voiced = frame.voiced   # no, continue

        # Now merge.. 
        if not merge_required:
            return frames

        merged_frames = []
        prev_frame = frames[0]
        prev_voiced = prev_frame.voiced

        big_frame_start = prev_frame.start

        for frame in frames[1:]:
            if frame.voiced != prev_voiced:
                merged_frames.append(Frame(big_frame_start, 
                                               prev_frame.end,
                                               prev_voiced,
                                               self._frame_len))
                big_frame_start = frame.start
            prev_frame = frame
            prev_voiced = frame.voiced

        # last frame
        merged_frames.append(Frame(big_frame_start, 
                                       prev_frame.end,
                                       prev_voiced,
                                       self._frame_len))
        self._frames = merged_frames

    def scale(self):
        """Frame dimension scaling according to frame_len option

        Returns: list of scaled Frame objects

        The method is used to sum small frames with frame.duration < --frame-len
        and replace them with a single Frame object
        """
        frames = self._frames
        # 'small' frame - frame which's len < frame_len
        frame_len = self._frame_len
        ret_frames = []  # list of frames that will be returned
        
        first_small_frame = None
        small_frames_total_length = 0  # length is seconds
        small_frames_voiced = 0        # voiced frames length
        small_frames_unvoiced = 0      # unvoiced frames length

        for frame in frames:
            duration = frame.duration
            frame.compute_count(self._frame_len)
            if duration < frame_len:    # this is a small frame               
                # update counters
                small_frames_total_length += duration
                if frame.voiced:
                    small_frames_voiced +=  duration
                else:
                    small_frames_unvoiced += duration
                
                if small_frames_total_length > frame_len: # let's create a Frame object
                    new_frame = Frame(first_small_frame.start,
                                      frame.end,
                                      small_frames_voiced > small_frames_unvoiced, 
                                      self._frame_len)
                    # Reset counters
                    first_small_frame = None
                    small_frames_total_length = 0
                    small_frames_voiced = 0
                    small_frames_unvoiced = 0

                    ret_frames.append(new_frame)
                elif not first_small_frame:      # this is the FIRST small frame in current section
                    first_small_frame = frame

            else:                         # this is not a small frame but..
                if first_small_frame:     # ..there was a small frame before
                    small_frames_total_length += duration
                    if frame.voiced:
                        small_frames_voiced +=  duration
                    else:
                        small_frames_unvoiced += duration
                                    
                    new_frame = Frame(first_small_frame.start,
                                          frame.end,
                                          small_frames_voiced > small_frames_unvoiced, 
                                          self._frame_len)
                    # Reset counters
                    first_small_frame = None
                    small_frames_total_length = 0
                    small_frames_voiced = 0
                    small_frames_unvoiced = 0

                    ret_frames.append(new_frame)                
                else:                       # just append this frame to the list
                    ret_frames.append(frame)
        self._compute_count()
        self._frames = ret_frames

    def create_labels(self):
        frame_len = self._frame_len
        labels = []
        frame_id = 0
        frame = self.frames[0]

        for i in range(1, len(self)):         
            t_point = i*frame_len            
            while(True):                
                if frame.start <= t_point <= frame.end or abs(frame.start - t_point) < frame_len :
                    labels.append( (t_point, t_point + frame_len, frame.voiced))
                    break                                    
                else:
                    frame_id += 1
                    try:
                        frame = self.frames[frame_id]
                    except IndexError:
                        break
        self._labels = labels        

    @property
    def frames(self):
        return self._frames
      
    @property 
    def frame_len(self):
        return self._frame_len

    @frame_len.setter
    def frame_len(self, value):
        if value and self._frame_len != value:
            self._labels = []
            self._frame_len = value
            self.merge()
            self.scale()
            self.create_labels()


def equalize_framelen(*lo_list):
    """Align labels objects by using minimal frame length and size"""
    if len(set(len(labels) for labels in lo_list)) != 1:
        min_frame_len = min(labels.frame_len for labels in lo_list)
        for labels in lo_list:
            labels.frame_len = min_frame_len
