import os
import subprocess
import sys
import csv

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class StudentGradeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.setWindowTitle("Student Grade Editor")
        self.resize(820, 620)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        title = QLabel("Student Grade Editor")
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        controls_layout = QHBoxLayout()

        load_button = QPushButton("Load File")
        load_button.clicked.connect(self.choose_file)

        self.bonus_input = QLineEdit()
        self.bonus_input.setPlaceholderText("Bonus points")
        self.bonus_input.setValidator(QIntValidator(-1000, 1000, self))
        self.bonus_input.returnPressed.connect(self.apply_bonus)

        update_button = QPushButton("Update File")
        update_button.clicked.connect(self.update_file)

        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)

        controls_layout.addWidget(load_button)
        controls_layout.addWidget(self.bonus_input)
        controls_layout.addStretch()
        controls_layout.addWidget(update_button)
        controls_layout.addWidget(about_button)
        main_layout.addLayout(controls_layout)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table)

        self.setCentralWidget(central_widget)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        self.selected_file = file_path
        if file_path:
            self.selected_file = file_path
            self.student_ids.clear()
            self.original_grades.clear()
            self.corrected_grades.clear()

        with open(self.selected_file, mode='r', encoding='utf-8-sig', newline='') as f: 
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.student_ids.append(row[0])
                grade = int(row[1])
                self.original_grades.append(grade)
                self.corrected_grades.append(grade)

            self.update_table()

    def apply_bonus(self):
        # TODO: Implement bonus calculation logic here.
        # Read the integer bonus from self.bonus_input and update corrected_grades.
        pass

    def update_table(self):
        for row in range(50):
            values = (
                self.student_ids[row] if row < len(self.student_ids) else "",
                self.original_grades[row] if row < len(self.original_grades) else "",
                self.corrected_grades[row] if row < len(self.corrected_grades) else "",
            )
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))

    def update_file(self):
        # TODO: Implement CSV writing logic here.
        # Write student IDs and corrected grades to self.selected_file.

        self.open_file_cross_platform(self.selected_file)

    def open_file_cross_platform(self, file_path):
        if not file_path:
            return

        if sys.platform.startswith("win"):
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About")
        dialog.resize(360, 180)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Student Grade Editor"))
        layout.addWidget(QLabel("Author: Ravid Fathi"))
        layout.addWidget(QLabel("Email: Ravid.Fathi@s.afeka.ac.il"))
        layout.addWidget(QLabel("GitHub Repository: [PLACEHOLDER_URL]"))
        layout.addStretch()

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        dialog.exec()


MainWindow = StudentGradeEditor


def main():
    app = QApplication.instance() or QApplication(sys.argv)

    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as style_file:
            app.setStyleSheet(style_file.read())

    window = StudentGradeEditor()
    window.show()

    if QApplication.instance() is app:
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
