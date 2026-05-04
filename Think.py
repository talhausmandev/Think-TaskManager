from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QDateTimeEdit, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QLabel, QMenu, QMessageBox
import threading
import datetime
import json
from plyer import notification
import PySide6.QtCore as qtcore
import os



if os.path.exists("tasks.json"):
    with open("tasks.json", "r") as f:
        tasks = json.loads(f.read())
else:
    with open("tasks.json", "w") as f:
        f.write(json.dumps([]))
        tasks = []

def manager():
    while True:
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        for task in tasks:
            task_time = datetime.datetime.fromisoformat(task["time"]).replace(second=0, microsecond=0)
            if task_time <= now:
                notification.notify(
                    title="Think - Your Own Task Manager",
                    message=f"{datetime.datetime.fromisoformat(task["time"]).strftime("%B %d, %Y - %I:%M %p")}\n{task["title"]}\n{task["message"]}",
                    timeout=10)
                tasks.remove(task)
                reset_list()
                with open("tasks.json", "w") as f:
                    f.write(json.dumps(tasks))

task_manager = threading.Thread(target=manager, daemon=True)
task_manager.start()

def context_menu(pos):
    item = tasks_list.itemAt(pos)
    menu = QMenu()
    if item:
        edit_action = menu.addAction(f"Edit Task")
        delete_action =  menu.addAction(f"Delete Task")
        

        index = tasks_list.row(item)
        action = menu.exec(tasks_list.mapToGlobal(pos))
        if action == delete_action:
            tasks.pop(index)
            reset_list()
        elif action == edit_action:
            task_title_input.setText(tasks[index]["title"])
            task_message_input.setText(tasks[index]["message"])
            task_time_input.setDateTime(qtcore.QDateTime(datetime.datetime.fromisoformat(tasks[index]["time"])))
            tasks.pop(index)
            reset_list()
    
        

    
    
    with open("tasks.json", "w") as f:
        f.write(json.dumps(tasks))

def reset_list():
    new_list = [f"{t["title"]}  |  {datetime.datetime.fromisoformat(t["time"]).strftime("%B %d, %Y - %I:%M %p")}" for t in tasks]
    tasks_list.clear()
    tasks_list.addItems(new_list)

def reset_inputs():
    task_title_input.clear()
    task_message_input.clear()
    task_time_input.setDateTime(qtcore.QDateTime.currentDateTime())

def save_task():
    task_title = task_title_input.text()
    task_message = task_message_input.toPlainText()
    if task_title or task_message:
        qdt = task_time_input.dateTime()
        y = qdt.date().year()
        m = qdt.date().month()
        d = qdt.date().day()
        h = qdt.time().hour()
        mi = qdt.time().minute()
        task_time = datetime.datetime(int(y), int(m), int(d) , int(h), int(mi)).isoformat()
        new_task = {
            "title": task_title,
            "message": task_message,
            "time": task_time
            }
        tasks.append(new_task)
        reset_list()
        reset_inputs()
        with open("tasks.json", "w") as f:
            f.write(json.dumps(tasks))
    else:
        QMessageBox.information(window, "Info", "your task title or message is empty.")


tasks_for_task_list = [f"{t["title"]}  |  {datetime.datetime.fromisoformat(t["time"]).strftime("%B %d, %Y - %I:%M %p")}" for t in tasks]





app = QApplication()
window = QMainWindow()
window.setWindowTitle("Think")
window.setFixedSize(700, 400)
main_container = QWidget()
left_container = QWidget()
right_container = QWidget()
main_Layout = QHBoxLayout(main_container)
left_Layout = QVBoxLayout(left_container)
right_Layout = QVBoxLayout(right_container)

task_title_input = QLineEdit()
task_title_input.setPlaceholderText("Enter Task Title..")
task_message_input = QTextEdit()
task_message_input.setPlaceholderText("Enter Task Message..")
task_time_input = QDateTimeEdit()
save_button = QPushButton("Save Task")
save_button.clicked.connect(save_task)
save_button.setCursor(qtcore.Qt.PointingHandCursor)


tasks_label = QLabel("All Tasks")
tasks_list = QListWidget()
tasks_list.addItems(tasks_for_task_list)
tasks_list.setContextMenuPolicy(qtcore.Qt.CustomContextMenu)
tasks_list.customContextMenuRequested.connect(context_menu)

left_Layout.addWidget(task_title_input)
left_Layout.addWidget(task_message_input)
left_Layout.addWidget(task_time_input)
left_Layout.addWidget(save_button)
right_Layout.addWidget(tasks_label)
right_Layout.addWidget(tasks_list)

main_Layout.addWidget(left_container)
main_Layout.addWidget(right_container)

window.setCentralWidget(main_container)

with open("style.qss") as f:
    window.setStyleSheet(f.read())


window.show()
app.exec()
