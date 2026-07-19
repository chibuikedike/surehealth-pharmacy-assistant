from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunk:
    """
    Represents a searchable chunk of a document.
    """

    id: int
    text: str

    def to_dict(self) -> dict:
        """
        Convert the document chunk to a dictionary.
        """

        return {
            "id": self.id,
            "text": self.text,
        }

    def __str__(self) -> str:
        return self.text