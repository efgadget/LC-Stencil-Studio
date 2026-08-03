import sys

from PySide6.QtWidgets import QApplication

from ui.windows.main_window import MainWindow

from engine.project_manager import ProjectManager


def main():

    print("===================================")
    print("LC STENCIL STUDIO")
    print("Versione 0.1.0-alpha")
    print("===================================")

    app = QApplication(sys.argv)

    manager = ProjectManager()

    project = manager.new_project(
        name="Nuovo progetto",
        width=300,
        height=300,
        thickness=0.19,
        material_name="Mylar"
    )

    print("Project:", project.name)
    print("Material:", project.material)

    window = MainWindow(project)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
