import io
import os
import sys
import socket
import struct
import traceback
import errno
import fcntl


class ODK_pipe(io.IOBase):

    def __init__(self, name, outbuffersize=1024, inbuffersize=1024):
        """ An implementation of a file-like Python object pipe on Linux using socket.
        """
        self.name = name
        self.outbuffersize = outbuffersize
        self.inbuffersize = inbuffersize
        
        
        # Create socket
        self.file_name = '/tmp/HmiRuntime'
        self.mode = 0o777 # RW permisisons 

        # AF_UNIX: process on the same machine
        # SOCK_STREAM: stream oriented socket
        self.pipe_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
        print(sys.stderr, 'Connecting to %s' % self.file_name)
        
        '''   
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
        '''
        
     
        
        # Socket connection 
        try:
            self.pipe_socket.connect(self.file_name)
            print(sys.stderr, 'Connect to %s' % self.file_name)
        except socket.error as msg:
            print(sys.stderr, msg)
            #sys.exit(1) 
           
                           
        
    def __del__(self):
        try:
            print('del')
            self.pipe_socket.close()
            print(sys.stderr, 'Close connection to %s' % self.file_name)
        except socket.error as msg:
            print(sys.stderr, msg)
            sys.exit(1) 
         
       
    def __exit__(file):
        try:
            pipe_socket.close()
            print(sys.stderr, 'Close connection to %s' % self.file_name)
        except socket.error as msg:
            print(sys.stderr, msg)
            sys.exit(1) 

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

    # Check if there are data into pipe
    def isDataInPipe(self):
        try:
            # Check if buffer is not empty
            # Receive data from the socket.
            data_buffer = self.pipe_socket.recv(1024)
            #print("isDataInPipe dimension: " + str(data_buffer) )
            if data_buffer != 0:
               finished = 1
        except Exception:
           traceback.print_exc() 
        return data_buffer

    def readPipeBuffer(self):
        finished = 0
        fullDataRead = []

        while 1:
            try:
                bytesToRead = 1024
                finished = 0
                if not bytesToRead:
                    break
                # Read pipe  
                data = self.pipe_socket.recv(1024)
                sdata = str(data.decode)
                fullDataRead.append(sdata)
            except Exception:
                traceback.print_exc() 
                break

        dataBuf = sdata
        return dataBuf

    def write(self, data):
        try:
            print("Call write and wait wit data:" + str(data))
            print("Write")
            self.pipe_socket.sendall(data.encode())
        except Exception:
           traceback.print_exc() 
        return len(data)

    def close(self):
        try:
            self.pipe_socket.close()
            self.pipe = 0
        except Exception:
            pass

    def read(self, length=None):
        # Always compare None by identity, not equality
        print("Call read")
        try:
           if length is None:
               length = self.inbuffersize
           length = 1024
           read_value = self.socket_pipe.recv(length)
           reads = read_value.decode()
        except Exception:
           traceback.print_exc() 
           if read_value != 0:
               # TODO ?????
               #raise __builtins__.BrokenPipeError(win32api.FormatMessage(resp[0]))
               print(reads)
               print("Valore letto")
           else:
               return str(reads)
            