from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from words import Ui_MainWindow
import pymysql
from crawl import main
import sys

class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("背单词v0.1")
        #数据库
        self.connect=pymysql.connect(
            host='localhost',
            user='root',
            password='lyy218063',
            database='words',
            charset='utf8'
        )
        self.cur=self.connect.cursor()
        sql='select * from words'
        self.cur.execute(sql)

        result=self.cur.fetchall()

        for r in result:
            data=" ".join(r[1:])
            self.listWidget.addItem(data)

        self.pushButton.clicked.connect(self.get_word)
    def get_word(self):
        try:
            word=self.lineEdit.text()
            types, means=main(word)
            types=" ".join(types)
            means=" ".join(means)
            print(types,means)

            sql="insert into words(word,type,mean) values(%s,%s,%s)"
            self.cur.execute(sql,[word,types,means])
            self.listWidget.addItem(word+" "+types+" " +means)
            self.connect.commit()
            self.lineEdit.clear()
        except Exception as e:
            print(e)
            self.connect.rollback()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.connect.close()
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ui=Main()
    ui.show()
    sys.exit(app.exec())