#!/usr/bin/env python3
#file : port_scan2.py
#author : Tegar Dev
import argparse
import socket
from colorama import init, Fore

from threading import Thread, Lock
from queue import Queue

# warna
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

logo = f"""
   ^^^^^^^
   |      |
   |      |
   |  ({RED}o{RESET}){RED}o{RESET})
  (c      _)
   |   ___)      {GREEN}  __________________ _____________________{RESET}
   L____/        {GREEN}  \______   \_____  \\______   \__    ___/{RESET}
  /     \        {GREEN}   |     ___//   |   \|       _/ |    |{RESET}
 /       \       {GREEN}   |    |   /    |    \    |   \ |    |{RESET}
 |L_|    |       {GREEN}   |____|   \_______  /____|_  / |____|{RESET}
 | ||    |       {GREEN}                    \/       \/{RESET}
 | ||    |
 L(_)___/                      Port Scanner
   \###|
    |||                      coded : Tegar Dev
    LLL_
   (___))                Komunitas : AsukaDev Official
"""

N_THREADS = 200
q = Queue()
print_lock = Lock()

def port_scan(port):
    """
    Scan a port on the global variable `host`
    """
    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        with print_lock:
            print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
    finally:
        s.close()


def scan_thread():
    global q
    while True:
        worker = q.get()
        port_scan(worker)
        q.task_done()


def main(host, ports):
    global q
    for t in range(N_THREADS):
        t = Thread(target=scan_thread)
        t.daemon = True
        t.start()

    for worker in ports:
        q.put(worker)
    q.join()


if __name__ == "__main__":
    print(logo)
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [ p for p in range(start_port, end_port)]

    main(host, ports)
