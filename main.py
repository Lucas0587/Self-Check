import sys
import os
import slide, SingleChoose, setting
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtGui import QIcon
from function import read_json

class parent_page(QWidget):

    if os.path.exists("temp.json"):
        os.remove("temp.json")

    def __init__(self,parent=None):
        super(parent_page, self).__init__(parent)
        self.show_message_box = True
        self.label_title = QLabel("Slide自查器")
        self.label_combox = QLabel("请在右侧选择需要的功能")
        self.combox=QComboBox()
        self.label_choose_path=QLabel("请选择需要使用的文档，\n若不选择则默认选择模板文档")
        self.button_choose = QPushButton("选择")
        self.label_tip_path = QLabel("文件路径为：")
        self.label_filepath = QLabel()
        self.button_start = QPushButton("开始")
        self.button_exit = QPushButton("退出")
        self.button_setting = QPushButton("设置")
        self.label_version = QLabel("版本号：1.3.0")
        self.layout_init()

    def informationtxt(self, fpath):
        # 保存路径信息
        txt_path = os.path.join(os.getcwd(), "information.txt")
        with open(txt_path, "w", encoding="utf-8") as file:
            file.write(fpath)

    def closeEvent(self, event):
        if self.show_message_box:
            reply = QMessageBox.question(self, '确认退出', "确定要退出吗？", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if os.path.exists("information.txt"):
                    os.remove("information.txt")
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def choose(self):
        # 选择文件路径
        file = QFileDialog.getOpenFileNames(None, '选择文件', os.getcwd(), "All Files(*);;Text Files(*.txt)")
        fpath = str(file[0]).replace('/', '\\').replace('\'', ' ').replace('[', ' ').replace(']', ' ').strip()
        fname = os.path.basename(fpath)
        if ".xlsx" not in fname and ".csv" not in fname:
            QMessageBox.warning(self, "警告", "选择的不是excel文件")
        else:
            self.label_filepath.setText(fpath)
            self.informationtxt(fpath)

    def start(self):
        # 开启两个页面
        # 设置跳转时不弹出QMessageBox窗口
        self.show_message_box = False
        text=self.combox.currentText()
        if text=="\n问题猜答案\n":
            self.index_ui=slide.child_page()
            self.index_ui.show()
            self.close()
        elif text=="\n单项选择\n":
            self.index_ui = SingleChoose.child_page_two()
            self.index_ui.show()
            self.close()

    def set_page(self):
        # 设置页面
        self.show_message_box = False
        self.setting_ui = setting.SettingsWindow()
        self.setting_ui.show()
        self.close()

    def layout_init(self):
        def pagesetting():
            vbox = QVBoxLayout()

            hbox1 = QHBoxLayout()
            hbox1.addWidget(self.label_combox)
            hbox1.addWidget(self.combox)

            hbox2 = QHBoxLayout()
            hbox2.addWidget(self.label_choose_path)
            hbox2.addWidget(self.button_choose)

            hbox3 = QHBoxLayout()
            hbox3.addWidget(self.label_tip_path)
            hbox3.addWidget(self.label_filepath)

            hbox4 = QHBoxLayout()
            hbox4.addWidget(self.button_start)
            hbox4.addSpacing(40)
            hbox4.addWidget(self.button_exit)
            hbox4.addSpacing(40)
            hbox4.addWidget(self.button_setting)

            vbox.addWidget(self.label_title)
            vbox.addSpacing(20)
            vbox.addLayout(hbox1)
            vbox.addSpacing(20)
            vbox.addLayout(hbox2)
            vbox.addSpacing(20)
            vbox.addLayout(hbox3)
            vbox.addSpacing(20)
            vbox.addLayout(hbox4)
            vbox.addSpacing(20)
            vbox.addWidget(self.label_version)

            self.setLayout(vbox)

        def stylesetting():
            data = read_json()['main']
            label_font_size = data["label_font_size"]
            title_background_color = data["title_background_color"]
            title_font_size = data["title_font_size"]
            button_font_size = data["button_font_size"]
            button_padding = data["button_padding"]
            button_border_radius = data["button_border_radius"]
            button_background_color = data["button_background_color"]
            button_pressed_color = data["button_pressed_color"]
            filepath_font_size = data["filepath_font_size"]
            window_background_color = data["window_background_color"]

            label_style = f"QLabel{{font-size:{label_font_size}px}}"
            title_style = f"QLabel{{background-color:{title_background_color};font-size:{title_font_size}px;padding:20px}}"
            button_style = f"QPushButton{{font-size:{button_font_size}px;padding:{button_padding}px;border-radius:{button_border_radius}px;background-color:{button_background_color}}}" \
                           f"QPushButton:pressed{{background-color:{button_pressed_color}}}"
            filepath_style = f"QLabel{{background-color:#ffffff;font-size:{filepath_font_size}px}}"
            window_style = f"#MainWindow{{background-color:{window_background_color}}}"

            self.move(300, 300)
            self.setMinimumWidth(720)
            self.setWindowTitle("主窗口")
            self.setObjectName("MainWindow")
            self.setWindowIcon(QIcon(os.path.join(os.path.join(os.getcwd(), "icon"), "main.ico")))
            self.setStyleSheet(window_style)

            self.label_title.setAlignment(Qt.AlignCenter)
            self.label_title.setStyleSheet(title_style)

            self.label_combox.setAlignment(Qt.AlignCenter)
            self.label_combox.setStyleSheet(label_style)

            self.combox.addItems(["\n问题猜答案\n", "\n单项选择\n"])
            self.combox.setMinimumHeight(60)
            self.combox.setStyleSheet("QComboBox{font-size:20px;}")

            self.label_choose_path.setAlignment(Qt.AlignCenter)
            self.label_choose_path.setStyleSheet(label_style)

            self.button_choose.clicked.connect(self.choose)
            self.button_choose.setStyleSheet(button_style)

            self.label_tip_path.setStyleSheet(label_style)

            if os.path.exists("information.txt"):
                with open("information.txt", "r", encoding="utf-8") as f:
                    text_path = f.readline()
                    self.label_filepath.setText(text_path)
            self.label_filepath.setContentsMargins(15, 5, 5, 5)
            self.label_filepath.setStyleSheet(filepath_style)

            self.button_start.clicked.connect(self.start)
            self.button_start.setStyleSheet(button_style)

            self.button_exit.clicked.connect(self.close)
            self.button_exit.setStyleSheet(button_style)

            self.button_setting.setStyleSheet(button_style)
            self.button_setting.clicked.connect(self.set_page)

            self.label_version.setStyleSheet(label_style)

        pagesetting()
        stylesetting()

def main():
    page = QApplication(sys.argv)
    win = parent_page()
    win.show()
    sys.exit(page.exec())

if __name__ == '__main__':
    main()