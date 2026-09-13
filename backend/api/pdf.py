import re

from fpdf import FPDF

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_TABLE_SEPARATOR_RE = re.compile(r"^[|\-:\s]+$")
_MAX_TOKEN_LEN = 80


def _break_long_tokens(line: str) -> str:
    """Insert spaces into tokens fpdf2 couldn't otherwise wrap (e.g. dash-only table rules)."""
    return " ".join(
        " ".join(tok[i:i + _MAX_TOKEN_LEN] for i in range(0, len(tok), _MAX_TOKEN_LEN))
        if len(tok) > _MAX_TOKEN_LEN else tok
        for tok in line.split(" ")
    )


def _clean(line: str) -> str:
    line = _BOLD_RE.sub(r"\1", line)
    line = line.replace("*", "").replace("_", "")
    line = line.encode("latin-1", "ignore").decode("latin-1").strip()
    if _TABLE_SEPARATOR_RE.match(line):
        return ""
    line = line.replace("|", "  ")
    return _break_long_tokens(line)


def render_pdf(text: str) -> bytes:
    """Render markdown-ish blog text into a simple, readable PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for raw_line in text.splitlines():
        stripped = raw_line.strip()

        if not stripped:
            pdf.ln(4)
            continue

        # Prefixes are detected before _clean() strips markdown markers.
        if stripped.startswith("### "):
            body = _clean(stripped[4:])
            if body:
                pdf.set_font("Helvetica", "B", 13)
                pdf.multi_cell(pdf.epw, 8, body)
        elif stripped.startswith("## "):
            body = _clean(stripped[3:])
            if body:
                pdf.set_font("Helvetica", "B", 16)
                pdf.multi_cell(pdf.epw, 9, body)
        elif stripped.startswith("# "):
            body = _clean(stripped[2:])
            if body:
                pdf.set_font("Helvetica", "B", 20)
                pdf.multi_cell(pdf.epw, 10, body)
        elif stripped.startswith(("- ", "* ")):
            body = _clean(stripped[2:])
            if body:
                pdf.set_font("Helvetica", "", 11)
                pdf.multi_cell(pdf.epw, 7, f"  - {body}")
        else:
            body = _clean(stripped)
            if body:
                pdf.set_font("Helvetica", "", 11)
                pdf.multi_cell(pdf.epw, 7, body)
            else:
                pdf.ln(4)

    return bytes(pdf.output())
