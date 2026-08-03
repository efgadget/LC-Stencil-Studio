import sys

from PySide6.QtWidgets import QApplication

from ui.windows.main_window import MainWindow
from engine.project_manager import ProjectManager


def main():

    print("=" * 40)
    print("LC STENCIL STUDIO")
    print("Versione 0.3.0")
    print("=" * 40)

    app = QApplication(sys.argv)

    manager = ProjectManager()

    project = manager.new_project(
        name="Nuovo progetto",
        material_name="Mylar 300x300"
    )

    print("Project:", project.name)
    print("Material:", project.material)

    window = MainWindow(project)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()