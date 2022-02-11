import io
import os
import sys
import struct
import traceback
import errno


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
        # Create pipe
        self.file_name = "/tmp/HmiRuntime"
        self.mode = 0o777 # RW permisison
        self.pipe = 0
       
        
        try:
             # File FIFO (named pipe) creation if doesn't exist
             os.mkfifo(self.file_name, self.mode)   
        except OSError as oe: 
            if oe.errno != errno.EEXIST:
               raise
            elif(oe.errno == errno.EEXIST):
               # Open connection
               # self.pipe = os.open(self.file_name, os.O_RDWR|os.O_CREAT) 
               print("Pipe created")
                           
        
    def __del__(self):
        try:
            os.write(self.pipe, ''.encode())
        except Exception as e:
           print(e.args[1]) 
        os.close(self.pipe)

    def __exit__(file):
        os.remove(file)

    # Use docstrings, not comments
    def isatty(self):
        """Is the stream interactive (connected to a terminal/tty)?"""
        return False

    def seekable(self):
        return False

    def fileno(self):
        # return self.fd
        raise NotImplementedError

    def seek(self):
        # I think this is clearer than an IOError
        raise NotImplementedError

    def tell(self):
        # as above
        raise NotImplementedError

    def isDataInPipe(self):
        try:
            # Check if buffer is not empty
            self.pipe = os.open(self.file_name, os.O_RDWR|os.O_CREAT)
            data_buffer = sys.getsizeof(self.pipe)
            print("isDataInPipe dimension: " + str(data_buffer) )
            if data_buffer != 0:
               finished = 1
            os.close(self.pipe)
        except Exception:
           traceback.print_exc() 
        return data_buffer

    def readPipeBuffer(self):
        finished = 0
        fullDataRead = []

        while 1:
            try:
                self.pipe = os.open(self.file_name, os.O_RDWR|os.O_CREAT)
                bytesToRead = sys.getsizeof(self.pipe)
                finished = 0
                if not bytesToRead:
                    break
                # Read pipe  
                data = os.read(self.pipe,bytesToRead)  
                fullDataRead.append(data)
                os.close(self.pipe)
            except Exception:
                traceback.print_exc() 
                break

        dataBuf = ''.join(fullDataRead)
        return dataBuf

    def write(self, data):
    
            print("Call write and wait wit data:" + str(data))
            self.pipe = os.open(self.file_name, os.O_RDWR|os.O_CREAT)
            print("Scrivo")
            # write_value = (data)
            if not isinstance(data, bytes):
               write_value = bytes(data, 'utf-8')
            os.write(self.pipe,write_value)
            print(write_value)
            print(len(write_value))
            os.close(self.pipe)
            return len(data)

    def close(self):
        try:
            if self.handle:
                os.close(self.pipe)
            self.pipe = 0
        except Exception:
            pass

    def read(self, length=None):
        # Always compare None by identity, not equality
        print("Call read")
        os.open(self.file_name, os.O_RDWR|os.O_CREAT)
        if length is None:
            length = self.inbuffersize
        length = sys.getsizeof(self.pipe)
        read_value = os.read(self.pipe, length)
        print(read_value)
        if read_value != 0:
            # TODO ?????
            #raise __builtins__.BrokenPipeError(win32api.FormatMessage(resp[0]))
            print(read_value.decode())
            print("Valore letto")
        else:
            return str(read_value)
            
