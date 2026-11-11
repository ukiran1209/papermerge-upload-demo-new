"""Run a local upload with Papermerge 3.5.3's path and file-copy helpers."""

import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from papermerge.core.pathlib import docver_path
from papermerge.core.utils.misc import copy_file


class LocalBackend:
    """Demo adapter around the local file writer used by the tagged release."""

    def __init__(self, root: Path):
        self.root = root.resolve()

    async def upload(self, key: Path, content: bytes) -> Path:
        destination = (self.root / key).resolve()
        if key.is_absolute() or not destination.is_relative_to(self.root):
            raise ValueError("Upload path must stay inside the storage root")

        await copy_file(src=content, dst=destination)
        return destination


async def upload_document(
    backend: LocalBackend, filename: str, content: bytes
) -> Path:
    """Store one version of a document under a newly generated UUID."""
    if (
        filename in {"", ".", ".."}
        or any(char in filename for char in ("/", "\\", ":", "\0"))
    ):
        raise ValueError("Expected a plain filename")

    key = docver_path(uuid4(), file_name=filename)
    return await backend.upload(key, content)


async def main() -> None:
    content = b"Papermerge upload demo\n"
    with TemporaryDirectory(prefix="papermerge-upload-") as directory:
        backend = LocalBackend(Path(directory))
        stored = await upload_document(backend, "sample.txt", content)
        if stored.read_bytes() != content:
            raise RuntimeError("Stored file does not match the uploaded bytes")

        print("upload_document -> docver_path -> LocalBackend.upload -> copy_file")
        print(f"Verified {len(content)} bytes in {stored.relative_to(backend.root)}")


if __name__ == "__main__":
    asyncio.run(main())
