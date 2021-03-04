# distutils: language = c++
# distutils: extra_compile_args= -std=c++11

# We try to import the following functions from cysignals.
# If not present, we will define alternatives, that obviously lack functionality (in particual keyboard interrupt).

cdef void* check_allocarray(size_t, size_t) except? NULL
cdef void* check_reallocarray(void*, size_t, size_t) except? NULL
cdef void* check_malloc(size_t) except? NULL
cdef void* check_calloc(size_t, size_t) except? NULL
cdef void* check_realloc(void*, size_t) except? NULL
cdef void sig_free(void* ptr) nogil
cdef int sig_on() except 0
cdef void sig_off()
