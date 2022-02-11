import io
from ODK_pipe_Linux import ODK_pipe
from Tags import Tag
from Tags import TagSet
from threading import Thread
import time


class Runtime:
    def __init__(self, notifyCallback):
        self.pinename = "HmiRuntime"
        # Create pipeline
        self.client = ODK_pipe(self.pinename)
        # A callback function to be called when data is available.
        self.notifyCallback = notifyCallback
        # start a thread which will start the daemon process
        self.th1 = Thread(target=self.callbackDaemon)
        # Make the thread a daemon so that it will be killed when the main thread exits.
        self.th1.daemon = True
        # start the thread
        self.th1.start()

    def __exit__(self):
        # print("exit started")
        self.th1.join()
        self.client.close()
        self.__del__()

    # Read single Tag, return only the value
    def ReadTagValueSync(self, name):
        return_result = self.client.write("ReadTagValue %s\n" % name)
        response = self.client.read()
        tag = Tag(response)
        return tag.value

    def WriteTagValue(self, name, value):
        return self.client.write("WriteTagValue %s %d\n" % (name, value))

    # Subscribe Tags
    def SubscribeTagValue(self, name):
        return self.client.write("SubscribeTagValue %s\n" % name)

    # Unsubscribe all Tags
    def UnsubscribeTagValue(self, name):
        return self.client.write("UnsubscribeTagValue %s\n" % name)

    def SendExpertCommand(self, jsonCommand):
        return self.client.write(jsonCommand)

    def SetCharSet(self, encoding):
        return self.client.write(encoding)

    def callbackDaemon(self):
        # 1. As long as thread is active
        # 2. Check if data is present in the pipe
        # 3. Read the data if it is there
        # 4. Invoke the callback function set in the constructor using the data
        while 1:
            time.sleep(0.01)
            if self.client.isDataInPipe():
                response = self.client.read()
                self.notifyCallback(response)
