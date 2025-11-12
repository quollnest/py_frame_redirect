import unittest
from frame_rop.redirect import redirect, re_enter
from frame_rop.generator_headers import generator_redirect, GeneratorYield, stop_iteration
from frame_rop.generators import redirect_wrapper_pre, redirect_wrapper_post, redirect_generator, to_generator

import inspect


class GeneratorTests(unittest.TestCase):
    '''
        Test generator constructions
    '''

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

        def bar(value):
            return value

        target_frame = inspect.currentframe()
        val = 5

        _bar = wrapper(bar, target_frame)
        frame, cmp, _ = _foo(_bar, val)
        assert cmp[0] == val + 1
        cmp = re_enter(frame)
        assert cmp == val

    def test_multiple_reentry_function(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            value = bar(value)    
            value = bar(value)          
            value = bar(value)          
            return value

        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                redirect(
                    args[0],
                    target_frame = target_frame
                )
                return fn(*args, **kwargs)
            return _wrap

        def bar(value):
            return value + 1

        target_frame = inspect.currentframe()
        val = 5

        _bar = wrapper(bar, target_frame)
        frame, cmp, _ = _foo(_bar, val)
        assert cmp[0] == val

        frame, cmp, _ = re_enter(frame)
        assert cmp[0] == val + 1

        frame, cmp, _ = re_enter(frame)
        assert cmp[0] == val + 2

        cmp = re_enter(frame)
        assert cmp == val + 3

    def test_generator_redirect(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            value = bar(value)    
            value = bar(value)          
            value = bar(value)          
            return value

        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                generator_redirect(
                    args,
                    {},
                    target_frame = target_frame
                )
                return fn(*args, **kwargs)
            return _wrap

        def bar(value):
            return value + 1

        target_frame = inspect.currentframe()
        val = 5

        _bar = wrapper(bar, target_frame)
        obj = _foo(_bar, val)
        cmp = obj.get_return_values()[0]
        assert cmp[0] == val

        obj = obj.re_enter()
        cmp = obj.get_return_values()[0]
        assert cmp[0] == val + 1

        obj = obj.re_enter()
        cmp = obj.get_return_values()[0]
        assert cmp[0] == val + 2

        obj = obj.re_enter()
        cmp = obj
        assert cmp == val + 3

    def test_simple_generator(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            value = bar(value)    
            value = bar(value)          
            value = bar(value)          
            return value

        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                generator_redirect(
                    args,
                    kwargs, 
                    target_frame = target_frame
                )
                return fn(*args, **kwargs)
            return _wrap

        def bar(value):
            return value + 1

        def simple_foo_generator(val):
            target_frame = inspect.currentframe()

            _bar = wrapper(bar, target_frame)
            obj = _foo(_bar, val)
            cmp = obj.get_return_values()[0]
            yield cmp

            obj = obj.re_enter()
            cmp = obj.get_return_values()[0]
            yield cmp

            obj = obj.re_enter()
            cmp = obj.get_return_values()[0]
            yield cmp

        val = 5
        g = simple_foo_generator(val)
        cmp = next(g)
        assert cmp[0] == val

        cmp = next(g)
        assert cmp[0] == val + 1

        cmp = next(g)
        assert cmp[0] == val + 2

    def test_looping_over_generator(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            value = bar(value)    
            value = bar(value)          
            value = bar(value)          
            return value

        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                generator_redirect(
                    args,
                    kwargs,
                    target_frame = target_frame
                )
                return fn(*args, **kwargs)
            return _wrap

        def bar(value):
            return value + 1

        def simple_foo_generator(val):
            target_frame = inspect.currentframe()

            _bar = wrapper(bar, target_frame)
            obj = _foo(_bar, val)
            cmp = obj.get_return_values()[0]
            yield cmp

            obj = obj.re_enter()
            cmp = obj.get_return_values()[0]
            yield cmp

            obj = obj.re_enter()
            cmp = obj.get_return_values()[0]
            yield cmp

        val = 5
        lst = []
        for cmp in simple_foo_generator(val):
            assert cmp[0] == val
            lst.append(cmp[0])
            val += 1
        assert len(lst) == 3

    def test_looping_within_generator(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            for i in range(value):
                value = bar(value)
            return value

        def wrapper(fn, target_frame):
            def _wrap(*args, **kwargs):
                generator_redirect(
                    args,
                    kwargs,
                    target_frame = target_frame
                )
                return fn(*args, **kwargs)
            return _wrap

        def bar(value):
            return value + 1

        def simple_foo_generator(val):
            target_frame = inspect.currentframe()

            _bar = wrapper(bar, target_frame)
            obj = _foo(_bar, val)

            while not stop_iteration(obj):
                cmp = obj.get_return_values()[0]
                yield cmp
                obj = obj.re_enter()
            return

        val = 5
        lst = []
        for cmp in simple_foo_generator(val):
            assert cmp[0] == val
            lst.append(cmp[0])
            val += 1
        assert len(lst) == val // 2 


    def test_redirect_wrapper_pre(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            for i in range(value):
                value = bar(value)
            return value

        def bar(value):
            return value + 1

        def simple_foo_generator(val):
            target_frame = inspect.currentframe()

            _bar = redirect_wrapper_pre(bar, target_frame)
            obj = _foo(_bar, val)

            while not stop_iteration(obj):
                cmp = obj.get_return_values()[0]
                yield cmp
                obj = obj.re_enter()
            return

        val = 5
        lst = []
        for cmp in simple_foo_generator(val):
            assert cmp[0] == val
            lst.append(cmp[0])
            val += 1

        assert len(lst) == val // 2 


    def test_redirect_wrapper_post(self):
        '''
            Tests building redirects with wrappers
        '''
        def _foo(bar, value):
            for i in range(value):
                value = bar(value)
            return value

        def bar(value):
            return value + 1

        def simple_foo_generator(val):
            target_frame = inspect.currentframe()

            _bar = redirect_wrapper_post(bar, target_frame)
            obj = _foo(_bar, val)

            while not stop_iteration(obj):
                cmp = obj.get_return_values()[0]
                yield cmp
                obj = obj.re_enter()
            return

        val = 5
        lst = []
        for cmp in simple_foo_generator(val):
            val += 1
            assert cmp[0] == val
            lst.append(cmp[0])

        assert len(lst) == val // 2 


    def test_local_to_generator(self):
        '''
            Tests building redirects with wrappers
        '''
        class Tst:
            @staticmethod
            def bar(value):
                return value + 1
           
        def foo(value):
            for i in range(value):
                value = Tst.bar(value)
            return value

        def hooking_function(frame):
            old = Tst.bar
            Tst.bar = redirect_wrapper_pre(old, target_frame=frame)
            return old

        def unhooking_function(obj):
            Tst.bar = obj

        def local_to_generator(
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
           
            obj = invoke_fn(args[0]) 
            while not stop_iteration(obj):
                values = obj.get_return_values()
                yield values
                obj = obj.re_enter() 
            unhooking_fn(unhook_data)
            return

        val = 5
        lst = []
        for cmp in local_to_generator(foo, 
                hooking_function,
                val,
                unhooking_fn=unhooking_function
            ):
            assert cmp[0][0] == val
            lst.append(cmp[0][0])
            val += 1

        assert len(lst) == val // 2 

    def test_to_generator(self):
        '''
            Tests building redirects with wrappers
        '''
        class Tst:
            @staticmethod
            def bar(value):
                return value + 1
           
        def foo(value):
            for i in range(value):
                value = Tst.bar(value)
            return value

        def hooking_function(frame):
            old = Tst.bar
            Tst.bar = redirect_wrapper_pre(old, target_frame=frame)
            return old

        def unhooking_function(obj):
            Tst.bar = obj

        def foo_wrapper(args, kwargs):
            return foo(args[0])

        val = 5
        lst = []
        for cmp in to_generator(
                foo_wrapper, 
                hooking_function,
                val,
                unhooking_fn=unhooking_function
            ):
            assert cmp[0][0] == val
            lst.append(cmp[0][0])
            val += 1

        assert len(lst) == val // 2 

    def test_to_generator_class_method(self):
        '''
            Tests building redirects with wrappers
            This case works on a methodtype of an instance of a class 
        '''
        class Tst:
            def __init__(self):
                self.values = []

            def bar(self, value):
                self.values.append(value)
           
        def foo(value):
            obj = Tst()
            for i in range(value):
                obj.bar(i)
            return

        def hooking_function(frame):
            old = Tst.bar
            Tst.bar = redirect_wrapper_pre(old, target_frame=frame)
            return old

        def unhooking_function(obj):
            Tst.bar = obj

        def foo_wrapper(args, kwargs):
            return foo(args[0])

        val = 5
        lst = []
        for i, cmp in enumerate(to_generator(
                foo_wrapper, 
                hooking_function,
                val,
                unhooking_fn=unhooking_function
            )):
            assert cmp[0][1] == i 
            lst.append(cmp[0][1])

        assert len(lst) == val 


    def test_to_generator_handler_fn(self):
        '''
            Tests building redirects with wrappers
            This case works on a methodtype of an instance of a class 
        '''
        class Tst:
            def __init__(self):
                self.values = []

            def bar(self, value):
                self.values.append(value)
           
        def foo(value):
            obj = Tst()
            for i in range(value):
                obj.bar(i)
            return

        def hooking_function(frame):
            old = Tst.bar
            Tst.bar = redirect_wrapper_pre(old, target_frame=frame)
            return old

        def unhooking_function(obj):
            Tst.bar = obj

        def foo_wrapper(args, kwargs):
            return foo(args[0])
        
        def handler(args):
            return args[0][1]

        val = 5
        lst = []
        for i, cmp in enumerate(to_generator(
                foo_wrapper, 
                hooking_function,
                val,
                unhooking_fn=unhooking_function,
                handler_fn = handler
            )):
            assert cmp == i 
            lst.append(cmp)

        assert len(lst) == val 

if __name__ == '__main__':
    cl = GeneratorTests()
    cl.test_wrapper_function()
    cl.test_multiple_reentry_function()
    cl.test_generator_redirect()
    cl.test_simple_generator()
    cl.test_looping_over_generator()
    cl.test_looping_within_generator()
    cl.test_redirect_wrapper_pre()
    cl.test_redirect_wrapper_post()
    cl.test_to_generator()
    cl.test_to_generator_class_method()
