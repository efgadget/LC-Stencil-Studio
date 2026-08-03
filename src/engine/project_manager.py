from core.material import Material
from core.project import Project


class ProjectManager:
    """
    Gestisce il ciclo di vita dei progetti.
    """

    def __init__(self):

        self.current_project = None

    def new_project(
        self,
        name="Nuovo progetto",
        width=300,
        height=300,
        thickness=0.19,
        material_name="Mylar"
    ):

        material = Material(
            name=material_name,
            width=width,
            height=height,
            thickness=thickness
        )

        self.current_project = Project(
            name=name,
            material=material
        )

        return self.current_project

    def get_project(self):

        return self.current_project

    def has_project(self):

        return self.current_project is not None

    def close_project(self):

        self.current_project = None

    def project_name(self):

        if self.current_project:

            return self.current_project.name

        return ""