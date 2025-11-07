#ifndef PY_FRAME_MACRO_EXPANSION
#define PY_FRAME_MACRO_EXPANSION

#define REDIRECT_HEADER(VERSION) ( \
    void redirect_frame_VERSION( \
        struct PyFrameObj_VERSION* redirect_src, \
        struct PyFrameObj_VERSION* redirect_targ \
    ) \
)

#define REDIRECT_BODY(VERSION) \
void redirect_frame_VERSION( \
    struct PyFrameObj_VERSION* redirect_src, \
    struct PyFrameObj_VERSION* redirect_targ \
) \
{ \
 \
    /* Wrapper frame pointer */ \
    redirect_src->f_back = redirect_targ; \
    /* Data frame pointer */ \
    redirect_src->f_data->previous = redirect_targ->f_data; \
} 

#endif
