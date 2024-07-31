import os
import sys
import json
import main, slide, SingleChoose
from function import read_json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, \
    QColorDialog, QSpinBox, QHBoxLayout, QGroupBox,QMessageBox, QCheckBox
from PyQt5.Qt import Qt,QFont

class MainPage(QWidget):
    # 主页面
    def __init__(self, parent=None):
        super().__init__(parent)

        data = read_json()["main"]
        window_background_color = data["window_background_color"]
        label_font_size = data["label_font_size"]
        title_font_size = data["title_font_size"]
        title_background_color = data["title_background_color"]
        button_font_size = data["button_font_size"]
        button_padding = data["button_padding"]
        button_border_radius = data["button_border_radius"]
        button_background_color = data["button_background_color"]
        button_pressed_color = data["button_pressed_color"]
        filepath_font_size = data["filepath_font_size"]

        self.fontsize = [24,18]
        self.btn_color_background = self.set_button_style("选择：页面背景颜色", window_background_color)
        self.spin_page_font_size = self.set_spin_style(label_font_size, 12, 40, "页面字体大小")
        self.spin_title_font_size = self.set_spin_style(title_font_size, 12, 50, "标题字体大小")
        self.button_title_color = self.set_button_style("选择：标题颜色", title_background_color)
        self.spin_button_font_size = self.set_spin_style(button_font_size, 20, 50,"按钮字体大小")
        self.spin_button_margin = self.set_spin_style(button_padding, 0, 20, "按钮边距大小")
        self.spin_button_radius = self.set_spin_style(button_border_radius, 0, 20, "按钮弧度大小")
        self.btn_color_button = self.set_button_style("选择：按钮背景颜色", button_background_color)
        self.btn_color_button_pressed =self.set_button_style("选择：按钮按下颜色", button_pressed_color)
        self.spin_path_font_size = self.set_spin_style(filepath_font_size, 6, 24, "路径字体大小")
        self.preview = self.set_button_style("预览", "#e7e7e7")
        self.set_default = self.set_button_style("设为默认值", "#e7e7e7")
        self.preview.clicked.connect(self.preview_window)

        main_layout = QVBoxLayout(self)

        # 创建页面背景设置的大框
        background_group_box = self.set_label_style("页面背景设置",0)
        background_layout = QVBoxLayout(background_group_box)
        hbox_background1 = QHBoxLayout()
        hbox_background1.addWidget(self.set_label_style("页面背景颜色", 1))
        hbox_background1.addWidget(self.btn_color_background)
        hbox_background1.addStretch(1)
        background_layout.addLayout(hbox_background1)
        hbox_background2 = QHBoxLayout()
        hbox_background2.addWidget(self.set_label_style("字体大小", 1))
        hbox_background2.addWidget(self.spin_page_font_size)
        hbox_background2.addStretch(1)
        background_layout.addLayout(hbox_background2)
        main_layout.addWidget(background_group_box)

        # 创建标题设置的大框
        title_group_box = self.set_label_style("标题设置",0)
        title_layout = QVBoxLayout(title_group_box)
        title_hbox1 = QHBoxLayout()
        title_hbox1.addWidget(self.set_label_style("标题字体大小", 1))
        title_hbox1.addWidget(self.spin_title_font_size)
        title_hbox1.addStretch(1)
        title_layout.addLayout(title_hbox1)
        title_hbox2 = QHBoxLayout()
        title_hbox2.addWidget(self.set_label_style("标题颜色", 1))
        title_hbox2.addWidget(self.button_title_color)
        title_hbox2.addStretch(1)
        title_layout.addLayout(title_hbox2)
        main_layout.addWidget(title_group_box)

        # 创建按钮设置的大框
        button_group_box = self.set_label_style("按钮设置",0)
        button_layout = QVBoxLayout(button_group_box)
        button_hbox1= QHBoxLayout()
        button_hbox1.addWidget(self.set_label_style("按钮字体大小", 1))
        button_hbox1.addWidget(self.spin_button_font_size)
        button_hbox1.addStretch(1)
        button_layout.addLayout(button_hbox1)
        button_hbox2 = QHBoxLayout()
        button_hbox2.addWidget(self.set_label_style("按钮边距", 1))
        button_hbox2.addWidget(self.spin_button_margin)
        button_hbox2.addStretch(1)
        button_layout.addLayout(button_hbox2)
        button_hbox3 = QHBoxLayout()
        button_hbox3.addWidget(self.set_label_style("按钮弧度", 1))
        button_hbox3.addWidget(self.spin_button_radius)
        button_hbox3.addStretch(1)
        button_layout.addLayout(button_hbox3)
        button_hbox4 = QHBoxLayout()
        button_hbox4.addWidget(self.set_label_style("按钮颜色",1))
        button_hbox4.addWidget(self.btn_color_button)
        button_hbox4.addStretch(1)
        button_layout.addLayout(button_hbox4)
        button_hbox5 = QHBoxLayout()
        button_hbox5.addWidget(self.set_label_style("按钮按下颜色",1))
        button_hbox5.addWidget(self.btn_color_button_pressed)
        button_hbox5.addStretch(1)
        button_layout.addLayout(button_hbox5)
        main_layout.addWidget(button_group_box)

        # 创建路径文本设置的大框
        path_group_box = self.set_label_style("路径文本设置",0)
        path_layout = QVBoxLayout(path_group_box)
        path_hbox = QHBoxLayout()
        path_hbox.addWidget(self.set_label_style("路径文本大小", 1))
        path_hbox.addWidget(self.spin_path_font_size)
        path_hbox.addStretch(1)
        path_layout.addLayout(path_hbox)
        main_layout.addWidget(path_group_box)

        main_layout.addWidget(self.preview)
        main_layout.addStretch(1)

    def set_label_style(self,text,type):
        # 设置label样式
        font = QFont()
        if type == 1:
            label = QLabel(text)
            label.setMinimumWidth(150)
            label.setStyleSheet(f"QLabel{{font-size:{self.fontsize[type]}px}}")
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font.setFamily("KaiTi")
            label.setFont(font)
            return label
        elif type == 0:
            groupbox = QGroupBox(text)
            groupbox.setStyleSheet(f"QLabel{{font-size:{self.fontsize[type]}px}}")
            font.setFamily("SimHei")
            groupbox.setFont(font)
            return groupbox

    def set_spin_style(self, value, min, max, name):
        # 设置spin样式
        spin = QSpinBox()
        spin.setValue(int(value))
        spin.setMinimum(min)
        spin.setMaximum(max)
        spin.setMinimumWidth(100)
        spin.setObjectName(name)
        spin.valueChanged.connect(lambda val, obj_name=name: self.onChangeEvent(obj_name, val))
        return spin

    def set_button_style(self,text,color):
        # 设置button样式
        button_style = f"QPushButton{{font-size:20px; padding:5px;border-radius:10px;background-color:{color}}}"
        button = QPushButton(text)
        button.setStyleSheet(button_style)
        button.setObjectName(text)
        if text != "预览" and text !="设为默认值":
            button.clicked.connect(lambda : self.choose_color(button))
        return button

    def onChangeEvent(self, name, change):
        # change事件：每触发change就记录到temp.json
        name_variable_list = {
            "选择：页面背景颜色": "window_background_color", "选择：标题颜色": "title_background_color",
            "选择：按钮背景颜色": "button_background_color", "选择：按钮按下颜色": "button_pressed_color",
            "页面字体大小": "label_font_size", "标题字体大小": "title_font_size", "按钮字体大小": "button_font_size",
            "按钮边距大小": "button_padding", "按钮弧度大小": "button_border_radius", "路径字体大小": "filepath_font_size"
        }
        data = read_json()
        all_dict = {"main": data["main"], "slide": data["slide"], "single": data["single"]}
        all_dict['main'][name_variable_list[name]] = change
        with open('temp.json', 'w', encoding="utf-8") as json_file:
            json.dump(all_dict, json_file, indent=4)

    def choose_color(self, button):
        # 选择颜色窗口
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet("font-size:20px; padding:5px;border-radius:10px;background-color: %s;" % color.name())
        self.onChangeEvent(button.objectName(), button.palette().button().color().name())

    def preview_window(self):
        #预览窗口
        self.main_window = main.parent_page()
        self.main_window.show()

    def default_setting(self):
        label_font_size = 20
        title_background_color = "#94d2ef"
        title_font_size = 30
        button_font_size = 30
        button_padding = 10
        button_border_radius = 10
        button_background_color = "#e7e7e7"
        button_pressed_color = "#145214"
        filepath_font_size = 18
        window_background_color = "#F7FED5"

        dict = {"window_background_color": window_background_color,
                "label_font_size": label_font_size,
                "title_font_size": title_font_size,
                "title_background_color": title_background_color,
                "button_font_size": button_font_size,
                "button_padding": button_padding,
                "button_border_radius": button_border_radius,
                "button_background_color": button_background_color,
                "button_pressed_color": button_pressed_color,
                "filepath_font_size": filepath_font_size
        }
        return dict

class SlidePage(QWidget):
    # slide页面
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fontsize = [24, 18]
        self.btn_color_background = self.set_button_style("选择：页面背景颜色", "#e7e7e7")

        self.spin_label_font_size = self.set_spin_style(20, 12, 50, "标题大小")
        self.button_label_color = self.set_button_style("选择：问题背景颜色", "#ffffff")

        self.spin_button_font_size = self.set_spin_style(18, 12, 30, "按钮文本大小")
        self.spin_button_margin = self.set_spin_style(10, 0, 20, "按钮边距大小")
        self.btn_color_button = self.set_button_style("选择：按钮背景颜色", "#ffffff")
        self.btn_color_button_pressed = self.set_button_style("选择：按钮按下颜色", "#00ffff")
        self.spin_button_radius = self.set_spin_style(10, 0, 20, "按钮圆角大小")

        self.spin_answer_font_size = self.set_spin_style(20, 12, 30, "答案文本大小")
        self.button_answer_color = self.set_button_style("选择：隐藏答案背景颜色","#000000")
        self.button_answer_press_color = self.set_button_style("选择：揭晓答案背景颜色", "#ffffff")

        self.preview = self.set_button_style("预览", "#e7e7e7")
        self.preview.clicked.connect(self.preview_window)
        main_layout = QVBoxLayout(self)

        # 创建页面背景设置的大框
        background_group_box = self.set_label_style("页面背景设置", 0)
        background_layout = QVBoxLayout(background_group_box)
        hbox_background1 = QHBoxLayout()
        hbox_background1.addWidget(self.set_label_style("页面背景颜色", 1))
        hbox_background1.addWidget(self.btn_color_background)
        hbox_background1.addStretch(1)
        background_layout.addLayout(hbox_background1)
        main_layout.addWidget(background_group_box)

        # 创建标题设置的大框
        title_group_box = self.set_label_style("问题设置", 0)
        title_layout = QVBoxLayout(title_group_box)
        title_hbox1 = QHBoxLayout()
        title_hbox1.addWidget(self.set_label_style("字体大小", 1))
        title_hbox1.addWidget(self.spin_label_font_size)
        title_hbox1.addStretch(1)
        title_layout.addLayout(title_hbox1)
        title_hbox2 = QHBoxLayout()
        title_hbox2.addWidget(self.set_label_style("背景颜色", 1))
        title_hbox2.addWidget(self.button_label_color)
        title_hbox2.addStretch(1)
        title_layout.addLayout(title_hbox2)
        main_layout.addWidget(title_group_box)

        # 创建答案设置的大框
        answer_group_box = self.set_label_style("答案设置", 0)
        answer_layout = QVBoxLayout(answer_group_box)
        answer_hbox = QHBoxLayout()
        answer_hbox.addWidget(self.set_label_style("文字大小", 1))
        answer_hbox.addWidget(self.spin_answer_font_size)
        answer_hbox.addStretch(1)
        answer_layout.addLayout(answer_hbox)
        answer_hbox1 = QHBoxLayout()
        answer_hbox1.addWidget(self.set_label_style("隐藏答案颜色", 1))
        answer_hbox1.addWidget(self.button_answer_color)
        answer_hbox1.addStretch(1)
        answer_layout.addLayout(answer_hbox1)
        answer_hbox2 = QHBoxLayout()
        answer_hbox2.addWidget(self.set_label_style("揭晓答案颜色", 1))
        answer_hbox2.addWidget(self.button_answer_press_color)
        answer_hbox2.addStretch(1)
        answer_layout.addLayout(answer_hbox2)
        main_layout.addWidget(answer_group_box)

        # 创建按钮设置的大框
        button_group_box = self.set_label_style("按钮设置", 0)
        button_layout = QVBoxLayout(button_group_box)
        button_hbox1 = QHBoxLayout()
        button_hbox1.addWidget(self.set_label_style("按钮字体大小", 1))
        button_hbox1.addWidget(self.spin_button_font_size)
        button_hbox1.addStretch(1)
        button_layout.addLayout(button_hbox1)
        button_hbox2 = QHBoxLayout()
        button_hbox2.addWidget(self.set_label_style("按钮边距", 1))
        button_hbox2.addWidget(self.spin_button_margin)
        button_hbox2.addStretch(1)
        button_layout.addLayout(button_hbox2)
        button_hbox3 = QHBoxLayout()
        button_hbox3.addWidget(self.set_label_style("按钮弧度", 1))
        button_hbox3.addWidget(self.spin_button_radius)
        button_hbox3.addStretch(1)
        button_layout.addLayout(button_hbox3)
        button_hbox4 = QHBoxLayout()
        button_hbox4.addWidget(self.set_label_style("按钮颜色", 1))
        button_hbox4.addWidget(self.btn_color_button)
        button_hbox4.addStretch(1)
        button_layout.addLayout(button_hbox4)
        button_hbox5 = QHBoxLayout()
        button_hbox5.addWidget(self.set_label_style("按钮按下颜色", 1))
        button_hbox5.addWidget(self.btn_color_button_pressed)
        button_hbox5.addStretch(1)
        button_layout.addLayout(button_hbox5)
        main_layout.addWidget(button_group_box)

        main_layout.addWidget(self.preview)
        main_layout.addStretch(1)

    def set_label_style(self, text, type):
        # 设置label样式
        font = QFont()
        if type == 1:
            label = QLabel(text)
            label.setMinimumWidth(150)
            label.setStyleSheet(f"QLabel{{font-size:{self.fontsize[type]}px}}")
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font.setFamily("KaiTi")
            label.setFont(font)
            return label
        elif type == 0:
            groupbox = QGroupBox(text)
            groupbox.setStyleSheet(f"QLabel{{font-size:{self.fontsize[type]}px}}")
            font.setFamily("SimHei")
            groupbox.setFont(font)
            return groupbox

    def set_spin_style(self, value, min, max, name):
        # 设置spin样式
        spin = QSpinBox()
        spin.setValue(value)
        spin.setMinimum(min)
        spin.setMaximum(max)
        spin.setMinimumWidth(100)
        spin.setObjectName(name)
        spin.valueChanged.connect(lambda val, obj_name=name: self.onChangeEvent(obj_name, val))
        return spin

    def set_button_style(self, text, color):
        # 设置button样式
        button_style = f"QPushButton{{font-size:20px; padding:5px;border-radius:10px;background-color:{color}}}"
        button = QPushButton(text)
        button.setStyleSheet(button_style)
        button.setObjectName(text)
        if text != "预览":
            button.clicked.connect(lambda: self.choose_color(button))
        return button

    def choose_color(self, button):
        # 颜色设置
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet("font-size:20px; padding:5px;border-radius:10px;background-color: %s;" % color.name())
        self.onChangeEvent(button.objectName(),button.palette().button().color().name())

    def default_setting(self):
        label_font_size = 20
        label_background_color = "#ffffff"
        answer_font_size = 20
        answer_background_color = "#000000"
        answer_background_press_color = "#ffffff"
        button_font_size = 18
        button_padding = 10
        button_border_radius = 10
        button_background_color = "#ffffff"
        button_pressed_color = "#00ffff"
        window_background_color = "#e7e7e7"

        dict = {"window_background_color": window_background_color,
                "label_font_size": label_font_size,
                "label_background_color": label_background_color,
                "answer_font_size": answer_font_size,
                "answer_background_color": answer_background_color,
                "answer_background_press_color": answer_background_press_color,
                "button_font_size": button_font_size,
                "button_padding": button_padding,
                "button_border_radius": button_border_radius,
                "button_background_color": button_background_color,
                "button_pressed_color": button_pressed_color,
                }

        return dict

    def onChangeEvent(self, name, change):
        # change事件：每触发change就记录到temp.json
        name_variable_list = {
            "选择：页面背景颜色": "window_background_color", "选择：问题背景颜色": "label_background_color",
            "选择：按钮背景颜色": "button_background_color", "选择：按钮按下颜色": "button_pressed_color",
            "选择：隐藏答案背景颜色": "answer_background_color", "选择：揭晓答案背景颜色": "answer_background_press_color",
            "标题大小": "label_font_size", "按钮文本大小": "button_font_size", "按钮边距大小": "button_padding",
            "按钮圆角大小": "button_border_radius", "答案文本大小": "answer_font_size"
        }
        data = read_json()
        all_dict = {"main": data["main"], "slide": data["slide"], "single": data["single"]}
        all_dict['slide'][name_variable_list[name]] = change
        with open('temp.json', 'w', encoding="utf-8") as json_file:
            json.dump(all_dict, json_file, indent=4)

    def preview_window(self):
        self.slide_page = slide.child_page()
        self.slide_page.show()

class SinglePage(QWidget):
    # 单选窗口
    def __init__(self, parent=None):
        super().__init__(parent)

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

        self.fontsize = [24, 18]
        self.btn_color_background = self.set_button_style("选择：页面背景颜色", window_background_color)

        self.spin_label_font_size = self.set_spin_style(label_font_size, 12, 50, "标题大小")
        self.button_label_color = self.set_button_style("选择：问题背景颜色", label_background_color)

        self.spin_button_font_size = self.set_spin_style(button_font_size, 12, 30, "按钮文本大小")
        self.spin_button_margin = self.set_spin_style(button_padding, 0, 20, "按钮边距大小")
        self.btn_color_button = self.set_button_style("选择：按钮背景颜色", button_background_color)
        self.btn_color_button_press = self.set_button_style("选择：按钮按下颜色", button_pressed_color)
        self.btn_color_button_right = self.set_button_style("选择：按钮正确颜色", button_right_color)
        self.btn_color_button_wrong = self.set_button_style("选择：按钮错误颜色", button_wrong_color)
        self.spin_button_radius = self.set_spin_style(button_border_radius, 0, 20, "按钮圆角大小")

        self.spin_answer_font_size = self.set_spin_style(answer_font_size, 12, 30, "答案文本大小")
        self.button_answer_press_color = self.set_button_style("选择：答案背景颜色", answer_background_color)

        self.preview = self.set_button_style("预览", "#e7e7e7")
        self.preview.clicked.connect(self.preview_window)
        main_layout = QVBoxLayout(self)

        # 创建页面背景设置的大框
        background_group_box = self.set_label_style("页面背景设置", 0)
        background_layout = QVBoxLayout(background_group_box)
        hbox_background1 = QHBoxLayout()
        hbox_background1.addWidget(self.set_label_style("页面背景颜色", 1))
        hbox_background1.addWidget(self.btn_color_background)
        hbox_background1.addStretch(1)
        background_layout.addLayout(hbox_background1)
        main_layout.addWidget(background_group_box)

        # 创建标题设置的大框
        title_group_box = self.set_label_style("问题设置", 0)
        title_layout = QVBoxLayout(title_group_box)
        title_hbox1 = QHBoxLayout()
        title_hbox1.addWidget(self.set_label_style("字体大小", 1))
        title_hbox1.addWidget(self.spin_label_font_size)
        title_hbox1.addStretch(1)
        title_layout.addLayout(title_hbox1)
        title_hbox2 = QHBoxLayout()
        title_hbox2.addWidget(self.set_label_style("背景颜色", 1))
        title_hbox2.addWidget(self.button_label_color)
        title_hbox2.addStretch(1)
        title_layout.addLayout(title_hbox2)
        main_layout.addWidget(title_group_box)

        # 创建答案设置的大框
        answer_group_box = self.set_label_style("备注设置", 0)
        answer_layout = QVBoxLayout(answer_group_box)
        answer_hbox = QHBoxLayout()
        answer_hbox.addWidget(self.set_label_style("文字大小", 1))
        answer_hbox.addWidget(self.spin_answer_font_size)
        answer_hbox.addStretch(1)
        answer_layout.addLayout(answer_hbox)
        answer_hbox2 = QHBoxLayout()
        answer_hbox2.addWidget(self.set_label_style("背景颜色", 1))
        answer_hbox2.addWidget(self.button_answer_press_color)
        answer_hbox2.addStretch(1)
        answer_layout.addLayout(answer_hbox2)
        main_layout.addWidget(answer_group_box)

        # 创建按钮设置的大框
        button_group_box = self.set_label_style("按钮设置", 0)
        button_layout = QVBoxLayout(button_group_box)
        button_hbox1 = QHBoxLayout()
        button_hbox1.addWidget(self.set_label_style("按钮字体大小", 1))
        button_hbox1.addWidget(self.spin_button_font_size)
        button_hbox1.addStretch(1)
        button_layout.addLayout(button_hbox1)
        button_hbox2 = QHBoxLayout()
        button_hbox2.addWidget(self.set_label_style("按钮边距", 1))
        button_hbox2.addWidget(self.spin_button_margin)
        button_hbox2.addStretch(1)
        button_layout.addLayout(button_hbox2)
        button_hbox3 = QHBoxLayout()
        button_hbox3.addWidget(self.set_label_style("按钮弧度", 1))
        button_hbox3.addWidget(self.spin_button_radius)
        button_hbox3.addStretch(1)
        button_layout.addLayout(button_hbox3)
        button_hbox4 = QHBoxLayout()
        button_hbox4.addWidget(self.set_label_style("按钮颜色", 1))
        button_hbox4.addWidget(self.btn_color_button)
        button_hbox4.addStretch(1)
        button_layout.addLayout(button_hbox4)
        button_hbox5 = QHBoxLayout()
        button_hbox5.addWidget(self.set_label_style("按钮按下颜色", 1))
        button_hbox5.addWidget(self.btn_color_button_press)
        button_hbox5.addStretch(1)
        button_layout.addLayout(button_hbox5)
        button_hbox6 = QHBoxLayout()
        button_hbox6.addWidget(self.set_label_style("按钮正确颜色", 1))
        button_hbox6.addWidget(self.btn_color_button_right)
        button_hbox6.addStretch(1)
        button_layout.addLayout(button_hbox6)
        button_hbox7 = QHBoxLayout()
        button_hbox7.addWidget(self.set_label_style("按钮错误颜色", 1))
        button_hbox7.addWidget(self.btn_color_button_wrong)
        button_hbox7.addStretch(1)
        button_layout.addLayout(button_hbox7)
        main_layout.addWidget(button_group_box)

        # 创建出题模式的大框
        combobox_group_box = self.set_label_style("出题模式设置", 0)
        combobox_layout = QVBoxLayout(combobox_group_box)
        hbox_background8 = QHBoxLayout()
        hbox_background8.addWidget(self.set_label_style("开启不重复出题", 1))
        hbox_background8.addWidget(self.set_checkbox_style(non_repeat_check, "不重复出题"))
        hbox_background8.addStretch(1)
        combobox_layout.addLayout(hbox_background8)
        main_layout.addWidget(combobox_group_box)

        main_layout.addWidget(self.preview)
        main_layout.addStretch(1)

    def set_label_style(self,text,type):
        # 设置label样式
        font = QFont()
        if type == 1:
            label = QLabel(text)
            label.setMinimumWidth(150)
            label.setStyleSheet(f"QLabel{{font-size:{self.fontsize[type]}px}}")
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font.setFamily("KaiTi")
            label.setFont(font)
            return label
        elif type == 0:
            groupbox = QGroupBox(text)
            groupbox.setStyleSheet(f"QLabel{{font-size:{self.fontsize[type]}px}}")
            font.setFamily("SimHei")
            groupbox.setFont(font)
            return groupbox

    def set_spin_style(self, value, min, max, name):
        # 设置spin样式
        spin = QSpinBox()
        spin.setValue(int(value))
        spin.setMinimum(min)
        spin.setMaximum(max)
        spin.setMinimumWidth(100)
        spin.setObjectName(name)
        spin.valueChanged.connect(lambda val, obj_name=name: self.onChangeEvent(obj_name, val))
        return spin

    def set_checkbox_style(self, status, name):
        # 设置checkbox样式
        checkbox = QCheckBox()
        checkbox.setChecked(status)
        checkbox.setObjectName(name)
        checkbox.stateChanged.connect(lambda state, obj_name=name: self.onChangeEvent(obj_name, state))
        return checkbox

    def default_setting(self):
        window_background_color = "#e7e7e7"
        label_font_size = 20
        label_background_color = "#ffffff"
        answer_font_size = 20
        answer_background_color = "#ffffff"
        button_font_size = 18
        button_padding = 10
        button_border_radius = 10
        button_background_color = "#ffffff"
        button_pressed_color = "#00ffff"
        button_right_color = "#00ff00"
        button_wrong_color = "#ff0000"
        non_repeat_check = True

        dict = {"window_background_color": window_background_color,
                "label_font_size": label_font_size,
                "label_background_color": label_background_color,
                "answer_font_size": answer_font_size,
                "answer_background_color": answer_background_color,
                "button_font_size": button_font_size,
                "button_padding": button_padding,
                "button_border_radius": button_border_radius,
                "button_background_color": button_background_color,
                "button_pressed_color": button_pressed_color,
                "button_right_color": button_right_color,
                "button_wrong_color": button_wrong_color,
                "non_repeat_check": non_repeat_check
        }

        return dict

    def set_button_style(self,text,color):
        # 设置button样式
        button_style = f"QPushButton{{font-size:20px; padding:5px;border-radius:10px;background-color:{color}}}"
        button = QPushButton(text)
        button.setStyleSheet(button_style)
        button.setObjectName(text)
        if text != "预览" and text !="设为默认值":
            button.clicked.connect(lambda : self.choose_color(button))
        return button

    def onChangeEvent(self, name, change):
        # change事件：每触发change就记录到temp.json
        # checkbox返回的change为0/2，因此做bool操作
        if name == "不重复出题":
            change = bool(change)
        name_variable_list = {
            "选择：页面背景颜色": "window_background_color", "选择：问题背景颜色": "label_background_color",
            "选择：按钮背景颜色": "button_background_color", "选择：按钮按下颜色": "button_pressed_color",
            "选择：按钮正确颜色": "button_right_color", "选择：按钮错误颜色": "button_wrong_color", "选择：答案背景颜色": "answer_background_color",
            "标题大小": "label_font_size", "按钮文本大小": "button_font_size", "按钮边距大小": "button_padding",
            "按钮圆角大小": "button_border_radius", "答案文本大小": "answer_font_size", "不重复出题": "non_repeat_check"
        }
        data = read_json()
        all_dict = {"main": data["main"], "slide": data["slide"], "single": data["single"]}
        all_dict['single'][name_variable_list[name]] = change
        with open('temp.json', 'w', encoding="utf-8") as json_file:
            json.dump(all_dict, json_file, indent=4)

    def choose_color(self, button):
        # 设置颜色
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet("font-size:20px; padding:5px;border-radius:10px;background-color: %s;" % color.name())
        self.onChangeEvent(button.objectName(), button.palette().button().color().name())

    def preview_window(self):
        self.single_window = SingleChoose.child_page_two()
        self.single_window.show()

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if os.path.exists("temp.json"):
            os.remove("temp.json")

        self.tabs = QTabWidget()
        self.tabs.addTab(MainPage(), "主页面")
        self.tabs.addTab(SlidePage(), "问题猜答案")
        self.tabs.addTab(SinglePage(), "单项选择")

        self.btn_save = QPushButton("保存结果")
        self.btn_save.clicked.connect(self.save_results)

        self.btn_default = QPushButton("设为默认值（需重新启动）")
        self.btn_default.clicked.connect(self.default_results)

        self.layout_init()

    def layout_init(self):
        self.setWindowTitle("页面样式设置")
        self.setGeometry(200, 200, 960, 540)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addWidget(self.btn_save)
        vbox.addWidget(self.btn_default)

        central_widget.setLayout(vbox)

    def save_results(self):
        # 保存结果
        data = read_json()
        all_dict = {"main": data["main"], "slide": data["slide"], "single": data["single"]}
        with open('setting.json', 'w', encoding="utf-8") as json_file:
            json.dump(all_dict, json_file, indent=4)
        QMessageBox.information(self,"提示","保存成功")

    def default_results(self):
        main_result = MainPage().default_setting()
        slide_result = SlidePage().default_setting()
        single_result = SinglePage().default_setting()
        all_dict = {"main": main_result, "slide": slide_result, "single": single_result}
        with open('setting.json', 'w', encoding="utf-8") as json_file:
            json.dump(all_dict, json_file, indent=4)
        self.close()

    def closeEvent(self,event):
        self.close()
        self.main_window = main.parent_page()
        self.main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
