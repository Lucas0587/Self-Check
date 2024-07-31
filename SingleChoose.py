import sys
import random
import os
import main
from function import read_json, get_file_path, read_random_data_from_excel, read_random_data_from_csv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QMessageBox, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtGui import QIcon

class child_page_two(QWidget):

    if os.path.exists("temp.json"):
        os.remove("temp.json")

    def __init__(self):
        super(child_page_two, self).__init__()
        self.button_slide = QPushButton("开始")
        self.button_clear = QPushButton("清除")
        self.button_exit= QPushButton("退出")
        self.button_A = QPushButton("请点击“开始”开始")
        self.button_B = QPushButton("请点击“开始”开始")
        self.button_C = QPushButton("请点击“开始”开始")
        self.button_D = QPushButton("请点击“开始”开始")
        self.label_explain = QLabel()
        self.label_word = QLabel()
        self.label_right=QLabel()
        self.label_tip=QLabel()

        self.styles = self.style_list()
        self.button_right_style = self.styles["right"]
        self.button_wrong_style = self.styles["wrong"]
        self.non_repeat_check = self.styles["check"]

        self.wordlist = self.initial_wordlist()
        self.record = []
        self.right_num = 0
        self.wrong_num = 0

        self.layout_init()

    def initial_wordlist(self):
        file_path = get_file_path()
        if ".xlsx" in file_path:
            return read_random_data_from_excel(file_path)
        elif ".csv" in file_path:
            return read_random_data_from_csv(file_path)
        else:
            return []

    def set_choice(self, turkle):
        keys = [self.button_A, self.button_B, self.button_C, self.button_D]
        random_letters = random.sample(keys, len(turkle))
        result_dict = {letter: num for num, letter in zip(turkle, random_letters)}
        for key, value in result_dict.items():
            key.setText(self.wordlist[value][1])
        self.label_word.setText(self.wordlist[turkle[0]][0])

    def clear_all(self):
        self.record = []
        buttons = [self.button_A, self.button_B, self.button_C, self.button_D]
        for button in buttons:
            button.setStyleSheet(self.styles["button"])
            button.setText("请点击“开始”开始")
        self.label_word.setText("")
        self.label_tip.setText("")
        self.right_num, self.wrong_num = 0, 0
        self.label_right.setText(f"你答对了{self.right_num}道题，答错了{self.wrong_num}道题")

    def randomword(self):
        buttons = [self.button_A, self.button_B, self.button_C, self.button_D]
        for button in buttons:
            button.setStyleSheet(self.styles["button"])
            button.setEnabled(True)
        if len(self.wordlist) == 0:
            QMessageBox.information(self, "提示", "读取出错，请退出并重新选择列表")
            return 0

        self.turkle = random.sample(range(len(self.wordlist)), 4)
        if self.non_repeat_check == True:
            if len(self.record) == len(self.wordlist):
                reply = QMessageBox.question(self, '提示', "全部抽取完毕，是否重新开始抽取？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.clear_all()
                return 0
            while self.turkle[0] in self.record:
                self.turkle = random.sample(range(len(self.wordlist)), 4)
            self.record.append(self.turkle[0])
        self.set_choice(self.turkle)

        self.label_tip.setText("")

    def checkans(self):
        sender = self.sender().text()
        if sender == "请点击“开始”开始":
            self.randomword()
            return 0
        buttons = [self.button_A, self.button_B, self.button_C, self.button_D]
        for button in buttons:
            button.setEnabled(False)
        if sender == self.wordlist[self.turkle[0]][1]:
            self.sender().setStyleSheet(self.button_right_style)
            self.right_num += 1
        else:
            self.sender().setStyleSheet(self.button_wrong_style)
            for button in buttons:
                if button.text() == self.wordlist[self.turkle[0]][1]:
                    button.setStyleSheet(self.button_right_style)
            self.wrong_num += 1
        accuracy = self.right_num / (self.right_num + self.wrong_num)
        self.label_right.setText(f"你答对了{self.right_num}道题，答错了{self.wrong_num}道题，正确率{accuracy:.2%}")
        self.label_tip.setText(self.wordlist[self.turkle[0]][2])

    def closeEvent(self,event):
        self.close()
        self.main_window = main.parent_page()
        self.main_window.show()

    def layout_init(self):
        def pagesetting():
            vbox = QVBoxLayout()
            vbox.addWidget(self.label_explain)
            vbox.addStretch(1)
            vbox.addWidget(self.label_word)
            vbox.addStretch(1)
            hbox1 = QHBoxLayout()
            hbox1.addWidget(self.button_A)
            hbox1.addWidget(self.button_B)
            vbox.addLayout(hbox1)
            hbox2 = QHBoxLayout()
            hbox2.addWidget(self.button_C)
            hbox2.addWidget(self.button_D)
            vbox.addLayout(hbox2)
            vbox.addStretch(1)
            vbox.addWidget(self.label_tip)
            vbox.addStretch(1)
            hbox3 = QHBoxLayout()
            hbox3.addWidget(self.button_slide)
            hbox3.addWidget(self.button_clear)
            hbox3.addWidget(self.button_exit)
            vbox.addLayout(hbox3)
            vbox.addStretch(1)
            vbox.addWidget(self.label_right)
            self.setLayout(vbox)
        def stylesetting():
            window_style = self.styles["window"]
            label_style = self.styles["label"]
            answer_style = self.styles["answer"]
            button_style = self.styles["button"]

            self.setStyleSheet(window_style)

            self.label_explain.setWordWrap(True)
            self.label_explain.setAlignment(Qt.AlignCenter)
            self.label_explain.setText("选择题")
            self.label_explain.setStyleSheet("QLabel{font-size:20px;}")
            self.label_explain.setMinimumHeight(50)

            self.label_word.setWordWrap(True)
            self.label_word.setAlignment(Qt.AlignCenter)
            self.label_word.setStyleSheet(label_style)
            self.label_word.setMinimumHeight(80)

            self.label_right.setWordWrap(True)
            self.label_right.setText(f"你答对了{self.right_num}道题，答错了{self.wrong_num}道题")
            self.label_right.setStyleSheet(label_style)

            self.label_tip.setWordWrap(True)
            self.label_tip.setStyleSheet(answer_style)
            self.label_tip.setMinimumHeight(100)

            for name, function in zip([self.button_slide, self.button_exit, self.button_clear],
                                      [self.randomword, self.close, self.clear_all]):
                name.setStyleSheet(button_style)
                name.setMinimumHeight(40)
                name.clicked.connect(function)

            for name in [self.button_A, self.button_B, self.button_C, self.button_D]:
                name.setStyleSheet(button_style)
                name.setMinimumHeight(50)
                name.clicked.connect(self.checkans)

        self.move(300, 300)
        self.resize(960,540)
        icon_path=os.getcwd()
        self.setWindowIcon(QIcon(os.path.join(os.path.join(os.getcwd(), "icon"), "singlechoose.ico")))
        self.setWindowTitle("单选窗口")
        self.setObjectName("SingleChooseWindow")
        pagesetting()
        stylesetting()

    def style_list(self):
        data = read_json()["single"]
        window_background_color = data["window_background_color"]
        label_font_size = data["label_font_size"]
        label_background_color = data["label_background_color"]
        answer_font_size = data["answer_font_size"]
        answer_background_color = data["answer_background_color"]
        button_font_size = data["button_font_size"]
        button_padding = data["button_padding"]
        button_border_radius = data["button_border_radius"]
        button_background_color = data["button_background_color"]
        button_pressed_color = data["button_pressed_color"]
        button_right_color = data["button_right_color"]
        button_wrong_color = data["button_wrong_color"]
        non_repeat_check = data["non_repeat_check"]

        label_style = f"QLabel{{font-size:{label_font_size}px; background-color:{label_background_color}; font-weight:normal;}}"
        answer_style = f"QLabel{{background-color:{answer_background_color}; font-size:{answer_font_size}px; }}"
        button_style = f"QPushButton{{font-size:{button_font_size}px;padding:{button_padding}px;border-radius:{button_border_radius}px;background-color:{button_background_color}}}" \
                       f"QPushButton:pressed{{background-color:{button_pressed_color}}}"
        button_right_style = f"QPushButton{{font-size:{button_font_size}px;padding:{button_padding}px;border-radius:{button_border_radius}px;background-color:{button_right_color}}}"
        button_wrong_style = f"QPushButton{{font-size:{button_font_size}px;padding:{button_padding}px;border-radius:{button_border_radius}px;background-color:{button_wrong_color}}}"
        window_style = f"#SingleChooseWindow{{background-color:{window_background_color}}}"
        return {"label":label_style, "answer":answer_style, "button":button_style, "window":window_style,
                "right":button_right_style, "wrong":button_wrong_style, "check":non_repeat_check}

def index():
    page = QApplication(sys.argv)
    win = child_page_two()
    win.show()
    sys.exit(page.exec())

if __name__ == '__main__':
    index()