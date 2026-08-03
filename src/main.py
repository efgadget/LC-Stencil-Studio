import sys

from PySide6.QtWidgets import QApplication

from ui.windows.main_window import MainWindow
from ui.dialogs.new_project_dialog import NewProjectDialog


def main():

    print("=" * 40)
    print("LC STENCIL STUDIO")
    print("Versione 0.4.0")
    print("=" * 40)

    app = QApplication(sys.argv)

    dialog = NewProjectDialog()

    if dialog.exec() != dialog.DialogCode.Accepted:
        sys.exit()

    project = dialog.get_project()

    print(project.name)
    print(project.material)

    window = MainWindow(project)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()