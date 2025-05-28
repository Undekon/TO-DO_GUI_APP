from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout
from PyQt5 import QtWidgets, QtCore
from gui import Ui_MainWindow
import task_manager
from task_widget import TaskWidget

#do dodania: usuwanie tasków, tworzenie różnych list tasków (np. praca, dom, zakupy)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.taskFrameTemplate.hide()
        self.ui.taskFrameTemplate_2.hide()
        self.ui.taskFrameTemplate_3.hide()
        self.ui.taskFrameTemplate_4.hide()
        self.setWindowTitle("TO-DO app")
        self.show_all_tasks(self.ui.scrollAreaWidgetContents)
        self.ui.taskCategorySelect.model().item(0).setEnabled(False)


    # ---------- PAGES 
        self.ui.pagesWidget.setCurrentIndex(0)
    # ----- PAGE 1
        self.ui.openAddPageBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.addTaskPage))
    # ----- PAGE 2 ----- adding new tasks
        self.ui.addNewTaskBtn.clicked.connect(lambda: self.add_task())
        #change to page 1
        self.ui.addNewTaskBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.taskListPage))
        self.ui.backToPage1Btn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.taskListPage))
    # ----- PAGE 3
        self.ui.homeBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.taskListPage))
    # ----- PAGE 4 ----- Shopping list
        self.ui.shopBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.shopTaskListPage))
        self.ui.shopBtn.clicked.connect(lambda: self.show_shopping_list())
        
    # ----- PAGE 5 ----- School list
        self.ui.schoolBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.schoolTaskListPage))
        self.ui.schoolBtn.clicked.connect(lambda: self.show_school_list())
    # ----- PAGE 6 ----- Job list
        self.ui.jobBtn.clicked.connect(lambda: self.ui.pagesWidget.setCurrentWidget(self.ui.jobTaskListPage))
        self.ui.jobBtn.clicked.connect(lambda: self.show_job_list())

        self.ui.exitBtn.clicked.connect(self.close)
        self.ui.pagesWidget.currentChanged.connect(lambda: self.show_all_tasks(self.ui.scrollAreaWidgetContents))

    # ---------- LOAD DATA FROM FILE ON START
    task_manager.create_file_if_not_exists()

    def create_task_frame(self, content, id, category, scroll_parent, refresh_callback):
        # if refresh_callback == None:
        #      refresh_callback = self.show_all_tasks
        task_widget = TaskWidget(id, 
                                 content,
                                 category,
                                 scroll_parent,
                                 self.ui.taskFrameTemplate,
                                 self.ui.taskContentLabelTemplate,
                                 self.ui.trashButtonTaskTemplate,
                                 refresh_callback
                                 )
        scroll_parent.layout().addWidget(task_widget)

    def add_task(self):
        task_content = self.ui.taskNameInput.text()
        task_category = self.ui.taskCategorySelect.currentText().lower()
        if task_category == 'select category':
             task_category = 'general'
        self.ui.taskNameInput.clear()
        if (task_content == ""):
            print("empty input")
        else:
            task_manager.add_new_task(task_content, task_category)

    def show_all_tasks(self, parent=None):
        if parent == None:
            parent = self.ui.scrollAreaWidgetContents

        layout = parent.layout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.clear_task_list(parent)
        tasks = task_manager.load_data()
        
        #create task frame
        for task in tasks:
            self.create_task_frame(task['content'], task['id'], task['category'], parent, self.show_all_tasks)

    def clear_task_list(self,parent):
        layout = parent.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def show_shopping_list(self):
            layout = self.ui.shopScrollAreaWidgetContents.layout()
            layout.setAlignment(QtCore.Qt.AlignTop)
            parent = self.ui.shopScrollAreaWidgetContents
            self.clear_task_list(parent)

            tasks = task_manager.load_data()
            for task in tasks:
                if task['category'] == 'shopping list':
                    print (task)
                    self.create_task_frame(task['content'], task['id'], task['category'], parent, self.show_shopping_list)

    def show_school_list(self):
            layout = self.ui.schoolScrollAreaWidgetContents.layout()
            layout.setAlignment(QtCore.Qt.AlignTop)
            parent = self.ui.schoolScrollAreaWidgetContents
            self.clear_task_list(parent)

            tasks = task_manager.load_data()
            for task in tasks:
                if task['category'] == 'school list':
                    print (task)
                    self.create_task_frame(task['content'], task['id'], task['category'], parent, self.show_school_list)
    
    def show_job_list(self):
            layout = self.ui.jobScrollAreaWidgetContents.layout()
            layout.setAlignment(QtCore.Qt.AlignTop)
            parent = self.ui.jobScrollAreaWidgetContents
            self.clear_task_list(parent)

            tasks = task_manager.load_data()
            for task in tasks:
                if task['category'] == 'job list':
                    print (task)
                    self.create_task_frame(task['content'], task['id'], task['category'], parent, self.show_job_list)