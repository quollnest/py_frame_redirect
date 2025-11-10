import unittest 
from frame_rop.redirect import redirect, re_enter
from frame_rop.generator_headers import generator_redirect, GeneratorYield, stop_iteration 

import inspect

class GeneratorTests(unittest.TestCase):

    def test_wrapper_function(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            value = bar(value)           
            return value


        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                redirect(
                    args[0] + 1,
                    target_frame = target_frame
                )
                return fn(*args, **kwargs)
            return _wrap

        def _bar(value): 
            return value 

        target_frame = inspect.currentframe()
        val = 5

        bar = wrapper(_bar, target_frame)
        frame, cmp, _ = _foo(bar, val) 
        assert cmp[0] == val + 1
        cmp = re_enter(frame)

        assert cmp == val

    def test_simple_generator_function(self):
        '''
            Tests building redirects with wrappers
        '''
        def foo(bar, value):
            value = bar(value)           
            value = bar(value)           
            value = bar(value)           
            return value

        def bar(value): 
            return value + 1 

        def wrapper(fn, target_frame):
            '''
                Target wrapper function
            '''
            def _wrap(*args, **kwargs):
                generator_redirect(
                    *args,
                    target_frame=target_frame,
                    **kwargs 
                )
                return fn(*args, **kwargs)
            return _wrap

        def foo_generator(fn, value):
            '''
                Redirect generator function
            ''' 
            target_frame = inspect.currentframe()
            _fn = wrapper(fn, target_frame)

            obj = foo(_fn, value)
            while True:
                # Non-generator yield
                if stop_iteration(obj):
                    return 
               
                yield obj.get_args() 
                obj = re_enter(obj.get_frame())
    
        val = 5
        for i in foo_generator(bar, val):
            assert val == i
            val += 1
        


if __name__ == '__main__':
    cl = GeneratorTests()
    cl.test_simple_generator_function()

