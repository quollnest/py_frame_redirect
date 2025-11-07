#include "py_frame_redirect.h"

void redirect_frame_3_11(
    void *redirect_src_v,
    void *redirect_targ_v
)
{
    struct Py3_11FrameObj *redirect_src = (Py3_11FrameObj *)redirect_src_v;
    struct Py3_11FrameObj *redirect_targ = (Py3_11FrameObj *)redirect_targ_v;

    // Wrapper frame pointer
    redirect_src->f_back = redirect_targ;
    // Data frame pointer
    redirect_src->f_data->previous = redirect_targ->f_data;
}
