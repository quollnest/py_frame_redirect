from ctypes import cdll, c_size_t
import inspect

lib_redirect = cdll.LoadLibrary("./py_frame_redirect.so")

def redirect():
    self_frame = inspect.currentframe()
    src_frame = self_frame.f_back
    targ_frame = self_frame.f_back.f_back

    lib_redirect.redirect_frame(c_size_t(id(self_frame)), c_size_t(id(targ_frame)))
    return (src_frame, 12)

def reenter(frame):
    self_frame = inspect.currentframe()
    lib_redirect.redirect_frame(c_size_t(id(self_frame)), c_size_t(id(frame)))
