import time
import serial
import paho.mqtt.client as mqtt_client
import random

broker="broker.emqx.io"

client = mqtt_client.Client(f'lab_{random.randint(10000, 99999)}')

def get_connection(port):
    ser = serial.Serial(port, timeout=1)
    return ser

# def send(ser, message, mesg_len):
#     ser.write(message)
#     time.sleep(0.1)
#     result = None
#     if mesg_len != 0:
#         data = ser.read(mesg_len)
#         result = data.decode()
#         result = result.strip()
#         print(result)
#     return 
arr = []
avg_all = 0
avg = 0
duration = 20
stinput = True

if __name__ == '__main__':
    ser = get_connection("COM3")
    client.connect(broker)
    print("""Commands:
            1 - transfer of instantaneous sensor values
            2 - transfer of averaged data
            3 - streaming data
            4 - Stream min, max and current values (20 seconds)
            5 - on the threshold of turning on the light""")

    # while ser.inWaiting() < 0 and 
    while(True):
        if stinput:
            command = int(input("Enter: "))

        while ser.inWaiting() < 2:
            pass
        
        val = ser.read(2)
        # print(val)
        # val = ser.readline()
        # val = ser.read(count)
        result = val.decode()

        if(result!=""):
            result = int(result)
            arr = [result] + arr
            avg_all += int(result)
        if(len(arr)>=100):
            avg = avg_all / 100
            avg_all -= arr.pop()
        if(len(arr) < 100 and len(arr) > 0):
            avg = avg_all / len(arr)


        if command == 1:
            client.publish('lab/UNIQUE_ID/photo/instant', result)
        elif command == 2:
            client.publish('lab/UNIQUE_ID/photo/averge', avg)
        elif command == 3:
            if stinput:
                timer_start = time.time()
                stinput = False
            if time.time() - timer_start >= duration:
                stinput = True
            client.publish('lab/UNIQUE_ID/photo/stream', result)
        elif command == 4:
            if stinput:
                timer_start = time.time()
                stinput = False
            if time.time() - timer_start >= duration:
                stinput = True
            client.publish('lab/UNIQUE_ID/photo/stream4', result)
        elif command == 5:
            if stinput:
                timer_start = time.time()
                stinput = False
            if time.time() - timer_start >= duration:
                stinput = True
            client.publish('lab/UNIQUE_ID/photo/mean', (max(arr) + min(arr)) / 2)
            # client.publish('lab/UNIQUE_ID/photo/min', min(arr))
            client.publish('lab/UNIQUE_ID/photo/porog', result)
            





    client.disconnect()



    # print(type(val))
    # val = val.strip()
    # result = int.from_bytes(val, "big")
    #result = int(val)
    #val = ser.readline()
    # result = [int(byte_) for byte_ in val]  
    # result = (result[0] << 8 & 0xFF00) + (result[1] & 0xFF) 
    # result = map(result, 0, 1024, 0, 100)
    # result = val.decode()
    # result = result.strip()
    # print(result)
    # print("fkfkfjm")

# client.connect(broker)
# client.publish('lab/UNIQUE_ID/photo/instant', "Hello Irishka!!")
# client.disconnect()
