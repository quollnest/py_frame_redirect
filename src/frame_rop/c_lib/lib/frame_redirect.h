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

// Alignment equivalent PyObject_HEAD
typedef struct PyObjHead {
    size_t ref_count;
    void *type_info;
} PyObjHead;

#include "macro_expansion.h"

#include "frame_3_11.h"
#include "frame_3_13.h"


/*
    Given two PyFrameWrapper pointers, this rewrites the return address for the first
    PyFrameWrapper to be the second

    IN:
        redirect_src 
            A stack frame to redirect. This redirection will change where the frame
            returns to

        redirect_targ
            A stack frame to redirect into. This redirection will result in re-entry
            into this frame

    OUT: N/A

    Acts in place and modifies the contents of the src stack frame 
 */
// void redirect_frame(void* redirect_src, void* redirect_targ);


#endif
