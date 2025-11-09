import inspect
from ctypes import cdll, c_size_t

from .selector import frame_switch

def redirect(*args, target_frame = None, **kwargs):
    '''
        Redirect jumps back up the stack to a currently executing frame
        This requires a guarantee that the frames that are skipped are eventually returned  
    '''

    curr_frame = inspect.currentframe()

    if target_frame is None:
        target_frame = curr_frame.f_back.f_back

    src_frame = curr_frame.f_back

    print(f"Switching, {target_frame}, {id(target_frame)}")
    print("ROP Switchout:", id(curr_frame.f_back))

    frame_switch(
        c_size_t(id(curr_frame)),
        c_size_t(id(target_frame))
    )
    #print("ROP Target:", id(curr_frame.f_back))

    return (src_frame, args, kwargs)


def re_enter(frame):
    '''
        Re-enter returns control flow 
    '''
    curr_frame = inspect.currentframe()
    frame_switch(
        c_size_t(id(curr_frame)),
        c_size_t(id(frame))
    )
