import ctypes

from trash.utils import bind_function


class TDJson:
    def __init__(self, lib_path, on_error):
        lib = ctypes.CDLL(lib_path)
        self.__bind(lib)
        self.__link_error_callback(lib, on_error)

        self.__client_id = self.__create_client_id()

    def __bind(self, lib):
        self.__create_client_id = bind_function(
            lib.td_create_client_id, ctypes.c_int, []
        )
        self.receive = bind_function(
            lib.td_receive, ctypes.c_char_p, [ctypes.c_double]
        )
        self.send = bind_function(
            lib.td_send, None, [ctypes.c_int, ctypes.c_char_p]
        )
        self.execute = bind_function(
            lib.td_execute, ctypes.c_char_p, [ctypes.c_char_p]
        )

    @staticmethod
    def __link_error_callback(lib, on_error):
        if not on_error:
            return

        callback_type = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

        set_callback = lib.td_set_log_fatal_error_callback
        set_callback.restype = None
        set_callback.argtypes = [callback_type]

        set_callback(
            callback_type(on_error)
        )
