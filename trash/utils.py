def bind_function(native, restype, argtypes):
    native.restype = restype
    native.argtypes = argtypes

    return native
