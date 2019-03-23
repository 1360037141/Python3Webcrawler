from PyQt5 import QtWidgets,QtCore,QtGui
from untitled import Ui_MainWindow
from crawl import get_html
import sys,csv


class TaoBao(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(TaoBao, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click_data)

    def click_data(self):
        get_keyword=self.textEdit.toPlainText()
        number=self.comboBox.currentIndex()+1
        get_html(get_keyword,number*5)
        self.label_3.setText('采集完成')

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    taobao=TaoBao()
    taobao.show()
    sys.exit(app.exec())