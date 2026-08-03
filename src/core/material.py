from dataclasses import dataclass


@dataclass
class Material:
    """
    Rappresenta il materiale sul quale verrà realizzato lo stencil.
    Tutte le misure sono espresse in millimetri.
    """

    name: str
    width: float
    height: float
    thickness: float = 0.0
    color: str = "white"

    @property
    def size(self) -> str:
        return f"{self.width} x {self.height} mm"

    @property
    def area(self) -> float:
        return self.width * self.height

    def __str__(self):
        return f"{self.name} ({self.size})"