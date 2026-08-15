import contextvars
from typing import Optional, TypedDict


class Artifact(TypedDict):
    path: str
    kind: str  # untuk menyimpan jenis file: "audio"/"document"
    caption: Optional[str]


_artifacts: contextvars.ContextVar[Optional[list[Artifact]]] = contextvars.ContextVar(
    "artifacts", default=None
)


def start() -> None:
    """Mulai keranjang artifact baru untuk request saat ini"""
    print("ARTIFACT START")
    _artifacts.set([])


def add(path: str, kind: str = "audio", caption: Optional[str] = None) -> None:
    """Catat satu artifact untuk dikirim oleh layer pengiriman (CLI/Telegram)"""
    print("ARTIFACT ADD")
    print("path:", path)

    bucket = _artifacts.get()
    print("bucket:", bucket)

    if bucket is None:
        print("BUCKET IS NONE!")
        return

    bucket.append({"path": path, "kind": kind, "caption": caption})
    print("bucket after append:", bucket)


def collect() -> list[Artifact]:
    """Ambil semua artifact yang terkumpul pada request ini"""
    bucket = _artifacts.get()

    print("ARTIFACT COLLECT")
    print("bucket:", bucket)

    return _artifacts.get() or []
