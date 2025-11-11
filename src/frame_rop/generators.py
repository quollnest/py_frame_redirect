'''
    Some useful defaults for constructing
    generators
'''

import inspect
from typing import Callable

from .generator_headers import GeneratorYield, generator_redirect, stop_iteration

def redirect_wrapper_pre(fn: Callable, target_frame: "frame" = None):
    '''
        Target wrapper function
        :: fn : Callable :: Target Callable function
        :: target_frame : frame :: Target stack frame 
        Returns a wrapper function over the target callable
        This injects an indirection before calling the function
    '''
    if target_frame is None:
        target_frame = inspect.currentframe().f_back

    def _wrap(*args, **kwargs):
        # Cannot perform list expansion here or 
        # the caller breaks in python 3.11 
        generator_redirect(
            args,
            kwargs,
            target_frame = target_frame
        )
        return fn(*args, **kwargs)
    return _wrap

def redirect_wrapper_post(fn: Callable, target_frame: "frame" = None):
    '''
        Target wrapper function
        :: fn : Callable :: Target Callable function
        :: target_frame : frame :: Target stack frame 
        Returns a wrapper function over the target callable
        This injects an indirection after calling the function
    '''
    if target_frame is None:
        target_frame = inspect.currentframe().f_back

    def _wrap(*args, **kwargs):
        ret_args = fn(*args, **kwargs)
        generator_redirect(
            ret_args,
            {},
            target_frame=target_frame,
        )
        return ret_args 
    return _wrap



def redirect_generator(fn, *args, **kwargs):
    '''
        Redirect generator function
    ''' 
    obj = fn(*args, **kwargs)
    while True:
        # Non-generator yield
        if stop_iteration(obj):
            return
        
        # Yield collected values 
        yield obj.get_return_values() 

        # Re-enter the function 
        obj = obj.re_enter()

