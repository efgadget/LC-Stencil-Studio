"""
LC Stencil Studio
Project Manager
Versione 0.3.0
"""

from core.project import Project
from core.material_library import MaterialLibrary


class ProjectManager:
    """
    Gestisce il ciclo di vita dei progetti.
    """

    def __init__(self):

        self.library = MaterialLibrary()

        self.current_project = None

    def new_project(

        self,

        name="Nuovo progetto",

        material_name="Mylar 300x300"

    ):

        material = self.library.get(material_name)

        if material is None:

            raise ValueError(
                f"Materiale '{material_name}' non trovato."
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