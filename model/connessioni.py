from dataclasses import dataclass

from model.artObject import ArtObject


@dataclass
class Connessione:
    o1: ArtObject  # alternativa int
    o2: ArtObject
    peso: int

    def __str__(self) -> str:
        return (f"Arco: {self.o1.object_id} -"
                f" {self.o2.object_id} - peso: {self.peso}")
