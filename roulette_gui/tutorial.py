import sys

import numpy as np
from PyQt5.QtCore import QDate, Qt, QTime, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLabel, QWidget, \
    QLineEdit, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem


class RouletteApp(QWidget):
    def __init__(self):
        super().__init__()
        # self.toolbar = None
        self.pick_result = None
        self.clear_btn = None
        self.del_btn = None
        self.add_btn = None
        self.pick_btn = None
        self.table = None
        self.picked_item = None
        self.input_box = None
        self.pick_list = []
        self.on_click_idx = -1
        self.init_ui()
        return

    def init_ui(self):
        # 레이아웃 구성
        # 구성 요소 생성
        self.add_btn = QPushButton('add', self)  # 뽑기 리스트 추가
        self.del_btn = QPushButton('del', self)  # 뽑기 리스트 1개 삭제
        self.clear_btn = QPushButton('clear', self)  # 초기화
        self.pick_result = QLabel('pick result', self)  # 뽑기 결과 안내(result)
        self.picked_item = QLabel('picked item', self)  # 뽑힌 아이템
        self.pick_btn = QPushButton('pick', self)  # 뽑기
        self.input_box = QLineEdit(self)
        self.table = QTableWidget()

        # 단축키 설정
        # add_btn.setShortcut('Enter')
        self.del_btn.setShortcut('Ctrl+D')
        self.clear_btn.setShortcut('F5')
        self.pick_btn.setShortcut('Ctrl+P')

        # 구성 요소 스타일 설정
        self.pick_result.setAlignment(Qt.AlignCenter)
        self.picked_item.setAlignment(Qt.AlignCenter)

        pi_font = self.picked_item.font()
        pi_font.setPointSize(20)
        self.picked_item.setFont(pi_font)

        general_font = self.add_btn.font()
        general_font.setPointSize(12)
        self.pick_result.setFont(general_font)
        self.add_btn.setFont(general_font)
        self.del_btn.setFont(general_font)
        self.clear_btn.setFont(general_font)
        self.pick_btn.setFont(general_font)
        self.input_box.setFont(general_font)

        self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 구성 요소에 기능 연결
        self.input_box.editingFinished.connect(self.on_entered)
        self.add_btn.clicked.connect(self.on_entered)
        self.del_btn.clicked.connect(self.btn_del)
        self.clear_btn.clicked.connect(self.btn_clear)
        self.pick_btn.clicked.connect(self.pick)
        self.table.cellDoubleClicked.connect(self.cell_double_clicked)
        self.table.cellClicked.connect(self.cell_clicked)

        # 레이아웃 생성
        big_hbox = QHBoxLayout()
        left_vbox = QVBoxLayout()
        right_vbox = QVBoxLayout()
        left_small_hbox = QHBoxLayout()

        # 레이아웃에 구성 요소 배치
        left_small_hbox.addWidget(self.add_btn)
        left_small_hbox.addStretch(1)
        left_small_hbox.addWidget(self.del_btn)
        left_small_hbox.addStretch(1)
        left_small_hbox.addWidget(self.clear_btn)

        left_vbox.addStretch(1)
        left_vbox.addWidget(self.table)
        left_vbox.addStretch(1)
        left_vbox.addWidget(self.input_box)
        left_vbox.addStretch(1)
        left_vbox.addLayout(left_small_hbox)
        left_vbox.addStretch(1)

        right_vbox.addStretch(1)
        right_vbox.addWidget(self.pick_result)
        right_vbox.addStretch(1)
        right_vbox.addWidget(self.picked_item)
        right_vbox.addStretch(1)
        right_vbox.addWidget(self.pick_btn)
        right_vbox.addStretch(1)

        # 레이아웃 조립
        big_hbox.addStretch(1)
        big_hbox.addLayout(left_vbox)
        big_hbox.addStretch(1)
        big_hbox.addLayout(right_vbox)
        big_hbox.addStretch(1)

        # 레이아웃 적용
        self.setLayout(big_hbox)

        # 창 하단에 상태바 표시
        # self.statusBar().showMessage('start application', 3000)  # 창 하단에 상태바 표시, 시간 제한
        # self.statusBar().clearMessage()  # 상태바 메시지 삭제

        # 날짜, 시간 표시
        now = QDate.currentDate()
        # print(now.toString('yyyy-MM-dd(ddd)'))
        print(now.toString(Qt.ISODate))
        # print(now.toString(Qt.DefaultLocaleLongDate))
        time = QTime.currentTime()
        print(time.toString(Qt.DefaultLocaleShortDate))
        print(f'{now.toString(Qt.ISODate)} {time.toString(Qt.DefaultLocaleShortDate)}')
        datetime = QDateTime.currentDateTime()
        print(datetime.toString(Qt.DefaultLocaleShortDate))

        # 창 상단 메뉴 바 구성 세부 메뉴
        # exit
        # exit_action = QAction(QIcon('fabicon/ms-icon-310x310.png'), 'Exit', self)  # 액션 추가
        # exit_action.setShortcut('Ctrl+Q')  # 단축기 설정
        # exit_action.setStatusTip('Exit application')  # 메뉴에 마우스 올리면 하단에 나오는 설명
        # exit_action.triggered.connect(qApp.quit)  # 앱과 동작 연결

        # 화면에 종료 버튼 추가
        # btn = QPushButton(f'{now.toString(Qt.ISODate)}', self)  # 메인 창에 버튼 생성, 버튼에 쓰일 문자열 초기화
        # btn.setToolTip(f'{now.toString(Qt.ISODate)} {time.toString(Qt.DefaultLocaleShortDate)}')  # 버튼 툴팁 입력
        # btn.setStatusTip('Exit application')  # 메뉴에 마우스 올리면 하단에 나오는 설명
        # btn.move(50, 100)  # 버튼 위치
        # btn.resize(btn.sizeHint())  # 버튼 사이즈
        # btn.clicked.connect(QCoreApplication.instance().quit)  # 버튼을 누르면 일어날 동작

        # 메인 창
        # 메뉴 바 구성
        # self.statusBar()  # 창 상태바 생성
        # menubar = self.menuBar()
        # menubar.setNativeMenuBar(False)  # OS에 상관 없이 동일한 UI 적용
        # file_menu = menubar.addMenu('&action')  # 메뉴 바에 메뉴 추가
        # file_menu.addAction(exit_action)  # 메뉴 바 메뉴에 세부 메뉴 연결
        # 툴바
        # self.toolbar = self.addToolBar('Exit')  # 툴바 추가
        # self.toolbar.addAction(exit_action)  # 추가한 툴바에 액션 연결
        # 기타 구성
        self.setToolTip('This is a <b>QWidget</b> widget')  # 메인 창에 툴팁 입력
        # self.setFont(QFont('System', 12))  # 폰트 설정
        self.setWindowTitle('roulette')  # 창 제목
        self.setWindowIcon(QIcon('fabicon/ms-icon-310x310.png'))  # 창 아이콘 지정
        # self.move(300, 300)  # 위젯 위치 지정
        self.resize(1200, 800)  # 위젯 크기 지정
        # self.setGeometry(400, 250, 800, 500)  # 창의 위치와 크기 지정: 앞의 두 파라미터는 위치, 뒤는 크기
        self.center()  # 창이 화면 가운데 생성됨

        # 창 보여주기
        self.show()  # 화면에 위젯 표시

        return

    def center(self):  # 창이 화면 가운데 생성되게 함
        qr = self.frameGeometry()  # 창의 위치와 크기 정보 가져와서 똑같이 생긴 사각형 생성
        cp = QDesktopWidget().availableGeometry().center()  # 모니터 화면의 가운데 위치 파악
        qr.moveCenter(cp)  # 사각형을 화면 가운데로 이동
        self.move(qr.topLeft())  # 창을 사각형이 있는 위치로 이동
        return

    def on_entered(self):
        if len(self.input_box.text()) < 1:
            return
        self.pick_list.append(self.input_box.text())
        self.update_table()
        self.input_box.setText('')
        return

    def update_table(self):
        if len(self.pick_list) < 1:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(""))
            return
        self.table.setRowCount(len(self.pick_list))
        self.table.setColumnCount(1)
        for i in range(len(self.pick_list)):
            self.table.setItem(i, 0, QTableWidgetItem(self.pick_list[i]))
        return

    def pick(self):
        if len(self.pick_list) < 1:
            self.picked_item.setText('ERROR: no item')
            return
        idx = int(np.random.uniform(low=0, high=len(self.pick_list), size=1))
        self.picked_item.setText(self.pick_list[idx])
        return

    def cell_double_clicked(self, row, col):
        del self.pick_list[row]
        self.update_table()
        return

    def cell_clicked(self, row, col):
        self.on_click_idx = row
        return

    def btn_del(self):
        if len(self.pick_list) < 1:
            self.picked_item.setText('ERROR: no item')
            return
        elif self.on_click_idx == -1:
            self.picked_item.setText('ERROR: no select')
            return
        del self.pick_list[self.on_click_idx]
        self.update_table()
        self.on_click_idx = -1
        return

    def btn_clear(self):
        self.pick_list.clear()
        self.update_table()
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 어플리케이션 객체 생성
    ex = RouletteApp()
    sys.exit(app.exec_())
