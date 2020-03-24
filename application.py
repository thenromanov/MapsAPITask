import os
import sys
import requests
from copy import copy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mapModule import *

screenSize = (600, 450)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coords = [37.618909, 55.751400]
        self.scale = 15
        self.type = 'map'
        self.point = []
        self.getImage()
        self.initUI()

    def getImage(self):
        mapServer = 'http://static-maps.yandex.ru/1.x/'
        mapParams = {
            'll': ','.join(map(str, self.coords)),
            'z': str(self.scale),
            'l': self.type
        }
        if len(self.point) > 0:
            mapParams['pt'] = '{},{},comma'.format(self.point[0], self.point[1])
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

        mapActoin = QAction(QIcon('data/map.png'), 'Карта', self)
        mapActoin.triggered.connect(self.toMap)
        typeMap = self.addToolBar('Карта')
        typeMap.addAction(mapActoin)

        satelliteAction = QAction(QIcon('data/satellite.png'), 'Спутник', self)
        satelliteAction.triggered.connect(self.toSatellite)
        typeSatellite = self.addToolBar('Спутник')
        typeSatellite.addAction(satelliteAction)

        hybridAction = QAction(QIcon('data/hybrid.png'), 'Гибрид', self)
        hybridAction.triggered.connect(self.toHybrid)
        typeHybrid = self.addToolBar('Гибрид')
        typeHybrid.addAction(hybridAction)

        searchAction = QAction(QIcon('data/search.png'), 'Поиск', self)
        searchAction.triggered.connect(self.search)
        search = self.addToolBar('Поиск')
        search.addAction(searchAction)

        clearAction = QAction(QIcon('data/cross.png'), 'Очистить', self)
        clearAction.triggered.connect(self.clear)
        clear = self.addToolBar('Очистить')
        clear.addAction(clearAction)

        self.show()

    def search(self):
        address, okBtnPressed = QInputDialog.getText(self, 'Введите адрес', 'Введите адрес')
        if okBtnPressed:
            coords = getAddressCoords(address)
            if coords:
                self.coords = coords[0].copy()
                self.point = coords[0].copy()
                self.updateMap()

    def clear(self):
        self.point = []
        self.updateMap()

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
