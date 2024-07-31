import sys
import os
import main
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QMessageBox, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtGui import QIcon
from function import read_json, get_file_path, read_random_data_from_excel, read_random_data_from_csv

class child_page(QWidget):

    if os.path.exists("temp.json"):
        os.remove("temp.json")

    def __init__(self):
        super(child_page, self).__init__()
        self.button_slide = QPushButton("开始")
        self.button_clear = QPushButton("清除记录")
        self.button_confirm = QPushButton("查看答案")
        self.button_exitToMain = QPushButton("返回")
        self.label_explain = QLabel()
        self.label_word = QLabel()
        self.label_answer = QLabel()
        self.layout_init()
        self.wordlist = self.initial_wordlist()
        self.record = []

    def confirm(self):
        # 查看答案和隐藏互相转换
        text = self.button_confirm.text()
        if text == "查看答案":
            self.label_answer.setStyleSheet(self.style_list()["answer_press"])
            self.button_confirm.setText("隐藏")
        elif text == "隐藏":
            self.label_answer.setStyleSheet(self.style_list()["answer"])  # 设置label样式
            self.button_confirm.setText("查看答案")

    def randomword(self):
        # 开始出题
        self.button_confirm.setText("查看答案")
        if len(self.wordlist) == 0:
            QMessageBox.information(self, "提示", "读取出错，请退出并重新选择列表")
            return 0
        if True:
            # TODO 后续可加上重复出题模式
            if len(self.record) == len(self.wordlist):
                QMessageBox.information(self, "提示", "全部抽取完毕")
                return 0
            word_turkle = self.wordlist[random.randint(0, len(self.wordlist)-1)]
            while word_turkle in self.record:
                word_turkle = self.wordlist[random.randint(0, len(self.wordlist) - 1)]
            self.record.append(word_turkle)
        self.label_word.setText(word_turkle[0])
        self.label_answer.setText(f"{word_turkle[1]}\n[备注：{word_turkle[2]}]")
        self.label_answer.setStyleSheet(self.style_list()["answer"])

    def initial_wordlist(self):
        # 初始化列表，获取单词列表
        file_path = get_file_path()
        if ".xlsx" in file_path:
            return read_random_data_from_excel(file_path)
        elif ".csv" in file_path:
            return read_random_data_from_csv(file_path)
        else:
            return []

    def clear(self):
        # 清除记录：文本、答案清空，记录清空
        self.label_word.setText("")
        self.label_answer.setText("")
        self.label_answer.setStyleSheet(self.style_list()["answer"])
        self.record = []

    def layout_init(self):
        def pagesetting():
            vbox = QVBoxLayout()
            vbox.addWidget(self.label_explain)
            vbox.addSpacing(20)
            vbox.addWidget(self.label_word)
            vbox.addSpacing(20)
            vbox.addWidget(self.label_answer)
            vbox.addSpacing(20)
            hbox = QHBoxLayout()
            hbox.addWidget(self.button_slide)
            hbox.addWidget(self.button_confirm)
            hbox.addWidget(self.button_clear)
            hbox.addWidget(self.button_exitToMain)
            vbox.addLayout(hbox)
            vbox.addStretch(1)
            self.setLayout(vbox)
        def stylesetting():
            styles = self.style_list()
            window_style = styles["window"]
            label_style = styles["label"]
            answer_style = styles["answer"]
            button_style = styles["button"]

            self.resize(960, 540)
            self.move(300, 300)
            self.setWindowTitle("Slide_main")  # 设置界面
            self.setObjectName("SlideWindow")
            self.setWindowIcon(QIcon(os.path.join(os.path.join(os.getcwd(), "icon"), "slide.ico")))
            self.setStyleSheet(window_style)

            self.label_explain.setMinimumHeight(100)
            self.label_explain.setWordWrap(True)
            self.label_explain.setAlignment(Qt.AlignCenter)
            self.label_explain.setText("本程序是自我检查程序，点击“开始”随机抽取，点击“查看答案”查看答案，\n点击“清除记录”清除之前抽取记录，点击“返回”或者叉号返回主界面")
            self.label_explain.setStyleSheet("QLabel{font-size:20px;}")

            self.label_word.setMinimumHeight(100)
            self.label_word.setWordWrap(True)
            self.label_word.setAlignment(Qt.AlignCenter)
            self.label_word.setStyleSheet(label_style)  # 设置label样式

            self.label_answer.setMinimumHeight(150)
            self.label_answer.setWordWrap(True)
            self.label_answer.setAlignment(Qt.AlignCenter)
            self.label_answer.setStyleSheet(answer_style)  # 设置label样式

            for name, function in zip([self.button_slide, self.button_clear, self.button_confirm, self.button_exitToMain],
                                      [self.randomword, self.clear, self.confirm, self.close]):
                name.clicked.connect(function)
                name.setStyleSheet(button_style)

        pagesetting()
        stylesetting()

    def closeEvent(self,event):
        self.close()
        self.main_window = main.parent_page()
        self.main_window.show()

    def set_button_style(self, name, function):
        # 设置按钮样式
        button = QPushButton(name)
        button.clicked.connect(function)
        button.setMinimumHeight(50)
        return button

    def style_list(self):
        data = read_json()['slide']
        window_background_color = data["window_background_color"]
        label_background_color = data["label_background_color"]
        label_font_size = data["label_font_size"]
        answer_background_color = data["answer_background_color"]
        answer_press_color = data["answer_background_press_color"]
        answer_font_size = data["answer_font_size"]
        button_background_color = data["button_background_color"]
        button_font_size = data["button_font_size"]
        button_padding = data["button_padding"]
        button_border_radius = data["button_border_radius"]
        button_pressed_color = data["button_pressed_color"]

        label_style = f"QLabel{{font-size:{label_font_size}px; background-color:{label_background_color}; font-weight:normal;}}"
        answer_style = f"QLabel{{background-color:{answer_background_color}; }}"
        answer_press_style = f"QLabel{{background-color:{answer_press_color}; font-size:{answer_font_size}px; }}"
        button_style = f"QPushButton{{font-size:{button_font_size}px;padding:{button_padding}px;border-radius:{button_border_radius}px;background-color:{button_background_color}}}" \
                       f"QPushButton:pressed{{background-color:{button_pressed_color}}}"
        window_style = f"#SlideWindow{{background-color:{window_background_color}}}"
        return {"label":label_style, "answer":answer_style, "answer_press":answer_press_style, "button":button_style, "window":window_style}

def index():
    page = QApplication(sys.argv)
    win = child_page()
    win.show()
    sys.exit(page.exec())

if __name__ == '__main__':
    index()