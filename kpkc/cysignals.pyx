cimport cysignals.signals
cimport cysignals.memory

cdef inline void* check_allocarray(size_t count, size_t eltsize) except? NULL:
    return cysignals.memory.check_allocarray(count, eltsize)

cdef inline void* check_reallocarray(void* ptr, size_t count, size_t eltsize) except? NULL:
    return cysignals.memory.check_reallocarray(ptr, count, eltsize)

cdef inline void* check_calloc(size_t count, size_t eltsize) except? NULL:
    return cysignals.memory.check_calloc(count, eltsize)

cdef inline void* check_malloc(size_t size) except? NULL:
    return cysignals.memory.check_malloc(size)

cdef inline void* check_realloc(void* ptr, size_t size) except? NULL:
    return cysignals.memory.check_realloc(ptr, size)

cdef inline void sig_free(void* ptr) nogil:
    cysignals.memory.sig_free(ptr)

cdef inline int sig_on() except 0:
    return cysignals.signals.sig_on()

cdef inline void sig_off():
    cysignals.signals.sig_off()
