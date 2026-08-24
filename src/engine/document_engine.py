"""
LC Stencil Studio
Document Engine
Release 0.8.0
"""

import json
from pathlib import Path

from core.project import Project
from core.material import Material


class DocumentEngine:

    FORMAT_VERSION = 1

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
        return "" if self.project is None else self.project.name

    def is_modified(self):
        return False if self.project is None else self.project.modified

    def set_modified(self, value=True):
        if self.project is not None:
            self.project.modified = value

    def save_project(self, filename, image_path="", image_geometry=None):
        if self.project is None:
            return False
        path = Path(filename)
        if path.suffix.lower() != ".lcs":
            path = path.with_suffix(".lcs")
        self.project.file_path = str(path)
        self.project.image_path = image_path or self.project.image_path
        self.project.image_geometry = image_geometry or self.project.image_geometry or {}
        data = {
            "format": "LC-Stencil-Studio",
            "version": self.FORMAT_VERSION,
            "project": {
                "id": self.project.id,
                "name": self.project.name,
                "material": {
                    "name": self.project.material.name,
                    "width": self.project.material.width,
                    "height": self.project.material.height,
                    "thickness": self.project.material.thickness,
                    "color": self.project.material.color,
                },
                "image_path": self.project.image_path,
                "image_geometry": self.project.image_geometry,
            },
        }
        try:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            return False
        self.project.modified = False
        return True

    def load_project(self, filename):
        path = Path(filename)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            pdata = data["project"]
            mdata = pdata["material"]
            material = Material(
                name=mdata["name"], width=float(mdata["width"]),
                height=float(mdata["height"]),
                thickness=float(mdata.get("thickness", 0.0)),
                color=mdata.get("color", "white"),
            )
            project = Project(name=pdata["name"], material=material)
            project.id = pdata.get("id", project.id)
            project.file_path = str(path)
            project.image_path = pdata.get("image_path", "")
            project.image_geometry = pdata.get("image_geometry", {})
            project.modified = False
        except (OSError, ValueError, KeyError, TypeError):
            return None
        self.project = project
        return project
