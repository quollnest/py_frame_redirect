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

        if not isinstance(ret_args, tuple):
            ret_args_tup = tuple([ret_args])
        else:
            ret_args_tup = ret_args

        generator_redirect(
            ret_args_tup,
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


def __args_wrapper(fn, args, kwargs):
    '''
        Avoids a segfault on frame unwrapping 
    '''
    return fn(*args, **kwargs) 

def to_generator(
    invoke_fn,
    hooking_fn,
    *args,
    unhooking_fn = None,
     **kwargs):
    '''
        :: invoke_fn : callable :: Entrypoint
        :: hooking_fn: callable :: Single argument 
         function comprised of the target stack frame 
         may optinally return arguments for unhooking
        :: unhooking_fn : callable :: Single argument 
         function for unhooking the frame rop 
    '''
    target_frame = inspect.currentframe()
    unhook_data = hooking_fn(target_frame)
   
    obj = invoke_fn(args, kwargs) 
    while not stop_iteration(obj):
        values = obj.get_return_values()
        yield values
        obj = obj.re_enter() 
    return
