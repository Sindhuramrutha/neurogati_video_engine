"""Turns a .pptx deck into one accurate PNG per slide.

PowerPoint's own COM automation (win32com) was tried first and confirmed
non-viable on this machine -- Presentations.Open/Visible/Quit all fail
with the same COM error, reproduced identically from both a tool-launched
process and a terminal opened directly, ruling out a session/window-station
workaround. This uses LibreOffice instead, which is built for exactly this
kind of unattended conversion: `soffice --headless --convert-to pdf` turns
the whole deck into one PDF (one page per slide), then PyMuPDF (pure
Python, no extra system dependency) rasterizes each page to a PNG. Both
steps confirmed working end-to-end on a real 21-slide pilot deck, output
visually verified against the source.
"""

import subprocess
from pathlib import Path

import fitz  # PyMuPDF

_SOFFICE_CANDIDATES = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
]


def _find_soffice() -> str:
    for candidate in _SOFFICE_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "soffice.exe not found -- LibreOffice must be installed "
        "(https://www.libreoffice.org/download/download/)."
    )


def export_slides_to_png(pptx_path: Path, out_dir: Path, dpi: int = 200) -> list[Path]:
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = out_dir / f"{Path(pptx_path).stem}.pdf"
    subprocess.run(
        [
            _find_soffice(), "--headless", "--convert-to", "pdf",
            "--outdir", str(out_dir), str(pptx_path),
        ],
        check=True,
        capture_output=True,
        timeout=180,
    )
    if not pdf_path.exists():
        raise FileNotFoundError(f"LibreOffice did not produce the expected PDF at {pdf_path}")

    doc = fitz.open(str(pdf_path))
    matrix = fitz.Matrix(dpi / 72, dpi / 72)  # PDF's native unit is 72 DPI
    png_paths = []
    for i, page in enumerate(doc, start=1):
        png_path = out_dir / f"slide_{i:02d}.png"
        page.get_pixmap(matrix=matrix).save(str(png_path))
        png_paths.append(png_path)
    doc.close()
    return png_paths
