import os
import sys
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

screenSize = (600, 450)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coords = [37.618909, 55.751400]
        self.scale = 15
        self.type = 'map'
        self.getImage()
        self.initUI()

    def getImage(self):
        mapServer = 'http://static-maps.yandex.ru/1.x/'
        mapParams = {
            'll': ','.join(map(str, self.coords)),
            'z': str(self.scale),
            'l': self.type
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
        elif event.key() == Qt.Key_PageDown:
            self.scale = max(4, self.scale - 1)
        elif event.key() == Qt.Key_Right:
            self.coords[0] += 844 / 2 ** self.scale
            if self.coords[0] > 180:
                self.coords[0] -= 360
        elif event.key() == Qt.Key_Left:
            self.coords[0] -= 844 / 2 ** self.scale
            if self.coords[0] < -180:
                self.coords[0] += 360
        elif event.key() == Qt.Key_Up:
            self.coords[1] += 360 / 2 ** self.scale
            if self.coords[1] > 90:
                self.coords[1] -= 180
        elif event.key() == Qt.Key_Down:
            self.coords[1] -= 360 / 2 ** self.scale
            if self.coords[1] < -90:
                self.coords[1] += 180
        self.updateMap()

    def initUI(self):
        self.setGeometry(100, 100, *screenSize)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.mapFile)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        menu = self.menuBar()
        mapType = menu.addMenu('Тип карты')

        typeMap = QAction('Карта', self)
        mapType.addAction(typeMap)
        typeMap.triggered.connect(self.toMap)

        typeSatellite = QAction('Спутник', self)
        mapType.addAction(typeSatellite)
        typeSatellite.triggered.connect(self.toSatellite)

        typeHybrid = QAction('Гибрид', self)
        mapType.addAction(typeHybrid)
        typeHybrid.triggered.connect(self.toHybrid)

        self.show()

    def toMap(self):
        self.type = 'map'
        self.updateMap()

    def toSatellite(self):
        self.type = 'sat'
        self.updateMap()

    def toHybrid(self):
        self.type = 'sat,skl'
        self.updateMap()

    def closeEvent(self, event):
        os.remove(self.mapFile)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
