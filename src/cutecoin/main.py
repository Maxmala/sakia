"""
Created on 1 févr. 2014

@author: inso
"""
import signal
import sys
import logging
import asyncio

from quamash import QEventLoop
from PyQt5.QtWidgets import QApplication
from cutecoin.gui.mainwindow import MainWindow
from cutecoin.core.app import Application

if __name__ == '__main__':
    # activate ctrl-c interrupt
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    cutecoin = QApplication(sys.argv)
    loop = QEventLoop(cutecoin)
    asyncio.set_event_loop(loop)
    print("Debug enabled : {0}".format(loop.get_debug()))

    with loop:
        app = Application.startup(sys.argv, cutecoin, loop)
        window = MainWindow(app)
        window.startup()
        window.showMaximized()
        loop.run_forever()
    sys.exit()
