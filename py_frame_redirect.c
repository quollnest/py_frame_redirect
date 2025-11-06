#include "py_frame_redirect.h"

void redirect_frame(void *redirect_src_v, void *redirect_targ_v)
{
    // TODO : is void * required with cdll?
    Py311FrameObj *redirect_src = (Py311FrameObj *)redirect_src_v;
    Py311FrameObj *redirect_targ = (Py311FrameObj *)redirect_targ_v;

    // Wrapper frame pointer
    redirect_src->f_back = redirect_targ;
    // Data frame pointer
    redirect_src->f_data->previous = redirect_targ->f_data;
}
