#  - * -coding: utf - 8 -*-
#  Этот скрипт обращается к устройствам локальной сети используя ssdp запросы, получая информацию о них.

import socket
import re


def discover():
    """
    Функция формирует SSDP запрос и отправляет его в локальную сеть,
    прослушивая ответы и добавляя откликнувшиеся устройства в список.
    """

    # IP и Port для SSDP запроса
    ssdp_addr = "239.255.255.250"
    ssdp_port = 1900
    ssdp_mx = 2
    ssdp_st = "ssdp:all"

    #  Время ожидания
    waiting = 2

    ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
                  "HOST: {}:{}\r\n".format(ssdp_addr, ssdp_port) + \
                  "MAN: \"ssdp:discover\"\r\n" + \
                  "MX: {}\r\n".format(ssdp_mx) + \
                  "ST: {}\r\n".format(ssdp_st) + "\r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(waiting)
    paths = []
    while True:
        try:
            #  Отправка SSDP запроса
            sock.sendto(ssdpRequest.encode(), (ssdp_addr, ssdp_port))
            print("Прослушиваем локальную сеть...\r", end='')

            #  Прослушивание ответа
            data, fromaddr = sock.recvfrom(1024)
            parsed = re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', str(data, 'utf-8'))
            if parsed not in paths:
                paths.append(parsed)
                print("\nНайдено SSDP устройство:\n", parsed)
        except socket.error as e:
            print("Данных пока нет")
            print(e)


discover()
