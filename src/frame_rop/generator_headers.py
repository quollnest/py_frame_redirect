'''
    This module defines a class for ease of use when redirecting out of generators
    This distinguishes between return types and redirected objects
'''

import inspect
from typing import TypeVar, Callable

from ctypes import cdll, c_size_t

from .selector import frame_switch
from .redirect import re_enter 

def stop_iteration(obj):
    '''
        Indicates whether a generator should stop iteration
    '''
    return not isinstance(obj, GeneratorYield)

class GeneratorYield:
    '''
        Wrapper object on generator yields
         This is only for type detection to distinguish 
         between redirection and returning
    '''
    def __init__(self, frame, *args, **kwargs):
        '''
            GeneratorYield constructor
            :: frame : frame :: StackFrame object 
            :: *args : args :: Arguments
            :: **kwargs : kwargs :: Keyword Arguments
        '''
        self._frame = frame
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        '''
            Dispatch to get args
        '''
        return self.get_args()

    def get_args(self):
        '''
            Gets saved arguments 
        '''
        return (self._args, self._kwargs)

    def get_return_values(self):
        '''
            Verbose dispatch to get_args
        '''
        return self.get_args()

    def get_frame(self):
        '''
            Getter for the frame
        '''
        return self._frame

    def re_enter(self) -> TypeVar("GeneratorYield") | object:
        '''
            Bound re-entry function for the frame
        '''
        return re_enter(self.get_frame())


def generator_redirect(
    args: list,
    kwargs: dict,
    *,
    target_frame = None) -> GeneratorYield:
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
    return GeneratorYield(src_frame, *args, **kwargs)
