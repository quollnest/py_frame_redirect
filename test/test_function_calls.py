import unittest 
from frame_rop.redirect import redirect, re_enter

import inspect
from functools import partial

glb_target_frame = None

class SimpleReentrancyTests(unittest.TestCase):

    def test_single_return(self):

        def _foo(value):
            value = _bar(value)           
            return value
 
        def _bar(value): 
            frame = inspect.currentframe()
            target_frame = frame.f_back.f_back
            redirect(value + 1, target_frame = target_frame)
            return value 

        val = 5
        frame, cmp, _ = _foo(val) 
        assert cmp[0] == val + 1
        cmp = re_enter(frame)

        assert cmp == val
   

    def test_global_frame(self):
        global glb_target_frame
        glb_target_frame = inspect.currentframe()

        def _foo(value):
            value = _bar(value)           
            return value

        def _bar(value): 
            global gbl_target_frame
            redirect(value + 1, target_frame = glb_target_frame)
            return value 

        val = 5
        frame, cmp, _ = _foo(val) 
        assert cmp[0] == val + 1
        cmp = re_enter(frame)

        assert cmp == val


    def test_passing_frame(self):
        '''
            Tests passing the frame down
        '''
        target_frame = inspect.currentframe()

        def _foo(bar, frame, value):
            value = bar(frame, value)           
            return value

        def _bar(target_frame, value): 
            redirect(value + 1, target_frame = target_frame)
            return value 

        val = 5
        frame, cmp, _ = _foo(_bar, target_frame, val) 
        assert cmp[0] == val + 1
        cmp = re_enter(frame)

        assert cmp == val


    def test_partial(self):
        '''
            Tests constructing partial functions
        '''
        def _foo(bar, value):
            value = bar(value)           
            return value

        def _bar(target_frame, value): 
            redirect(value + 1, target_frame = target_frame)
            return value 

        target_frame = inspect.currentframe()
        val = 5

        bar = partial(_bar, target_frame)
        frame, cmp, _ = _foo(bar, val) 
        assert cmp[0] == val + 1
        cmp = re_enter(frame)

        assert cmp == val


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

if __name__ == '__main__':
    cls = SimpleReentrancyTests()
    #cls.test_single_return()
    cls.test_hook()
