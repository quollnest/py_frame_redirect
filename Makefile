CC := gcc
CFLAGS := -Werror -Wvla -Wall -Wno-unused --warn-no-unused-variable -Wunused-result

BASEDIR := src/frame_rop/c_lib
TARGET_NAME := frame_rop.so

#---
# Relative directory setup
#---

SRCDIR := ${BASEDIR}/src
LIBDIR := ${BASEDIR}/lib

TARGET := ${BASEDIR}/${TARGET_NAME}

BUILDDIR := ${BASEDIR}/build

LIBS := -I${LIBDIR}
SRCFILES := $(wildcard ${SRCDIR}/*.c)
OBJFILES := $(patsubst ${SRCDIR}/%.c, ${BUILDDIR}/%.o, ${SRCFILES})

#-----
# Platform specific settings
#-----

# Determine platform based on uname -s
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	PLATFORM := OSX
	CC := clang
else ifeq ($(UNAME_S),Linux)
	PLATFORM := Linux
else
	PLATFORM := UNKNOWN
	$(error Platform $(UNAME_S) is unsupported)
endif

ifeq ($(PLATFORM),OSX)
	SHARED_OBJECT_FLAGS := -shared -Wl,-install_name,${TARGET}
else
	SHARED_OBJECT_FLAGS := -shared -Wl,-soname,${TARGET}
endif


#-----
# Rules
#-----

all: ${TARGET}


${TARGET}: ${OBJFILES}
	${CC} $^ ${CFLAGS} ${SHARED_OBJECT_FLAGS} -o $@ ${LIBS}


${BUILDDIR}/%.o : ${SRCDIR}/%.c | ${BUILDDIR}
	${CC} $^ ${CFLAGS} -c -o $@ ${LIBS}


build: ${BUILDDIR} ${OBJFILES}

clean: 
	rm -rf ${BUILDDIR}
	rm -rf ${TARGET}

${BUILDDIR}:
	mkdir ${BUILDDIR}
