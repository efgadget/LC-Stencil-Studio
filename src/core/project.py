from dataclasses import dataclass, field
from uuid import uuid4

from core.material import Material


@dataclass
class Project:
    """
    Rappresenta un progetto LC Stencil Studio.
    """

    name: str
    material: Material

    id: str = field(default_factory=lambda: str(uuid4()))

    layers: list = field(default_factory=list)

    modified: bool = False

    def add_layer(self, layer):

        self.layers.append(layer)

        self.modified = True

    def remove_layer(self, layer):

        if layer in self.layers:

            self.layers.remove(layer)

            self.modified = True