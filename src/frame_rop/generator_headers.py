'''
    This module defines a class for ease of use when redirecting out of generators
    This distinguishes between return types and redirected objects
'''
import inspect
from ctypes import cdll, c_size_t

from .selector import frame_switch

def stop_iteration(obj):
    '''
        Indicates whether a generator should stop iteration
    '''
    return not isinstance(obj, GeneratorYield)

class GeneratorYield:
    def __init__(self, frame, *args, **kwargs):
        self._frame = frame
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        return self._args, self._kwargs

    def get_args(self):
        return self._args, self._kwargs

    def get_frame(self):
        return self._frame


def generator_redirect(*args, target_frame = None, **kwargs):
    '''
        Redirect jumps back up the stack to a currently executing frame
        This requires a guarantee that the frames that are skipped are eventually returned  
        Uses a GeneratorYield object
    '''

    curr_frame = inspect.currentframe()

    if target_frame is None:
        target_frame = curr_frame.f_back.f_back

    src_frame = curr_frame.f_back

    frame_switch(
        c_size_t(id(curr_frame)),
        c_size_t(id(target_frame))
    )
    return GeneratorYield(src_frame, args, kwargs)
