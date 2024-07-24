import os

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from loguru import logger

from frame_field import FrameField
from ui.ui_document_templater import Ui_MainWindow
from python_docx_replace import docx_replace, docx_get_keys

from utils import *


class DocumentTeplatter(QtWidgets.QMainWindow, Ui_MainWindow):
    @logger.catch
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.doc: Document
        self.doc_path: str
        self.current_dir: str = os.getcwd()
        self.template_path: str = self.current_dir + '/templates/'
        self.result_path: str = self.current_dir + '/result/'
        self.frame_list: list = []
        self.param_list: list = []
        self.listWidget_template.doubleClicked.connect(self.__create_redaction_template_input_field)
        self.listWidget_template.fileReceived.connect(self.__load_docx)
        self.pushButton_redaction_template_save.clicked.connect(self.__save_result_docs)
        self.__update_template_listwidget()

        if not os.path.exists('./templates'):
            os.mkdir('./templates')
        if not os.path.exists('./result'):
            os.mkdir('./result')

    @logger.catch
    def __load_docx(self, path: str):
        try:
            if path.endswith('.docx'):
                if not os.path.exists(self.template_path+os.path.basename(path)):
                    document = Document(path)
                    document.save(self.template_path+os.path.basename(path))
                else:
                    error = QMessageBox(text="Шаблон с таким именем уже есть")
                    error.exec()
            else:
                error = QMessageBox(text="Поддерживается только формат .docx")
                error.exec()
            self.__update_template_listwidget()
        except Exception as e:
            print(e)

    @logger.catch
    def __update_template_listwidget(self):
        file_names = [f for f in os.listdir(self.template_path) if f.endswith('.docx')]
        self.listWidget_template.clear()
        for i in file_names:
            self.listWidget_template.addItem(os.path.splitext(i)[0])

    @logger.catch
    def __create_redaction_template_input_field(self, bul_val=False):
        self.__delete_fields()
        if os.path.exists(self.template_path+self.listWidget_template.currentItem().text()+'.docx'):
            self.doc = Document(self.template_path+self.listWidget_template.currentItem().text()+'.docx')
            keys = docx_get_keys(self.doc)
            if not keys:
                parse_docx(self.doc)
            self.save_file_name = self.listWidget_template.currentItem().text()
            for i in keys:
                self.param_list.append(i)
                frame = FrameField(self.scrollAreaWidgetContents)
                frame.label.setText(i)
                self.frame_list.append(frame)
                self.verticalLayout_2.addWidget(frame.get_frame())
        else:
            error = QMessageBox(text="Не найдены файлы шаблона")
            error.exec()

    @logger.catch
    def __save_result_docs(self, bul_val=False):
        for i in self.frame_list:
            eval(f"docx_replace(self.doc, {i.label.text()}='{i.lineEdit.text()}')")
        self.doc.save(os.getcwd()+'/result/'+self.save_file_name+'.docx')
        self.label_info.setText(f"Файл сохранён: ./result/{self.save_file_name}.docx")

    @logger.catch
    def __delete_fields(self, bul_val=False):
        for i in self.frame_list:
            i.get_frame().deleteLater()
        self.frame_list.clear()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = DocumentTeplatter()
    MainWindow.show()
    sys.exit(app.exec())