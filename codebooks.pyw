import sys
from codebook_ui.codebook_main import *

def main():
    print('Starting...')

    app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QMainWindow()
    # ui = CodebooksMainWindow(os.path.dirname(os.path.realpath(__file__)))
    # ui.setupUi(window)
    # window.show()
    current_directory = os.path.dirname(os.path.realpath(__file__))
    window = CodebooksMainWindow(current_directory)
    
    sys.exit(app.exec_())


# Runtime
if __name__ == '__main__':
    main()