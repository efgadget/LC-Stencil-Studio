"""
LC Stencil Studio
Document Engine
Sprint 010
"""

from core.project import Project


class DocumentEngine:

    def __init__(self):

        self.project = None

    def has_project(self):

        return self.project is not None

    def set_project(self, project: Project):

        self.project = project

    def get_project(self):

        return self.project

    def close_project(self):

        self.project = None

    def project_name(self):

        if self.project is None:
            return ""

        return self.project.name

    def is_modified(self):

        if self.project is None:
            return False

        return self.project.modified

    def set_modified(self, value=True):

        if self.project is not None:
            self.project.modified = value