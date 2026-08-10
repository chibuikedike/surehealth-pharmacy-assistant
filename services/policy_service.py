from pathlib import Path
from models.document_chunk import DocumentChunk


class PolicyService:
    """
    Loads, chunks, and searches pharmacy policy documents.
    """

    def __init__(self, policy_file: str):
        self._policy_file = Path(policy_file)

        self._document_text = ""
        self._chunks: list[DocumentChunk] = []

        self.reload_policy()

    # ==================================================
    # Public Methods
    # ==================================================

    def search_policy(
        self,
        query: str | None = None,
        limit: int = 10,
    ) -> list[DocumentChunk]:
        """
        Search the policy document using keyword matching.
        """

        if not query:
            return self._chunks[:limit]

        query = query.lower()

        matches = []

        for chunk in self._chunks:
            if query in chunk.text.lower():
                matches.append(chunk)

            if len(matches) >= limit:
                break

        return matches

    def get_policy(self) -> str:
        """
        Return the complete policy document.
        """

        return self._document_text

    def reload_policy(self) -> None:
        """
        Reload the policy document from disk.
        """

        if not self._policy_file.exists():
            raise FileNotFoundError(
                f"Policy file not found: {self._policy_file}"
            )

        self._document_text = self._policy_file.read_text(
            encoding="utf-8"
        )

        self._chunks = self._chunk_document(
            self._document_text
        )

    # ==================================================
    # Private Methods
    # ==================================================

    def _chunk_document(
        self,
        text: str,
    ) -> list[DocumentChunk]:
        """
        Split a document into searchable chunks.

        Each paragraph becomes one chunk.
        """

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        return [
            DocumentChunk(
                id=index,
                text=paragraph,
            )
            for index, paragraph in enumerate(
                paragraphs,
                start=1,
            )
        ]

    # ==================================================
    # Properties
    # ==================================================

    @property
    def policy_file(self) -> Path:
        return self._policy_file

    @property
    def policy_text(self) -> str:
        return self._document_text

    @property
    def chunks(self) -> list[DocumentChunk]:
        return self._chunks

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    @property
    def policy_length(self) -> int:
        return len(self._document_text)

    # ==================================================
    # Special Methods
    # ==================================================

    def __len__(self) -> int:
        return self.chunk_count

    def __repr__(self) -> str:
        return (
            f"PolicyService("
            f"file='{self._policy_file.name}', "
            f"chunks={self.chunk_count})"
        )
