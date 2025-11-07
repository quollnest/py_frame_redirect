import unittest 
from frame_rop.redirect import redirect, re_enter

import inspect

class SimpleReentrancyTests(unittest.TestCase):

    def test_single_return(self):

        def _foo(value):
            _bar(value)           
            return value
 
        def _bar(value): 
            frame = inspect.currentframe()
            target_frame = frame.f_back.f_back
            redirect(value + 1, target_frame = target_frame)

        val = 5
        frame, cmp, _ = _foo(val) 
        assert cmp[0] == val + 1
        cmp = re_enter(frame)
        assert cmp == val

    def test_hook(self): 

        class CLS:
            def __init__(self):
                self._list = list() 

            def fn(self, it): 
                for i in it:
                    self.append(i)

            def append(self, val):
                self._list.append(val)

        def hook(fn): 
            frame = inspect.currentframe()
            target_frame = frame.f_back
            print(f"Hooking {id(target_frame)}")

            def _wrap(*args, **kwargs):
                print(f"Redirecting {id(target_frame)}")
                vals = redirect(
                    *args, 
                    target_frame=target_frame,
                    **kwargs
                ) 
                print('Resumed', vals)
                return fn(*args, **kwargs)
            return _wrap 

        # Hooked
        frame = inspect.currentframe()
        print(f"Hooking frame: {id(frame)}")

        CLS.append = hook(CLS.append)
        
        x = CLS()
        x.append(5)
        assert 5 not in x._list

        #(frame, arg, kwarg) = x.fn([1, 2, 3])
        #(frame, arg, kwarg) = re_enter(frame) 
        #(frame, arg, kwarg) = re_enter(frame) 
        #re_enter(frame) 
        


if __name__ == '__main__':
    cls = SimpleReentrancyTests()
    cls.test_hook()
