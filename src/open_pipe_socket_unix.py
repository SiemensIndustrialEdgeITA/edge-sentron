import io
import struct
import os


class ODK_pipe(io.IOBase):

    def __init__(self, name,outbuffersize=1024,inbuffersize=1024):

        """ An implementation of a file-like Python object pipe on Unix using socket.
        """
        self.name = name # /tmp/HmiRuntime
        self.outbuffersize = outbuffersize
        self.inbuffersize = inbuffersize
        self.length = 1024
        
        # AF_UNIX: process on the same machine
        # SOCK_STREAM: stream oriented socket
        pipe_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        pipe_socket.setblocking(0)

        err = last_value

        # Socket connection 
        try:
            self.fd = pipe_socket.connect(self.name)
            print(sys.stderr, 'Connect to %s' % self.name)
        except socket.error as msg:
            print(sys.stderr, msg)

    def __del__(self):
        raise NotImplementedError

    def __exit__(self):
        self.__del__()

    # Use docstrings, not comments
    def isatty(self):
        """Is the stream interactive (connected to a terminal/tty)?"""
        return False

    def seekable(self):
        return False

    def fileno(self):
        return self.fd

    def seek(self):
        # I think this is clearer than an IOError
        raise NotImplementedError

    def tell(self):
        # as above
        raise NotImplementedError

    def isDataInPipe(self):
        return self.outbuffersize

    def readPipeBuffer(self):
        finished = 0
        try:
            read_value = pipe_socket.recv(self.length)
        except socket.error as msg:
            print(sys.stderr, msg)
            finished = -1
        return read_value.decode()

    def write(self, data):
        pipe_socket.sendall(data.encode())
        return len(self.length)

    def close(self):
        try:
            pipe_socket.close()
        except socket.error as msg:
            print(sys.stderr, msg)
            pass

    def read(self, length=None):
        # Always compare None by identity, not equality
        if length is None:
            length = self.inbuffersize
        resp = read_value = pipe_socket.recv(length)
        return resp.decode()