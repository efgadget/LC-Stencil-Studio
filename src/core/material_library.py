"""
LC Stencil Studio
Material Library
Versione 0.3.0
"""

import json
from pathlib import Path

from core.material import Material


class MaterialLibrary:

    def __init__(self):

        self.materials = []

        self.load()

    def load(self):

        path = (
            Path(__file__)
            .parent.parent
            / "resources"
            / "materials.json"
        )

        with open(path, "r", encoding="utf-8") as file:

            data = json.load(file)

        self.materials = []

        for item in data:

            material = Material(
                name=item["name"],
                width=item["width"],
                height=item["height"],
                thickness=item["thickness"]
            )

            self.materials.append(material)

    def names(self):

        return [m.name for m in self.materials]

    def get(self, name):

        for material in self.materials:

            if material.name == name:
                return material

        return None