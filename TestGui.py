# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'superv1.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import sys, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QAbstractItemView

SPEED = 2
TIME_FLOW = 1 / SPEED


class BackendThread(QtCore.QObject):
    update_date = QtCore.pyqtSignal(list, list)

    def __init__(self, MainProcess, *args, **kwargs):
        self.main_process = MainProcess
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            self.main_process.update()
            r = self.main_process.RESOURCES_PANEL
            c = self.main_process.TECHNOLOGIST_PANEL
            self.update_date.emit(r, c)
            time.sleep(TIME_FLOW)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, MainProcess, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_process = MainProcess
        self.init_game_loop()

        self.ZONING_BUTTONS = list()
        self.TECHNOLOGISTS_BUTTONS = {
            'military': {'rate': None, 'T': None},
            'civil': {'rate': None, 'T': None},
            'beyond': {'rate': None, 'T': None}
        }
        self.TECHNOLOGISTS_LABELS = {
            'military': None,
            'civil': None,
            'beyond': None
        }

        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(850, 315, 148, 285))
        self.textBrowser.setObjectName("textBrowser")

        self.RESOURCES_PANEL = None
        self.TECHNOLOGIST_PANEL = None
        self.WAT_SELECT_LIST = None

        self.init()
        self.init_all_widget()

        self.show()

    def init(self):
        self.resize(1000, 600)
        self.setMinimumSize(QtCore.QSize(1000, 600))
        self.setMaximumSize(QtCore.QSize(1000, 600))
        self.setWindowTitle("SuperContinent")

    def init_zoning_buttons(self):
        # 这段代码毫无意义，但是如果不加上，第一个按钮有点不一样，强迫症表示很不舒服。如果你测试的时候没有其他情况，可能是我脸比较黑
        temp = QtWidgets.QPushButton(self)
        temp.setGeometry(0, 0, 0, 0)
        temp.setText('')
        ##########

        for i in range(6):
            for j in range(6):
                b = QtWidgets.QPushButton(self)

                x = 600 + j * 40
                y = 0 + i * 40

                b.setGeometry(x, y, 50, 50)
                b.setText('')
                self.ZONING_BUTTONS.append(b)

    def init_technologist_buttons(self):
        X_base = 950
        X_instance = 20
        tech_buttons = [
            (0, 250), (1, 250),
            (0, 270), (1, 270),
            (0, 290), (1, 290)
        ]
        keys = [val for val in self.TECHNOLOGISTS_BUTTONS.keys() for i in range(2)]

        for (x, y), key in zip(tech_buttons, keys):
            b = QtWidgets.QPushButton(self)
            b.setGeometry(X_base + X_instance * x, y, 30, 30)
            b.setText('T' if x else ('4' if y == 290 else '3'))

            self.TECHNOLOGISTS_BUTTONS[key]['T' if x else 'rate'] = b

    def init_technologist_labels(self):
        X_base = 850
        Y_base = 256
        Y = [Y_base + i * 20 for i in range(3)]

        style = "font: 10pt ;border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0)"

        for k, y in zip(self.TECHNOLOGISTS_LABELS.keys(), Y):
            label = QtWidgets.QLabel(self)
            label.setGeometry(X_base, y, 100, 18)
            label.setStyleSheet(style)
            label.setText(f"未选科技：{k}")

            self.TECHNOLOGISTS_LABELS[k] = label

    def gen_table(self, row, col, h_size, v_size):
        table = QtWidgets.QTableWidget(self)

        table.setRowCount(row)
        table.setColumnCount(col)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)

        table.horizontalHeader().setVisible(False)
        table.horizontalHeader().setDefaultSectionSize(h_size)
        table.horizontalHeader().setHighlightSections(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(v_size)
        table.verticalHeader().setHighlightSections(False)

        for r in range(row):
            for c, item in enumerate(QtWidgets.QTableWidgetItem() for _ in range(col)):
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(r, c, item)

        return table

    def resource_table_view(self):
        table = self.gen_table(5, 3, 48, 26)
        table.setGeometry(850, 3, 148, 135)

        panels = ("能量", "矿物", "食物", "物资", "合金")
        for row in range(5):
            item = table.item(row, 0)
            item.setText(panels[row])

        for row in range(5):
            for col in range(2):
                item = table.item(row, col + 1)
                item.setText('')

        self.RESOURCES_PANEL = table

    def cs_table_view(self):
        table = self.gen_table(3, 2, 73, 36)
        table.setGeometry(850, 140, 148, 110)
        panels = ("经济", '军事', "科研")

        for row in range(3):
            item = table.item(row, 0)
            item.setText(panels[row])

        for row in range(3):
            data = table.item(row, 1)
            data.setText('')

        self.TECHNOLOGIST_PANEL = table

    def init_wait_select_view(self):
        listView = QtWidgets.QListView(self)
        listView.setGeometry(607, 250, 237, 350)

        self.WAT_SELECT_LIST = listView

    def init_all_widget(self):
        self.init_technologist_buttons()
        self.init_technologist_labels()
        self.init_wait_select_view()
        self.init_zoning_buttons()
        self.resource_table_view()
        self.cs_table_view()

    def update_resource_panel(self, r_panel):
        for r in range(5):
            for c in range(2):
                text = r_panel[r][c]
                self.RESOURCES_PANEL.item(r, c + 1).setText(text)

    def update_technolgoist_panel(self, c_panel):
        for r in range(3):
            text = c_panel[r]
            self.TECHNOLOGIST_PANEL.item(r, 1).setText(text)

    def update_panel(self, r, c):
        self.update_resource_panel(r)
        self.update_technolgoist_panel(c)
        self.update()

    def init_game_loop(self):
        self.backend = BackendThread(self.main_process)

        self.backend.update_date.connect(self.update_panel)
        self.thread = QtCore.QThread()
        self.backend.moveToThread(self.thread)

        self.thread.started.connect(self.backend.run)
        self.thread.start()


class Sender(QtCore.QObject):
    RESOURCES_PANEL = [
        ("1000", "-200"), ("2000", "+312"), ("2000", "+100"), ("100000", "+30"), ("20000", "-10")
    ]
    TECHNOLOGIST_PANEL = [None, None, "1M"]

    def update_resource_panel(self):
        def g():
            for s, m in self.RESOURCES_PANEL:
                store = int(s)
                monthly = int(m)
                store += monthly
                return str(store), str(monthly)

        self.RESOURCES_PANEL = [i for i in g()]

    def update_technology_panel(self):
        sum = 0
        for s, m in self.RESOURCES_PANEL:
            sum += int(s) + int(m) * 10
            


# def update(self, r=None, t=None):
#     if r:
#         self.RESOURCES_PANEL = r[:]
#     if t:
#         self.TECHNOLOGIST_PANEL = t[:]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = MainWindow(Sender())

    sys.exit(app.exec_())
