import json

class Tag():
    def __init__(self, name, quality=0, timestamp=None, value=None, error=0, errordescription=""):
        self.name = name
        self.quality = quality
        self.timestamp = timestamp
        self.value = value
        self.error = error
        self.errordescription = errordescription

    def __init__(self, reply_result, decode = True, codec='utf-8'):
        if decode :
            res = reply_result.decode(codec).split(' ', 3)
        else:
            res = reply_result.split(' ', 2)
        command = res[0]
        self.quality = 0
        self.error = 0
        self.errordescription = ""
        if command.startswith('Notify'):
            # command mode
            self.name = res[1]
            if command == "Notify":
                # Notify Tag
                j = json.loads(res[2])
                if j.get("QualityCode") != None:
                    # return value
                    self.quality = j["QualityCode"]
                    self.timestamp = j["TimeStamp"]
                    self.value = j["Value"]
                else:
                    # return error
                    self.error = j["ErrorCode"]
                    self.errordescription = j["ErrorDescription"]

            if command == "NotifyReadTagValue":
                # set only value
                self.value = res[3]
            if command == "ErrorReadTagValue":
                # Error
                if command.startswith('{'):
                    # json error reply
                    j = json.loads(res[2])
                    self.error = j["ErrorCode"]
                    self.errordescription = j["ErrorDescription"]
                else:
                    self.errordescription = res[2]

        else:
            # json mode
            if decode:
                j = json.loads(reply_result.decode(codec))
            else:
                j = json.loads(reply_result)

    #def __del__(self):
        # print("del initiated")


    def __exit__(self):
        # print("exit started")
        self.__del__()

class TagSet():
    def __init__(self, reply_result, codec='utf-8'):
        res = reply_result.decode(codec).split(' ', 2)
        command = res[0]

        if command.startswith('Notify'):
            # command mode
            res = reply_result.decode(codec).split('\n')

            self.taglist = []
            for strTag in res:
                if len(strTag) > 3:
                    self.taglist.append(Tag(strTag, False))

        else:
            # json mode
            j = json.loads(reply_result.decode(codec))

    def TagList(self):
        return self.taglist


    #def __del__(self):
        # print("del initiated")


    def __exit__(self):
        # print("exit started")
        self.__del__()