import serial
#open serial port and initialize baud rate
ser = serial.Serial('COM4', 115200)
#set time out to avoid unending wait for serial read out
ser.ser_port.timeout = 2
#initialize x string for move coordinates
x = ''
#read in default startup data from arduino
print(ser.readline().decode())
print(ser.readline().decode())
#loop until exit command is input
while(x != 'quit'):
    #get input coordinates from user via terminal
    print("input coordinate or coordinates (X0Y0)")
    x = input()
    #write string to serial port in bytes form
    ser.write(x.encode())
    #get the return string from serial port
    return_string = ser.readline()
    if(return_string == 'ok'):
        print("movement was successful")
    if(return_string.split()[1] == 'error'):
        print("movement was unsuccessful, try again.")    
#close the port
ser.close()