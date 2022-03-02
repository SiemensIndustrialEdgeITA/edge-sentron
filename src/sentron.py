from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from datetime import datetime
from enum import Enum
import time
import numpy as np
import sys
sys.path.insert(0, '..\\') 
import threading
# from ODK_pipe_Socket_Linux import ODK_pipe
# import Runtime
import json
import sys
import socket


def printOnSuccess(jsonResponse):
    # parse and print success json
    tagsInfo = jsonResponse["Params"]["Tags"]
    for tag in tagsInfo:
        print(
            "Name : {}\nErrorCode : {}\nError Description : {}\n\n".format(
                tag["Name"], tag["ErrorCode"], tag["ErrorDescription"]
            )
        )


def printOnError(jsonResponse):
    # parse and print error json
    print(
        "Message : {}\nError Code : {}\nErrorDescription : {}".format(
            jsonResponse["Message"],
            jsonResponse["ErrorCode"],
            jsonResponse["ErrorDescription"],
        )
    )
    
def callbackFunction(response):
    # Callback comes here from Runtime
    # do JSON loading in a try block to avoid invalid JSON processing.

    print("------------ Callback READ ------------")
    print(response)

    # Split response
    s = response.split("\n",1)
    print(s)
    
    # Conncetion settings response from HMI
    # {"log":"\u003c_io.TextIOWrapper name='\u003cstderr\u003e' mode='w' encoding='utf-8'\u003e {\"ClientCookie\":\"myRequest1\",\"Message\":\"NotifyReadTag\",\"Params\":{\"Tags\":[{\"ErrorCode\":0,\"ErrorDescription\":\"\",\"Name\":\"Unit_Id\",\"Quality\":\"Good\",\"QualityCode\":192,\"TimeStamp\":\"2022-02-16 17:43:29.7227210\",\"Value\":\"1\"},{\"ErrorCode\":0,\"ErrorDescription\":\"\",\"Name\":\"Port_Number\",\"Quality\":\"Good\",\"QualityCode\":192,\"TimeStamp\":\"2022-02-16 17:43:27.5093550\",\"Value\":\"502\"},{\"ErrorCode\":0,\"ErrorDescription\":\"\",\"Name\":\"Ip_Address\",\"Quality\":\"Good\",\"QualityCode\":192,\"TimeStamp\":\"2022-02-16 17:43:24.0047780\",\"Value\":\"192.168.100.10\"},{\"ErrorCode\":0,\"ErrorDescription\":\"\",\"Name\":\"Enable\",\"Quality\":\"Good\",\"QualityCode\":192,\"TimeStamp\":\"2022-02-16 17:43:32.9775190\",\"Value\":\"TRUE\"}]}}\n","stream":"stdout","time":"2022-02-16T18:05:08.125940659Z"}

    try:
        # Parse response
        y = json.loads(s[0])
        msg = y['Message']
        print(msg)
        
        if msg == "NotifyWriteTag":
            print(msg)
            printOnSuccess(y)
        elif msg == "NotifyReadTag":
            
            print("---- RESPONSE ----")
            # Debug
            print(y['Params']['Tags'][0]['Value'])
            print(y['Params']['Tags'][1]['Value'])
            print(y['Params']['Tags'][2]['Value'])
            print(y['Params']['Tags'][3]['Value'])
            
            print(msg)
            printOnSuccess(y)
            # Get tags value
            enable = y['Params']['Tags'][3]['Value']
            print(enable)
            global modbus_enable
            if(enable == "TRUE"):   
                modbus_enable = "TRUE"
                # Get connection parameters tags
                global plc_address, modbus_port , unit_id
                plc_address = y['Params']['Tags'][2]['Value']
                modbus_port = y['Params']['Tags'][1]['Value']
                unit_id = int(y['Params']['Tags'][0]['Value'])
            if(enable == 'FALSE'):
                modbus_enable = "FALSE"
        elif msg == "ErrorWriteTag":
            printOnError(y)

            
    except json.decoder.JSONDecodeError:
        print("response is not a valid JSON")

# Init measures
def init():

    global plc_address 
    global modbus_port
    global unit_id
    global modbus_enable
    global pipe_socket

    plc_address = "192.168.100.1"
    modbus_port = "502"
    unit_id = 1
    modbus_enable = "FALSE"

    ConnectionState = 0
    ErrorState = 0

    # Voltage L-N (V)
    L1_N = 0
    L2_N = 0
    L3_N = 0

    # Voltage L-L (V)
    L1_L2 = 0
    L2_L3 = 0
    L3_L1 = 0

    # Current (I)
    I1 = 0
    I2 = 0
    I3 = 0

    # Apparent power (VA)
    S_L1 = 0
    S_L2 = 0
    S_L3 = 0

    # Active power (W)
    P_L1 = 0
    P_L2 = 0
    P_L3 = 0

    # Reactive power (var)
    Q_L1 = 0
    Q_L2 = 0
    Q_L3 = 0

    # Power Factor
    PF_L1 = 0
    PF_L2 = 0
    PF_L3 = 0

    # Frequency
    Frequency = 0

    # L_N avg (V)
    L_N_Avg = 0

    # L_L avg (V)
    L_L_Avg = 0

    # I avg (I)
    I_Avg = 0

    # Total apparent power (VA)
    S_Total = 0

    # Total active power (W)
    P_Total = 0

    # Total apparent power (var)
    Q_Total = 0

    # Total power factor
    PF_Total = 0

    # Neutral current (A)
    I_N = 0

    # Total active energy imported - current period (Wh)
    P_Total_Imp = 0

    # Total reactive energy imported - current period (varh)
    Q_Total_Imp = 0

    # Total active energy exported - current period (Wh)
    P_Total_Exp = 0

    # Total reactive energy exported - current period (varh)
    Q_Total_Exp = 0

# Set WinCC Unified values
def setValues(values):

    # Connection state 
    # 0: disconnect 
    # 1: connect
    ConnectionState = connection_state
    
    # Error state 
    # 0: no error 
    # 1: error
    ErrorState = error_state

    # Voltage L-N (V)
    L1_N = values[0]
    L2_N = values[1]
    L3_N = values[2]

    # Voltage L-L (V)
    L1_L2 = values[3]
    L2_L3 = values[4]
    L3_L1 = values[5]

    # Current (I)
    I1 = values[6]
    I2 = values[7]
    I3 = values[8]

    # Apparent power (VA)
    S_L1 = values[9]
    S_L2 = values[10]
    S_L3 = values[11]

    # Active power (W)
    P_L1 = values[12]
    P_L2 = values[13]
    P_L3 = values[14]

    # Reactive power (var)
    Q_L1 = values[15]
    Q_L2 = values[16]
    Q_L3 = values[17]

    # Power Factor
    PF_L1 = values[18]
    PF_L2 = values[19]
    PF_L3 = values[20]

    # Frequency
    Frequency = values[27]

    # L_N avg (V)
    L_N_Avg = values[28]

    # L_L avg (V)
    L_L_Avg = values[29]

    # I avg (I)
    I_Avg = values[30]

    # Total apparent power (VA)
    S_Total = values[31]

    # Total active power (W)
    P_Total = values[32]

    # Total apparent power (var)
    Q_Total = values[33]

    # Total power factor
    PF_Total = values[34]

    # Neutral current (A)
    I_N = values[35]

    # Total active energy imported - current period (Wh)
    P_Total_Imp = values[50]

    # Total reactive energy imported - current period (varh)
    Q_Total_Imp = values[51]

    # Total active energy exported - current period (Wh)
    P_Total_Exp = values[52]

    # Total reactive energy exported - current period (varh)
    Q_Total_Exp = values[53]
    
    # Last polling timestamp
    Polling_timestamp = datetime.now()
    
    # Prepare query for WinCC
    writeTagCommand = '{"Message":"WriteTag","Params":{"Tags":[{"Name":"ConnectionState","Value":"' + str(ConnectionState) + '"},{"Name":"Polling_Timestamp","Value":"' + str(Polling_timestamp) + '"},{"Name":"ErrorState","Value":"' + str(ErrorState) + '"},{"Name":"L1_N","Value":"' + str(L1_N) + '"},{"Name":"L2_N","Value":"' + str(L2_N) + '"},{"Name":"L3_N","Value":"' + str(L3_N) + '"}, {"Name":"L1_L2","Value":"' + str(L1_L2) + '"},{"Name":"L2_L3","Value":"' + str(L2_L3) + '"},{"Name":"L3_L1","Value":"' + str(L3_L1) + '"},{"Name":"I1","Value":"' + str(I1) + '"},{"Name":"I2","Value":"' + str(I2) + '"},{"Name":"I3","Value":"' + str(I3) + '"},{"Name":"S_L1","Value":"' + str(S_L1) + '"},{"Name":"S_L2","Value":"' + str(S_L2) + '"},{"Name":"S_L3","Value":"' + str(S_L3) + '"},{"Name":"P_L1","Value":"' + str(P_L1) + '"},{"Name":"P_L2","Value":"' + str(P_L2) + '"},{"Name":"P_L3","Value":"' + str(P_L3) + '"},{"Name":"Q_L1","Value":"' + str(Q_L1) + '"},{"Name":"Q_L2","Value":"' + str(Q_L2) + '"},{"Name":"Q_L3","Value":"' + str(Q_L3) + '"},{"Name":"Frequency","Value":"' + str(Frequency) + '"},{"Name":"L_N_Avg","Value":"' + str(L_N_Avg) + '"},{"Name":"L_L_Avg","Value":"' + str(L_L_Avg) + '"},{"Name":"I_Avg","Value":"' + str(I_Avg) + '"},{"Name":"S_Total","Value":"' + str(S_Total) + '"},{"Name":"P_Total","Value":"' + str(P_Total) + '"},{"Name":"Q_Total","Value":"' + str(Q_Total) + '"},{"Name":"PF_L1","Value":"' + str(PF_L1) + '"},{"Name":"PF_L2","Value":"' + str(PF_L2) + '"},{"Name":"PF_L3","Value":"' + str(PF_L3) + '"},{"Name":"PF_Total","Value":"' + str(PF_Total) + '"},{"Name":"I_N","Value":"' + str(I_N) + '"},{"Name":"P_Total_Imp","Value":"' + str(P_Total_Imp) + '"},{"Name":"Q_Total_Imp","Value":"' + str(Q_Total_Imp) + '"},{"Name":"P_Total_Exp","Value":"' + str(P_Total_Exp) + '"},{"Name":"Q_Total_Exp","Value":"' + str(Q_Total_Exp) + '"}]},"ClientCookie":"CookieReadTags123"}\n'
    print(writeTagCommand)
    
    # Send data to WinCC
    pipe_socket.sendall(writeTagCommand.encode()) 
    print("Sended measures")      
    
    
# Init variables
init()


# Polling time (s)
polling_time = 5

# Sentron enable
sentron_enable = 0

# Connection state init
connection_state = 0

# Modbus TCP parameters
plc_address
modbus_port
unit_id

# Modbus TCP/IP enable
modbus_enable


        
# Values array - Device registers - Create device class 
values = np.zeros(100)


# Modbus client
client = ModbusClient(plc_address, modbus_port)

# Error 
error_state = 0          # error state 
error_code = 0           # error code number
error_code_desc = ""     # error code description

# Write command WinCC
writeTagCommand = ""

'''
# Try first socket connection
try:
    connection_state = client.connect()
    connection_state = 1
    
except  Exception as e:
    connection_state = 0
'''    

length = 1024

# Unix path
file_name = '/temp/HmiRuntime'


# Windows path
# file_name = '\\\\.\\pipe\\HmiRuntime'

# AF_UNIX: process on the same machine
# SOCK_STREAM: stream oriented socket
pipe_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
pipe_socket.setblocking(0)

print(sys.stderr, 'Connecting to %s' % file_name)

# Socket connection 
try:
    pipe_socket.connect(file_name)
    print(sys.stderr, 'Connected to %s' % file_name)
except socket.error as msg:
    print(sys.stderr, msg)


# Read tag from WinCC
readTagCommand = '{"Message":"ReadTag","Params":{"Tags":["Enable","IPv4","Port_Number","Unit_Id"]},"ClientCookie":"myRequest1"}\n'
pipe_socket.sendall(readTagCommand.encode())


#Read register - Set interval from HMI
while True:

      # Start reading time
      startime = time.time()

      print("------------------------------------")
      timestamp = datetime.now()   
      print("Timestamp: ", timestamp)
      if(connection_state == 1):
           print("Connection state: ONLINE")
      elif(connection_state == 0):
           print("Connection state: OFFLINE")
      
      
      # Check if there are data on socket
      try:
          print("Receive data")
          read_value = pipe_socket.recv(length)
          print("Received data")
          reads = read_value.decode()
          callbackFunction(reads)
      except BlockingIOError:
          print('no data')
      
      
      print(modbus_enable)
      print(plc_address)
      print(modbus_port)
      print(unit_id)

      if(modbus_enable == "TRUE"):
         print("Polling enabled")
         # If connection is open run modbus reading registers
         if(connection_state == 1):
    
               try:   
                       # Read 100 registers - 16 int
                       register_1 = 0 # start address first block
                       request_1 = client.read_holding_registers(register_1, 100, unit = unit_id)

                       # Read 100 registers - 16 int
                       register_2 = 548 # start address third block
                       request_2 = client.read_holding_registers(register_2, 100, unit = unit_id)

                       # decode_32_bit
                       index_register = 0
                       index_register_modbus = 0
              
                       # Compose index register query n.1
                       for index_register in range (50):
              
                           temp_register_value_1 = request_1.registers[index_register_modbus]
                           temp_register_value_2 = request_1.registers[index_register_modbus + 1]
                           temp_registers = []
                           temp_registers.append(temp_register_value_1)
                           temp_registers.append(temp_register_value_2)
                  
                           decoder = BinaryPayloadDecoder.fromRegisters(temp_registers, Endian.Big, wordorder=Endian.Little)
                           values[index_register] = decoder.decode_32bit_float()
                  
                           index_register_modbus += 2

              
                       # decode_32_bit
                       index_register = 0
                       index_register_modbus = 0

                       # Compose index register query n.2
                       for index_register in range (50):
              
                           temp_register_value_1 = request_2.registers[index_register_modbus]
                           temp_register_value_2 = request_2.registers[index_register_modbus + 1]
                           temp_registers = []
                           temp_registers.append(temp_register_value_1)
                           temp_registers.append(temp_register_value_2)
                  
                           decoder = BinaryPayloadDecoder.fromRegisters(temp_registers, Endian.Big, wordorder=Endian.Little)
                           values[index_register + 50] = decoder.decode_32bit_float()
                  
                           index_register_modbus += 2

               except  Exception as e:
                       values = np.zeros(100)
                       error_state = 1
                       error_code = 1
                       error_code_desc = e.args[0]
                       connection_state = 0
              
      
               # Write on WinCC 
               setValues(values)
            
      
               # End time
               endtime = time.time()
               print("Execution time: %s seconds " % (endtime - startime))
               print("Error code: ", error_code, " description: ", error_code_desc)
               time.sleep(polling_time)
     
     
            # Else if connection is close store zeros into dabatabase
         elif(connection_state == 0):
      
                 values = np.zeros(100)
                
                 # Write zeros on WinCC 
                 setValues(values)
        
                 # Send data to WinCC
                 # runtime.SendExpertCommand(writeTagCommand)
                 pipe_socket.sendall(writeTagCommand.encode())  

                 # End time
                 endtime = time.time()
                 print("Execution time: %s seconds " % (endtime - startime))
                 #  print("Error: ", error_code)
                 print("Error code: ", error_code, " description: ", error_code_desc)
                 # Modbus client
                 client = ModbusClient(plc_address, modbus_port)
                 connection_state = client.connect()
     
                 if(connection_state == True):
                    connection_state = 1
                    error_state = 0
                    error_code = 0
                    error_code_desc = ""
                 elif(connection_state == False):
                    connection_state = 0
                    error_state = 0
                    error_code = 0
                    error_code_desc = ""

                 time.sleep(polling_time)
      
      elif(modbus_enable == "FALSE"):
             print("Polling disabled")
             connection_state = 0
             error_state = 0
             values = np.zeros(100)
             # End time
             endtime = time.time()
             print("Execution time: %s seconds " % (endtime - startime))
             print("Error code: ", error_code, " description: ", error_code_desc)
             time.sleep(polling_time)