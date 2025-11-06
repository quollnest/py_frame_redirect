/*
    Provides a single Python-exposed function for redirecting the call stack.
    Can be used for all kinds of frame-re-entry schenanigans, such as;
        - Spinning your own generator-style system
        - Patching over the control flow of someone else's (potentially somewhat
          blackboxed or unknown) Python code
        - Combining the above two to patch a reductive blackbox into a generator over
          the components being reduced

    Note that this code is inherently unstable, as it uses internal details of CPython's
    call stack. Version updates can and will break this. Relatedlty, it is compatible
    only with GIL-enabled CPython.
 */

#ifndef PY_FRAME_REDIRECT_H
#define PY_FRAME_REDIRECT_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct Py311FrameObj Py311FrameObj;
typedef struct Py311FrameData Py311FrameData;

typedef struct Py313FrameObj Py313FrameObj;
typedef struct Py313FrameData Py313FrameData;

// Alignment equivalent PyObject_HEAD
typedef struct PyObjHead {
    size_t ref_count;
    void *type_info;
} PyObjHead;


struct Py311FrameObj {
    PyObjHead obj_h;
    Py311FrameObj *f_back;
    Py311FrameData *f_data;
    void *f_trace;
    int f_lineno;
    char f_trace_lines;
    char f_trace_opcodes;
    char f_fast_as_locals;
    void *_f_frame_data[1];
};

struct Py311FrameData {
    void *f_func;
    void *f_globals;
    void *f_builtins;
    void *f_locals;
    void *f_code;
    Py311FrameObj *frame_obj;
    Py311FrameData *previous;
    void *prev_instr;
    int stacktop;
    bool is_entry;
    char owner;
    void *localsplus[1];
};


struct Py313FrameObj {
    // TODO
};

struct Py313FrameData {
    // TODO
};



/*
    Given two PyFrameWrapper pointers, this rewrites the return address for the first
    PyFrameWrapper to be the second

    IN:
        redirect_src [PyFrameWrapper *] @VOIDED
            A stack frame to redirect. This redirection will change where the frame
            returns to

        redirect_targ [PyFrameWrapper *] @VOIDED
            A stack frame to redirect into. This redirection will result in re-entry
            into this frame

    OUT: N/A
 */
void redirect_frame(void *redirect_src_v, void *redirect_targ_v);
#endif
