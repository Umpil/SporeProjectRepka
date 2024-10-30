import serial
import time

# Настройка последовательного порта
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

def send_command(command, delay=1):
    ser.write((command + '\r\n').encode())
    time.sleep(delay)
    response = ser.read(ser.in_waiting).decode()
    return response

# Установите параметры точки доступа
send_command('AT+SAPBR=3,1,"CONTYPE","GPRS"')
send_command('AT+SAPBR=3,1,"APN","internet.tele2.ru"')  # Замените your_apn на APN вашего оператора

# Откройте контекст PDP
send_command('AT+SAPBR=1,1')
send_command('AT+SAPBR=2,1')

# Инициализация HTTP-сервиса
send_command('AT+HTTPINIT')

# Установка URL
send_command('AT+HTTPPARA="URL","http://spore.k-lab.su')

# Отправка GET-запроса
send_command('AT+HTTPACTION=0')

# Чтение ответа сервера
response = send_command('AT+HTTPREAD', delay=2)
print("Response:", response)

# Закрытие HTTP-сервиса
send_command('AT+HTTPTERM')

# Закрытие контекста PDP
send_command('AT+SAPBR=0,1')

# Закрытие последовательного порта
ser.close()

