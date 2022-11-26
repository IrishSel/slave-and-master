import serial

ser.in_waiting 
ser.write(b'b')  
ser.write(b'1')  
data = ser.read_all().decode().strip()

mesg_length = {b'1': 5,
               b'2': 5}  


def get_connection():
    ser = serial.Serial('COM10', timeout=1)
    return ser


def get_sensor(ser, sensor_byte, tries=3):
    for _ in range(tries):
        ser.write(sensor_byte)
        data = ser.read(mesg_length[sensor_byte]).decode().strip()
        if data == '':
            print('No data, something wrong')
        else:
            break
    return data


ser = get_connection()
for i in range(10):
    print(f'Data are (try {i})', get_sensor(ser, b'1'))
ser.close()
ser = get_connection()
for i in range(10, 20):
    print(f'Data are (try {i})', get_sensor(ser, b'2'))
ser.close()
