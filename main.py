import sys
from  manager_password import *

def manager_password():
    app = QtWidgets.QApplication(sys.argv)
    manager_password = Telas_manager_password()
    sys.exit(app.exec_())
if __name__ == '__main__':
    manager_password()

