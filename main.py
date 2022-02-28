import socket
import configparser
import time
import random


config = configparser.ConfigParser()
config.read('config.ini')

server_hostname = config.get('settings', 'server_hostname')
server_port = int(config.get('settings', 'server_port'))
send_interval = float(config.get('settings', 'send_interval'))
random_data_mode = False
if int(config.get('settings', 'random_data_mode')) == 1:
    random_data_mode = True
    print('Random data mode ON')


def randomize_data():
    global in_flowrate, in_temperature, in_humidity, outside_temperature, outside_humidity, \
        ventilation_temperature, ventilation_humidity, co2_value, filter_differential_pressure

    in_flowrate = random.randrange(0, 999)
    in_temperature = random.normalvariate(25, 5)
    in_humidity = random.randrange(0, 99)
    outside_temperature = random.normalvariate(10, 7)
    outside_humidity = random.randrange(0, 99)
    ventilation_temperature = random.normalvariate(20, 2)
    co2_value = random.normalvariate(400, 20)
    filter_differential_pressure = random.randrange(0, 100)


def init_tcp_socket():
    global client_sock
    print('socket_init: TCP socket init...')
    try:
        client_sock.settimeout(5)
        client_sock.connect((server_hostname, server_port))

    except Exception as err:
        print('socket_init: TCP sock connect error!', err)
        raise SystemExit
    else:
        return True


def send_data_tcp_sock(payload_bytes):
    try:
        if client_sock.send(payload_bytes) == len(payload_bytes):
            return True
        else:
            print('tcp_send: TCP send fail!')
            return False
    except Exception as err:
        print('tcp_send: TCP send exception:', err)
        return False


if __name__ == '__main__':
    client_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    init_tcp_socket()
    device_serial = '12311'
    in_flowrate = 122
    in_temperature = 12.3
    in_humidity = 71
    outside_temperature = -12.3
    outside_humidity = 54
    ventilation_temperature = 23.2
    ventilation_humidity = 42
    co2_value = 491
    filter_differential_pressure = 233

    tx_counter = 0

    while True:
        if random_data_mode:
            randomize_data()
        tx_str = '{}|{}|{:.1f}|{}|{:.1f}|{}|{:.1f}|{}|{:.2f}|{}\n'.format(device_serial, in_flowrate, in_temperature,
                                                                          in_humidity, outside_temperature,
                                                                          outside_humidity, ventilation_temperature,
                                                                          ventilation_humidity, co2_value,
                                                                          filter_differential_pressure)

        tx_byte = tx_str.encode(encoding='utf-8', errors='ignore')
        print('DEBUG: tx_byte:{}'.format(tx_byte))
        if not send_data_tcp_sock(tx_byte):
            # TCP socket send error
            print('TCP send error, try init tcp socket')
            init_tcp_socket()

        tx_counter = tx_counter + 1
        print('DEBUG: TX_counter:{}'.format(tx_counter))
        time.sleep(send_interval)
