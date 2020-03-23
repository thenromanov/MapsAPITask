import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

screenSize = (600, 450)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.coords = [37.618909, 55.751400]
        self.scale = 15
        self.getImage()
        self.initUI()

    def getImage(self):
        mapServer = 'http://static-maps.yandex.ru/1.x/'
        mapParams = {
            'll': ','.join(map(str, self.coords)),
            'z': str(self.scale),
            'l': 'map'
        }
        response = requests.get(mapServer, params=mapParams)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.mapFile = "map.png"
        with open(self.mapFile, "wb") as file:
            file.write(response.content)
            file.close()

    def updateMap(self):
        self.getImage()
        self.pixmap = QPixmap(self.mapFile)
        self.image.setPixmap(self.pixmap)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.scale = min(17, self.scale + 1)
        if event.key() == Qt.Key_PageDown:
            self.scale = max(0, self.scale - 1)
        self.updateMap()

    def initUI(self):
        self.setGeometry(100, 100, *screenSize)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.mapFile)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
        self.show()

    def closeEvent(self, event):
        os.remove(self.mapFile)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
