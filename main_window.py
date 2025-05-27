from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout
from PyQt5 import QtWidgets, QtCore
from gui import Ui_MainWindow
import task_manager

#do dodania: usuwanie tasków, tworzenie różnych list tasków (np. praca, dom, zakupy)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.taskFrameTemplate.hide()
        self.setWindowTitle("TO-DO app")

        self.show_all_tasks()

    # ---------- PAGES 
        self.ui.pagesWidget.setCurrentIndex(0)
    # ----- PAGE 1
        self.ui.openAddPageBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.addTaskPage))

    # ----- PAGE 2 ----- adding new tasks
        self.ui.addNewTaskBtn.clicked.connect(lambda: self.add_task())
        #change to page 1
        self.ui.addNewTaskBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.taskListPage))
        self.ui.backToPage1Btn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.taskListPage))

        self.ui.pagesWidget.currentChanged.connect(self.show_all_tasks)

    # ---------- LOAD DATA FROM FILE ON START
    task_manager.create_file_if_not_exists()

    def create_task_frame(self, content, id):
        # --- Copy all items from taskTemplate
        # Frame
        task_frame = QtWidgets.QFrame()
        task_frame.setStyleSheet(self.ui.taskFrameTemplate.styleSheet())
        task_frame.setMinimumSize(self.ui.taskFrameTemplate.minimumSize())
        task_frame.setMaximumHeight(self.ui.taskFrameTemplate.maximumHeight())
        task_frame.setFrameShape(self.ui.taskFrameTemplate.frameShape())
        task_frame.setFrameShadow(self.ui.taskFrameTemplate.frameShadow())
        # Layout
        layout = QHBoxLayout(task_frame)
        layout.setSpacing(10)
        # Content Label
        task_label = QtWidgets.QLabel()
        task_label.setStyleSheet(self.ui.taskContentLabelTemplate.styleSheet())
        task_label.setMinimumSize(self.ui.taskContentLabelTemplate.minimumSize())
        task_label.setMaximumSize(self.ui.taskContentLabelTemplate.maximumSize())
        task_label.setFont(self.ui.taskContentLabelTemplate.font())
        task_label.setText(content)
        # Trash Btn
        trash_button = QPushButton()
        trash_button.setMinimumSize(self.ui.trashButtonTaskTemplate.minimumSize())
        trash_button.setMaximumSize(self.ui.trashButtonTaskTemplate.maximumSize())
        trash_button.setStyleSheet(self.ui.trashButtonTaskTemplate.styleSheet())
        trash_button.setIcon(self.ui.trashButtonTaskTemplate.icon())
        trash_button.setIconSize(self.ui.trashButtonTaskTemplate.iconSize())
        # Add widgets to layout
        layout.addWidget(task_label)
        layout.addWidget(trash_button)
        # Add widget to scrollArea
        scroll_frame = self.ui.scrollAreaWidgetContents.layout()
        scroll_frame.addWidget(task_frame)

        trash_button.clicked.connect(lambda: task_manager.delete_task(id))
        trash_button.clicked.connect(lambda: self.show_all_tasks())

    def add_task(self):
        task_content = self.ui.taskNameInput.text()
        self.ui.taskNameInput.clear()
        if (task_content == ""):
            print("empty input")
        else:
            task_manager.add_new_task(task_content)

    def show_all_tasks(self):
        layout = self.ui.scrollAreaWidgetContents.layout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.clear_task_list()
        tasks = task_manager.load_data()
        
        #create task frame
        for task in tasks:
            self.create_task_frame(task['content'], task['id'])

    def clear_task_list(self):
        layout = self.ui.scrollAreaWidgetContents.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()