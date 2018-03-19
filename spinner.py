# Written by Nestor Lee for DIS2018
#
# Background Audio by: Balloon Game Kevin MacLeod (incompetech.com)
# Licensed under Creative Commons: By Attribution 3.0 License
# http://creativecommons.org/licenses/by/3.0/
#
# Background Image found: https://pngtree.com/freebackground/circus-stage-background-material_805701.html
# Assume licensed under Creative Commons
#
# Main

# Imports the Class files
# import GameConsole
import SpinnerConsoleWindow
# import QRCodeScanner

# Using the multiprocessing library to run different processes for the different interfaces
from multiprocessing import Process


# def consoleWindow():
#     root = Tk()
#     root.title("Spinning Wheel Console")
#     display = GameConsole.GameConsole(root)
#     root.mainloop()
#
#
# def qrCodeScanner():
#     initiateQRCodeScanner = QRCodeScanner.QRCodeScanner()


def spinnerWindow():
    initiateSpinnerWindow = SpinnerConsoleWindow.SpinnerConsoleWindow()


if __name__ == '__main__':
    # Process(target=qrCodeScanner).start()
    # Process(target=consoleWindow).start()
    Process(target=spinnerWindow).start()