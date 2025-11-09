import unittest 
from frame_rop.redirect import redirect, re_enter

import inspect
from functools import partial

class ClassReentrancyTests(unittest.TestCase):

    def test_class_wrap(self):
        '''
            Tests wrapping methodtypes
        '''
        class DummyList:
            def __init__(self):
                self.lst = []

            def append(self, obj):
                self.lst.append(obj)



        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                redirect(args, target_frame = target_frame)
                return fn(*args, **kwargs)
            return _wrap


        target_frame = inspect.currentframe()

        apnd = wrapper(DummyList.append, target_frame)
        obj = DummyList()
        val = 5

        frame, cmp, _ = apnd(obj, val) 
        assert cmp[0][1] == val
        cmp = re_enter(frame)

        assert cmp == None 
        assert val in obj.lst

    def test_class_bind(self):
        '''
            Tests binding to class objects 
        '''
        class DummyList:
            def __init__(self):
                self.lst = []

            def append(self, obj):
                self.lst.append(obj)



        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                redirect(args, target_frame = target_frame)
                return fn(*args, **kwargs)
            return _wrap


        target_frame = inspect.currentframe()

        apnd = wrapper(DummyList.append, target_frame)

        old_apnd = DummyList.append
        DummyList.append = apnd


        obj = DummyList()
        val = 5

        frame, cmp, _ = DummyList.append(obj, val) 
        assert cmp[0][1] == val
        cmp = re_enter(frame)

        assert cmp == None 
        assert val in obj.lst

if __name__ == '__main__':
    unittest.main()
