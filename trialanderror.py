import time
import os
def emptyTerminal():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')
counter = 2
while counter > 0:
    print("Signing in", end= "", flush=True)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    emptyTerminal()
    counter -= 1



eiwjkeaoje
