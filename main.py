import sys
from PyQt5.QtWidgets import *
import random
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import operator

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Initialize()

    def Initialize(self):
        vLayer = QHBoxLayout()
        bLayer = QHBoxLayout()
        window = QVBoxLayout()

        self.Random = QPushButton('Random', self)
        self.Best = QPushButton('Best', self)
        self.Output = QTextEdit()
        self.Output.isReadOnly()

        self.Random.clicked.connect(self.onRandomClick)
        self.Best.clicked.connect(self.onBestClick)

        vLayer.addWidget(self.Random)
        vLayer.addWidget(self.Best)
        bLayer.addWidget(self.Output)

        window.addLayout(vLayer)
        window.addLayout(bLayer)

        self.setLayout(window)
        self.setWindowTitle('Lotto')
        self.setGeometry(300, 300, 300, 600)
        self.show()

    def onRandomClick(self):
        Alphabet = ['A', 'B', 'C', 'D', 'E']

        Label = ''
        Label += '로또 번호 랜덤 추첨하겠습니다.\n\n'
        Label += '발행일 : ' + str(datetime.now()) + '\n\n'
        Label += '-------------------------\n\n'

        for i in range(5):
            arr = []
            for j in range(5):
                num = random.randrange(1, 46)
                if num < 10:
                    string = '0'
                    string += str(num)
                    arr.append(string)
                else:
                    arr.append(str(num))
            arr.sort()
            Label += '  ' + str(Alphabet[i]) + '  자  동 ' + str(arr[0]) + ' ' + str(arr[1]) + ' '  + str(arr[2]) + ' '  + str(arr[3]) + ' '  + str(arr[4]) + '\n\n'
        Label += '-------------------------'
        self.Output.setText(Label)

    def onBestClick(self):
        Number = {}
        URL = 'https://dhlottery.co.kr/gameResult.do?method=statByNumber'
        request = requests.get(URL)
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')

        data = str(soup.find('table', id='printTarget').find('tbody').find_all('tr'))

        for i in range(45):
            nDelimiter = 0
            nDelimiter = data.find('</tr>')
            num = data[nDelimiter - 9: nDelimiter - 6]
            data = data[nDelimiter + 5:]
            Number[i + 1] = int(num)

        Number = sorted(Number.items(), key=operator.itemgetter(1), reverse=True)

        Alphabet = ['A', 'B', 'C', 'D', 'E']

        Label = ''
        Label += '로또 번호 랜덤 추첨하겠습니다.\n\n'
        Label += '발행일 : ' + str(datetime.now()) + '\n\n'
        Label += '-------------------------\n\n'

        for i in range(5):
            arr = []
            use = [False] * 11
            for j in range(5):
                num = random.randrange(0, 10)
                if not use[num]:
                    use[num] = True
                    arr.append(Number[num][0])
                else:
                    while 1:
                        num = random.randrange(0, 10)
                        if not use[num]:
                            use[num] = True
                            arr.append(Number[num][0])
                            break

            arr.sort()
            Label += '  ' + str(Alphabet[i]) + '  자  동 ' + str(arr[0]) + ' ' + str(arr[1]) + ' '  + str(arr[2]) + ' '  + str(arr[3]) + ' '  + str(arr[4]) + '\n\n'
        Label += '-------------------------'
        self.Output.setText(Label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
