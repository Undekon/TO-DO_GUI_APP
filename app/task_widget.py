from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt5 import QtWidgets
from task_manager import delete_task

class TaskWidget(QFrame):
    def __init__(self, _id, _content, _category, _parent, _frame_template, _label_template, _trash_template, showalltasks_callout):
        super().__init__(_parent)
        self.id = _id
        self.content = _content
        self.category = _category
        self.refresh_list = showalltasks_callout
        self.widget_parent = _parent
        #frame template elements
        self.setup_ui(_frame_template, _label_template, _trash_template, _content, _id, self.widget_parent)

    def handle_delete(self, id):
        delete_task(id)
        self.refresh_list()

    def setup_ui(self, frame_template, label_template, trash_btn_template, content, id, widget_parent):
        # --- Appearance is copied from task template widget
        self.setStyleSheet(frame_template.styleSheet())
        self.setMinimumSize(frame_template.minimumSize())
        self.setMaximumHeight(frame_template.maximumHeight())
        self.setFrameShape(frame_template.frameShape())
        self.setFrameShadow(frame_template.frameShadow())
        # Layout
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        # Content Label
        self.task_label = QtWidgets.QLabel(self)
        self.task_label.setStyleSheet(label_template.styleSheet())
        self.task_label.setMinimumSize(label_template.minimumSize())
        self.task_label.setMaximumSize(label_template.maximumSize())
        self.task_label.setFont(label_template.font())
        self.task_label.setText(content)
        layout.addWidget(self.task_label)
        # Trash Btn
        self.trash_button = QPushButton(self)
        self.trash_button.setMinimumSize(trash_btn_template.minimumSize())
        self.trash_button.setMaximumSize(trash_btn_template.maximumSize())
        self.trash_button.setStyleSheet(trash_btn_template.styleSheet())
        self.trash_button.setIcon(trash_btn_template.icon())
        self.trash_button.setIconSize(trash_btn_template.iconSize())
        layout.addWidget(self.trash_button)

        #Edit Btn

        #Button connections
        self.trash_button.clicked.connect(lambda: self.handle_delete(id))
