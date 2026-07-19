"""Upload widget for tagged XML files in workshop notebooks."""

from __future__ import annotations

from pathlib import Path

import ipywidgets as widgets
from IPython.display import display

UPLOAD_DIR = Path("data")  # legacy; use _resolve_data_dir()
XML_PATH: Path | None = None


def _resolve_data_dir() -> Path:
    candidates = (
        Path("data"),
        Path("../data"),
        Path("../../data"),
        Path("../../../data"),
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    for candidate in candidates:
        parent = candidate.parent
        if (parent / "scripts").is_dir() or (parent / "notebooks").is_dir():
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
    data = Path("data")
    data.mkdir(exist_ok=True)
    return data


def show_upload() -> None:
    """Display a file upload button and save the XML into the session."""
    global XML_PATH

    data_dir = _resolve_data_dir()

    upload = widgets.FileUpload(
        accept=".xml,application/xml,text/xml",
        multiple=False,
        description="Choisir un XML",
        button_style="primary",
    )
    status = widgets.Output()

    def save_uploaded_file(change):
        global XML_PATH
        with status:
            status.clear_output()
            if not upload.value:
                return

            file_info = upload.value[0]
            content = file_info["content"]
            if hasattr(content, "tobytes"):
                content = content.tobytes()

            XML_PATH = data_dir / file_info["name"]
            XML_PATH.write_bytes(content)
            print(f"Fichier enregistré dans votre session : {XML_PATH}")
            print("Vous pouvez maintenant exécuter la cellule suivante.")

    upload.observe(save_uploaded_file, names="value")
    display(widgets.VBox([upload, status]))


def get_xml_path() -> Path:
    """Return the uploaded XML path, or the most recent file in data/."""
    if XML_PATH is not None and XML_PATH.exists():
        return XML_PATH

    data_dir = _resolve_data_dir()
    xml_paths = sorted(
        data_dir.glob("*.xml"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not xml_paths:
        raise FileNotFoundError(
            "Aucun fichier XML trouvé. Téléversez d'abord votre fichier dans la cellule ci-dessus."
        )
    return xml_paths[0]
