import sys

from PyQt5.QtWidgets import QApplication

from regexport.app import App


def main():
    qapp = QApplication(sys.argv)
    app = App()
    win = app.create_gui()
    win.show()
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    main()
