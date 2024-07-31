from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from loguru import logger
from python_docx_replace import docx_replace, docx_get_keys
from docx import Document
import pypandoc

from frame_field import FrameField
from ui.ui_document_templater import Ui_MainWindow


from utils import *


class DocumentTeplatter(QtWidgets.QMainWindow, Ui_MainWindow):
    @logger.catch
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.doc: Document
        self.doc_path: str
        self.template_path: str = os.getcwd() + '/templates/'
        self.frame_list: list = []
        self.data: dict = {}

        self.__connection()

        check_folders()
        self.__get_data()

        self.__update_template_listwidget()

    @logger.catch
    def __connection(self):
        self.listWidget_template.doubleClicked.connect(self.__choose_template)
        self.listWidget_template.fileReceived.connect(self.__load_docx)
        self.pushButton_redaction_template_save.clicked.connect(self.__save_result_docs)
        self.pushButton_open.clicked.connect(self.__open_file)

    @logger.catch
    def __open_file(self, event):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Word Files (*.docx)")
        self.__load_docx(file_path)

    @logger.catch
    def __load_docx(self, path: str):
        try:
            if path:
                if path.endswith('.docx'):
                    if not os.path.exists(self.template_path+os.path.basename(path)):
                        document = Document(path)
                        keys = docx_get_keys(document)
                        if keys:
                            document.save(self.template_path+os.path.basename(path))
                        else:
                            error = QMessageBox(text="Не найдены строки шаблона\nПроверьте правильность заполнения шаблона")
                            error.exec()
                    else:
                        error = QMessageBox(text="Шаблон с таким именем уже есть")
                        error.exec()
                else:
                    error = QMessageBox(text="Поддерживается только формат .docx")
                    error.exec()
                self.__update_template_listwidget()
            else:
                self.label_info.setText("Файл не выбран")
        except Exception as e:
            print(e)

    @logger.catch
    def __update_template_listwidget(self):
        file_names = [f for f in os.listdir(self.template_path) if f.endswith('.docx')]
        self.listWidget_template.clear()
        for i in file_names:
            self.listWidget_template.addItem(os.path.splitext(i)[0])

    @logger.catch
    def __choose_template(self, event=False):
        if os.path.exists(self.template_path+self.listWidget_template.currentItem().text()+'.docx'):
            self.__delete_fields()
            path = self.template_path+self.listWidget_template.currentItem().text()+'.docx'
            self.doc = Document(path)
            self.__convert_docx(path)
            self.__create_redaction_template_input_field()

            self.label_info.setText(f"Открыт шаблон {self.listWidget_template.currentItem().text()}")
        else:
            error = QMessageBox(text="Не найдены файлы шаблона")
            error.exec()

    @logger.catch
    def __convert_docx(self, path: str):
        try:
            pypandoc.convert_file(path, 'html', outputfile='templates/temp.html')
            self.__open_html()
        except Exception as e:
            self.label_info.setText(e)

    @logger.catch
    def __open_html(self):
        with open('templates/temp.html', 'r', encoding='utf-8') as file:
            self.widget_docs_view.setHtml(file.read())

    @logger.catch
    def __create_redaction_template_input_field(self):
        keys = docx_get_keys(self.doc)
        if keys:
            keys = sort_list(keys)
            self.save_file_name = self.listWidget_template.currentItem().text()
            for i in keys:
                frame = FrameField(self.scrollAreaWidgetContents, self.data)
                frame.label.setText(i)
                self.frame_list.append(frame)
                self.verticalLayout_scrollAreaWidgetContents.addWidget(frame.get_frame())
        else:
            error = QMessageBox(text="Не найдены строки шаблона\nПроверьте правильность заполнения шаблона")
            error.exec()

    @logger.catch
    def __save_result_docs(self, event=False):
        for i in self.frame_list:
            docx_replace(self.doc, **{i.label.text(): i.lineEdit.text()})
        save_path = QFileDialog.getSaveFileName(None,
                                                'Save file',
                                                './result/'+self.save_file_name,
                                                "Word Files (*.docx)")
        try:
            self.doc.save(save_path[0])
            self.label_info.setText(f"Файл сохранён: {save_path[0]}")
        except FileNotFoundError:
            self.label_info.setText("Не выбрано место сохранения")

    @logger.catch
    def __delete_fields(self, event=False):
        for i in self.frame_list:
            i.get_frame().deleteLater()
        self.frame_list.clear()

    @logger.catch
    def __get_data(self):
        self.data = get_data_dict()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = DocumentTeplatter()
    MainWindow.show()
    sys.exit(app.exec())
