"""Inspección de los informes en PDF: extrae el texto a .txt (al lado de cada PDF) y busca palabras clave
ligadas a las variables del sintético, mostrando página y fragmento.

PDFs incluidos:
  sbi_card_investor_presentations/   SBI Card (2.º emisor de India): gasto por tarjeta, saldo por tarjeta,
                                     mezcla online, mezcla de gasto, EMI/revolving, morosidad.
  crif_highmark_reports/             CRIF High Mark (buró de crédito): edad, sexo y nuevos tarjetahabientes,
                                     morosidad de tarjetas.
  worldline_digital_payments/        Worldline India: ticket promedio, gasto por categoría (MCC).
  mospi_plfs_2023_24/                PLFS (MoSPI): ingreso mensual por tipo de empleo, ocupación.

Uso (desde la raíz del repo):
  .venv/bin/python -I dataReal/scripts/inspeccionar_pdfs.py                 # todos los PDFs
  .venv/bin/python -I dataReal/scripts/inspeccionar_pdfs.py "spends per card" # buscar un término propio
"""
import re
import sys
from pathlib import Path

from pypdf import PdfReader

BASE = Path(__file__).resolve().parent.parent
CARPETAS = ["sbi_card_investor_presentations", "crif_highmark_reports", "worldline_digital_payments",
            "mospi_plfs_2023_24"]
CLAVES = sys.argv[1:] or [
    "spends per card", "spend per card", "receivables per card", "average ticket", "ATS",
    "online", "revolv", "EMI", "GNPA", "delinquen", "90+", "credit card",
    "age", "women", "female", "18-30", "<30", "salaried", "self-employed", "self employed",
    "average monthly", "earnings", "grocery", "fuel", "travel", "utilit", "dining", "cash",
]


def texto_pdf(pdf: Path) -> list[str]:
    txt = pdf.with_suffix(".txt")
    if txt.exists():
        return txt.read_text(encoding="utf-8").split("\f")
    paginas = []
    for p in PdfReader(pdf).pages:
        try:
            paginas.append(p.extract_text() or "")
        except Exception as e:  # algunas páginas con gráficos fallan
            paginas.append(f"[error extrayendo: {e}]")
    txt.write_text("\f".join(paginas), encoding="utf-8")
    return paginas


for carpeta in CARPETAS:
    for pdf in sorted((BASE / carpeta).glob("*.pdf")):
        paginas = texto_pdf(pdf)
        n_chars = sum(len(p) for p in paginas)
        print(f"\n{'=' * 100}\n{pdf.relative_to(BASE)} | {len(paginas)} páginas | {n_chars:,} caracteres de texto")
        if n_chars < 500:
            print("  ⚠ casi sin texto extraíble (PDF escaneado o solo imágenes)")
            continue
        for clave in CLAVES:
            patron = re.compile(re.escape(clave), re.IGNORECASE)
            hits = [(i + 1, m.start(), p) for i, p in enumerate(paginas) for m in patron.finditer(p)]
            if not hits:
                continue
            paginas_hit = sorted({h[0] for h in hits})
            print(f"  '{clave}': {len(hits)} coincidencias en páginas {paginas_hit[:15]}")
            for pag, pos, p in hits[:2]:
                frag = re.sub(r"\s+", " ", p[max(0, pos - 120): pos + 160])
                print(f"      p.{pag}: …{frag}…")
