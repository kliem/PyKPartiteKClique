# We define alternatives if cysignals is not present.

from libc.stdlib cimport malloc, calloc, realloc
from libc.stdlib cimport free

cdef extern from *:
    int unlikely(int) nogil  # Defined by Cython

cdef inline int sig_on() except 0:
    return 1

cdef inline void sig_off():
    pass

cdef inline void* check_allocarray(size_t count, size_t eltsize) except? NULL:
    cdef void* ret = malloc(count*eltsize)
    if unlikely(ret == NULL):
        if count*eltsize > 0:
            raise MemoryError("failed to allocate %s * %s bytes" % (count, eltsize))
    return ret

cdef inline void* check_calloc(size_t count, size_t eltsize) except? NULL:
    cdef void* ret = calloc(count, eltsize)
    if unlikely(ret == NULL):
        if count*eltsize > 0:
            raise MemoryError("failed to allocate %s * %s bytes" % (count, eltsize))
    return ret

cdef inline void* check_reallocarray(void* ptr, size_t count, size_t eltsize) except? NULL:
    cdef void* ret = realloc(ptr, count*eltsize)
    if unlikely(ret == NULL):
        if count*eltsize > 0:
            raise MemoryError("failed to allocate %s * %s bytes" % (count, eltsize))
    return ret

cdef inline void* check_malloc(size_t size) except? NULL:
    cdef void* ret = malloc(size)
    if unlikely(ret == NULL):
        if size > 0:
            raise MemoryError("failed to allocate %s bytes" % (size))
    return ret

cdef inline void* check_realloc(void* ptr, size_t size) except? NULL:
    cdef void* ret = realloc(ptr, size)
    if unlikely(ret == NULL):
        if size > 0:
            raise MemoryError("failed to allocate %s bytes" % (size))
    return ret

cdef inline void sig_free(void* ptr) nogil:
    free(ptr)
