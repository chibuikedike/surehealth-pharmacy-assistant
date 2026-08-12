from pathlib import Path
import re

from models.document_chunk import DocumentChunk


class PolicyService:
    """
    Loads, chunks, and searches the pharmacy policy document.
    """

    STOP_WORDS = {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "of",
        "to",
        "for",
        "in",
        "on",
        "at",
        "and",
        "or",
        "what",
        "which",
        "how",
        "does",
        "do",
        "can",
        "could",
        "would",
        "should",
        "i",
        "we",
        "our",
        "your",
        "me",
        "please",
        "tell",
        "about",
    }

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
        limit: int = 5,
    ) -> list[DocumentChunk]:
        """
        Search the policy document using keyword matching
        and relevance scoring.
        """

        if not query:
            return self._chunks[:limit]

        query = query.strip().lower()

        if not query:
            return []

        keywords = self._extract_keywords(query)

        if not keywords:
            return []

        scored_chunks = []

        for chunk in self._chunks:

            searchable_text = (
                chunk.searchable_text.lower()
            )

            score = 0

            # ------------------------------------------
            # Keyword matching
            # ------------------------------------------

            for keyword in keywords:

                occurrences = searchable_text.count(
                    keyword
                )

                score += occurrences

            # ------------------------------------------
            # Exact phrase bonus
            # ------------------------------------------

            if query in searchable_text:
                score += 5

            # ------------------------------------------
            # Title bonus
            # ------------------------------------------

            title = chunk.title.lower()

            for keyword in keywords:
                if keyword in title:
                    score += 3

            # ------------------------------------------
            # Keep relevant chunks
            # ------------------------------------------

            if score > 0:
                scored_chunks.append(
                    (score, chunk)
                )

        # ----------------------------------------------
        # Highest relevance first
        # ----------------------------------------------

        scored_chunks.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            chunk
            for score, chunk
            in scored_chunks[:limit]
        ]

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

        self._document_text = (
            self._policy_file.read_text(
                encoding="utf-8"
            )
        )

        self._chunks = self._chunk_document(
            self._document_text
        )

    # ==================================================
    # Keyword Processing
    # ==================================================

    def _extract_keywords(
        self,
        query: str,
    ) -> list[str]:
        """
        Extract meaningful keywords from a query.
        """

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query,
        )

        keywords = [
            word
            for word in words
            if word not in self.STOP_WORDS
            and len(word) > 1
        ]

        return list(dict.fromkeys(keywords))

    # ==================================================
    # Document Chunking
    # ==================================================

    def _chunk_document(
        self,
        text: str,
    ) -> list[DocumentChunk]:
        """
        Convert the policy document into structured
        searchable chunks.

        Each major policy heading becomes a chunk.
        """

        lines = text.splitlines()

        chunks = []

        current_section = ""
        current_title = ""
        current_content = []

        chunk_id = 1

        def save_chunk():
            nonlocal chunk_id
            nonlocal current_content

            content = "\n".join(
                current_content
            ).strip()

            if not content:
                return

            chunks.append(
                DocumentChunk(
                    id=chunk_id,
                    section=current_section,
                    title=current_title,
                    text=content,
                )
            )

            chunk_id += 1
            current_content = []

        for line in lines:

            stripped = line.strip()

            if not stripped:
                continue

            # ------------------------------------------
            # Major SECTION heading
            # ------------------------------------------

            if stripped.startswith("# SECTION "):

                save_chunk()

                current_section = stripped.lstrip(
                    "# "
                )

                current_title = ""

                continue

            # ------------------------------------------
            # Numbered policy heading
            # ------------------------------------------

            if re.match(
                r"^#{1,6}\s+\d+\.\d+",
                stripped,
            ):

                save_chunk()

                current_title = stripped.lstrip(
                    "# "
                )

                continue

            # ------------------------------------------
            # Other headings
            # ------------------------------------------
            
            if stripped.startswith("#"):

                heading = stripped.lstrip(
                    "# "
                )

                if current_title:
                    current_content.append(
                        heading
                    )
                else:
                    current_title = heading

                continue

            # ------------------------------------------
            # Normal content
            # ------------------------------------------

            current_content.append(
                stripped
            )

        # Save final chunk
        save_chunk()

        return chunks

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
