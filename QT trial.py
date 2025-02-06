import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QListWidget,
    QCheckBox,
    QRadioButton,
    QPushButton,
    QHBoxLayout,
)

class ComboBoxListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("ComboBox, ListBox, CheckBox, RadioButton Example")
        self.setGeometry(100, 100, 400, 300)

        # Set up the central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # ComboBox
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
       

        # ListBox
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(["Item A", "Item B", "Item C"])
        layout.addWidget(QLabel("Select items from the list:"), self)
        layout.addWidget(self.list_widget)

        # CheckBox
        self.check_box = QCheckBox("Enable Feature", self)
        layout.addWidget(self.check_box)

        # RadioButtons
        self.radio_button_1 = QRadioButton("Choice A", self)
        self.radio_button_2 = QRadioButton("Choice B", self)
        layout.addWidget(self.radio_button_1)
        layout.addWidget(self.radio_button_2)

        # Button to show selections
        self.show_selection_button = QPushButton("Show Selections", self)
        self.show_selection_button.clicked.connect(self.show_selections)
        layout.addWidget(self.show_selection_button)

        # Status Label
        self.status_label = QLabel("Selections will be displayed here.", self)
        layout.addWidget(self.status_label)

    def show_selections(self):
        selected_combo = self.combo_box.currentText()
        selected_list = [item.text() for item in self.list_widget.selectedItems()]
        check_box_status = "Checked" if self.check_box.isChecked() else "Unchecked"
        radio_button_status = "Choice A" if self.radio_button_1.isChecked() else "Choice B" if self.radio_button_2.isChecked() else "None"

        self.status_label.setText(
            f"ComboBox: {selected_combo}, "
            f"List: {', '.join(selected_list)}, "
            f"CheckBox: {check_box_status}, "
            f"RadioButton: {radio_button_status}"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComboBoxListApp()
    window.show()
    sys.exit(app.exec_())