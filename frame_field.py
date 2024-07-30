from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu


class FrameField:
    def __init__(self, parent, data):
        self.data = data
        self.frame = QtWidgets.QFrame(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_main = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_main.setObjectName("horizontalLayout_main")
        self.frame_field = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_field.sizePolicy().hasHeightForWidth())
        self.frame_field.setSizePolicy(sizePolicy)
        self.frame_field.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_field.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_field.setObjectName("frame_field")
        self.verticalLayout_field = QtWidgets.QVBoxLayout(self.frame_field)
        self.verticalLayout_field.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_field.setObjectName("verticalLayout_field")
        self.label = QtWidgets.QLabel(self.frame_field)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label.setObjectName("label")
        self.verticalLayout_field.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_field)
        self.lineEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_field.addWidget(self.lineEdit)
        self.horizontalLayout_main.addWidget(self.frame_field)
        self.frame_context_menu_button = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_context_menu_button.sizePolicy().hasHeightForWidth())
        self.frame_context_menu_button.setSizePolicy(sizePolicy)
        self.frame_context_menu_button.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_context_menu_button.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_context_menu_button.setObjectName("frame_context_menu_button")
        self.verticalLayout_context_menu_button = QtWidgets.QVBoxLayout(self.frame_context_menu_button)
        self.verticalLayout_context_menu_button.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_context_menu_button.setObjectName("verticalLayout_context_menu_button")
        self.pushButton_context_menu = QtWidgets.QPushButton(self.frame_context_menu_button)
        self.pushButton_context_menu.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_context_menu.setFont(font)
        self.pushButton_context_menu.setObjectName("pushButton_context_menu")
        self.verticalLayout_context_menu_button.addWidget(self.pushButton_context_menu)
        self.horizontalLayout_main.addWidget(self.frame_context_menu_button)

        self.pushButton_context_menu.setText(">")
        self.pushButton_context_menu.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.pushButton_context_menu.customContextMenuRequested.connect(self.showContextMenu)
        self.pushButton_context_menu.clicked.connect(self.showContextMenu)

    def get_frame(self):
        return self.frame

    def showContextMenu(self, pos):
        menu = QMenu(self.pushButton_context_menu)

        for key in self.data.keys():
            submenu = QMenu(key, self.pushButton_context_menu)
            for item in self.data[key]:
                action = submenu.addAction(item)
                action.triggered.connect(lambda checked, text=item: self.lineEdit.setText(text))
            menu.addMenu(submenu)

        menu.exec(self.pushButton_context_menu.mapToGlobal(self.pushButton_context_menu.rect().bottomLeft()))
