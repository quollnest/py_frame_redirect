#ifndef PY_FRAME_3_11
#define PY_FRAME_3_11

#include "frame_redirect.h"

struct PyFrame_Data_3_11;

struct PyFrameObj_3_11 {
    PyObjHead obj_h;
    struct PyFrameObj_3_11* f_back;
    struct PyFrameData_3_11* f_data;
    void* f_trace;
    int f_lineno;
    char f_trace_lines;
    char f_trace_opcodes;
    char f_fast_as_locals;
    void* _f_frame_data[1];
};

struct PyFrameData_3_11 {
    void* f_func;
    void* f_globals;
    void* f_builtins;
    void* f_locals;
    void* f_code;
    struct PyFrameObj_3_11* frame_obj;
    struct PyFrameData_3_11* previous;
    void* prev_instr;
    int stacktop;
    bool is_entry;
    char owner;
    void* localsplus[1];
};

// Macro expansion for function header
void redirect_frame_3_11(
        struct PyFrameObj_3_11* redirect_src,
        struct PyFrameObj_3_11* redirect_targ
    );

#endif
