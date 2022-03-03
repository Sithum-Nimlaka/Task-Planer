'''
Developer: Sithum Nimlaka Abeydheera
Date: 2022.03.03
'''

import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./Ui/task-planer.ui", self)
        self.setWindowTitle("Task Planner")
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveBtn.clicked.connect(self.saveChanges)
        self.addNewBtn.clicked.connect(self.addNew)

    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        self.updateTaskList(date=dateSelected)

    def updateTaskList(self, date):
        self.taskList.clear()
        db = sqlite3.connect("./db/todo.db")
        cursor = db.cursor()
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(Qt.Unchecked)
            self.taskList.addItem(item)

    def saveChanges(self):
        db = sqlite3.connect("./db/todo.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            task = item.text()
            if item.checkState() == Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Task Planner")
        messageBox.setText("Changes are saved!")
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNew(self):
        db = sqlite3.connect("./db/todo.db")
        cursor = db.cursor()
        newTask = self.newTaskInput.text()
        if newTask == "":
            messageBox = QMessageBox()
            messageBox.setWindowTitle("Task Planner")
            messageBox.setText("Can't add empty tasks!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.exec()
        else:
            date = self.calendarWidget.selectedDate().toPyDate()
            query = "INSERT INTO tasks(task, completed, date) VALUES(?,?,?)"
            row = (newTask, "NO", date,)
            cursor.execute(query, row)
            db.commit()
            self.newTaskInput.clear()
            messageBox = QMessageBox()
            messageBox.setWindowTitle("Task Planner")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Task added successfull!")
            messageBox.exec()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(App.exec())
