#include "frame_3_11.h"

void redirect_frame_3_11(
    struct PyFrameObj_3_11* redirect_src,
    struct PyFrameObj_3_11* redirect_targ
)
{
    /* Wrapper frame pointer */
    redirect_src->f_back = redirect_targ;
    /* Data frame pointer */
    redirect_src->f_data->previous = redirect_targ->f_data;
} 


