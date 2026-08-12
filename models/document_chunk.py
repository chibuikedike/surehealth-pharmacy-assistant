from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunk:
    """
    Represents a searchable section of a policy document.
    """

    id: int
    text: str
    section: str = ""
    subsection: str = ""
    title: str = ""

    @property
    def searchable_text(self) -> str:
        """
        Text used by the retrieval system.

        Includes document structure as well as
        the actual chunk content.
        """

        return " ".join(
            part
            for part in [
                self.section,
                self.subsection,
                self.title,
                self.text,
            ]
            if part
        )

    def to_dict(self) -> dict:
        """
        Convert the document chunk to a dictionary.
        """

        return {
            "id": self.id,
            "section": self.section,
            "subsection": self.subsection,
            "title": self.title,
            "text": self.text,
        }

    def __str__(self) -> str:
        return self.text
