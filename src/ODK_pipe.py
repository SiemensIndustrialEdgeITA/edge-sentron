import io
import msvcrt as ms # for fd magic
import win32api, win32file, win32pipe
import struct


class ODK_pipe(io.IOBase):

    def __init__(self, name,
                 outbuffersize=1000000,inbuffersize=1000000):
        """ An implementation of a file-like Python object pipe.

        Documentation can be found at
        https://msdn.microsoft.com/en-us/library/windows/desktop/aa365150(v=vs.85).aspx

        """
        self.name = name
        self.outbuffersize = outbuffersize
        self.inbuffersize = inbuffersize
        self.handle = win32file.CreateFile(
            r"\\.\pipe\%s" % name,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None,
        )
        err = win32api.GetLastError()
        self.fd = ms.open_osfhandle(int(self.handle), 0)

        self.flags, self.outbuffersize, self.inbuffersize, self.maxinstances = win32pipe.GetNamedPipeInfo(self.handle)

    def __del__(self):
        try:
            self.write(b'') # try to clear up anyone waiting
        except win32pipe.error: # no one's listening
            pass
        self.close()

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
        try:
            buffer, bytesToRead, result = win32pipe.PeekNamedPipe(self.handle, 1)
            finished = (result == -1)
        except win32api.error:
            finished = 1
        return len(buffer)

    def readPipeBuffer(self):
        finished = 0
        fullDataRead = []

        while 1:
            try:
                buffer, bytesToRead, result = win32pipe.PeekNamedPipe(self.handle, 1)
                # finished = (result == -1)
                if not bytesToRead:
                    break
                hr, data = win32file.ReadFile(self.handle, bytesToRead, None)
                fullDataRead.append(data)
            except win32api.error:
                finished = 1
                break

        dataBuf = ''.join(fullDataRead)
        return dataBuf

    def write(self, data):
        """WriteFileEx impossible due to callback issues."""
        # there is no need to compare the __name__ of the type!
        #data = data + "\r\n"
        if not isinstance(data, bytes):
            data = bytes(data, 'utf-8')
        res = win32file.WriteFile(self.handle, data)
        return len(data)

    def close(self):
        try:
            if self.handle:
                win32file.CloseHandle(self.handle)
            self.handle = 0
        except win32api.error:
            pass

    def read(self, length=None):
        # Always compare None by identity, not equality
        if length is None:
            length = self.inbuffersize
        resp = win32file.ReadFile(self.handle, length)
        if resp[0] != 0:
            raise __builtins__.BrokenPipeError(win32api.FormatMessage(resp[0]))
        else:
            return resp[1]
           
