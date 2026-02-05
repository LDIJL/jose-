from __future__ import annotations

from pathlib import Path


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf(output_path: Path) -> None:
    width, height = 595, 842  # A4 in points

    heading = "Formulación del problema"
    body_lines = [
        "El problema que se quiere estudiar es que las salsas especializadas LUYVAN todavía",
        "no logran que la gente las conozca, las pruebe y las compre de forma constante en la",
        "Ciudad de México, sobre todo cuando se intenta venderlas en cadenas como Tiendas",
        "3B, Neto, Bodega Aurrerá y otras parecidas.",
        "",
        "En pocas palabras, se busca entender cómo una empresa nueva que distribuye",
        "salsas artesanales puede ganarse la confianza de los consumidores y lograr entrar y",
        "mantenerse en este tipo de tiendas. Esto no es sencillo porque muchas personas",
        "prefieren las salsas de siempre, las marcas conocidas y los sabores a los que ya",
        "están acostumbradas. Además, las tiendas suelen ser cuidadosas con lo que ponen",
        "en sus estantes: tienen poco espacio y normalmente eligen productos que ya se",
        "venden bien o que vienen de marcas con historia.",
        "",
        "También hay riesgos claros: que la gente no compre la salsa por costumbre o por",
        "desconfianza, que la sienta \"rara\" o diferente a lo que suele comer, o que las tiendas",
        "no quieran darle lugar porque al principio podría venderse lento. A esto se suman",
        "retos prácticos: asegurar que siempre haya producto disponible, que se vea bien en el",
        "estante y que el empaque y el mensaje expliquen bien por qué vale la pena probarla",
        "para que la gente la compre otra vez.",
        "",
        "Resolver esto es importante para que LUYVAN pueda crecer, mantenerse en estas",
        "tiendas y vender más dentro del mercado al que quiere llegar.",
    ]

    content_lines = []
    content_lines.append("q")
    content_lines.append("0.93 0.93 0.93 rg")
    content_lines.append("50 90 495 690 re")
    content_lines.append("f")
    content_lines.append("Q")

    content_lines.append("BT")
    content_lines.append("/F2 18 Tf")
    content_lines.append("0.1 0.3 0.4 rg")
    content_lines.append("70 750 Td")
    content_lines.append(f"({pdf_escape(heading)}) Tj")
    content_lines.append("ET")

    content_lines.append("BT")
    content_lines.append("/F1 11 Tf")
    content_lines.append("0 0 0 rg")
    content_lines.append("70 720 Td")
    content_lines.append("14 TL")
    for line in body_lines:
        content_lines.append(f"({pdf_escape(line)}) Tj")
        content_lines.append("T*")
    content_lines.append("ET")

    content_stream = "\n".join(content_lines).encode("latin-1")

    objects: list[bytes] = []

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [3 0 R] /Count 1 >>".encode("ascii"))
    objects.append(
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
        f"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>".encode(
            "ascii"
        )
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    objects.append(
        b"<< /Length "
        + str(len(content_stream)).encode("ascii")
        + b" >>\nstream\n"
        + content_stream
        + b"\nendstream"
    )

    xref_positions = []
    pdf_parts = [b"%PDF-1.4\n"]

    for index, obj in enumerate(objects, start=1):
        xref_positions.append(sum(len(part) for part in pdf_parts))
        pdf_parts.append(f"{index} 0 obj\n".encode("ascii"))
        pdf_parts.append(obj)
        pdf_parts.append(b"\nendobj\n")

    xref_start = sum(len(part) for part in pdf_parts)
    pdf_parts.append(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf_parts.append(b"0000000000 65535 f \n")
    for pos in xref_positions:
        pdf_parts.append(f"{pos:010d} 00000 n \n".encode("ascii"))

    pdf_parts.append(
        b"trailer\n"
        + f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode("ascii")
        + b"startxref\n"
        + str(xref_start).encode("ascii")
        + b"\n%%EOF\n"
    )

    output_path.write_bytes(b"".join(pdf_parts))


if __name__ == "__main__":
    build_pdf(Path("formulacion_problema.pdf"))
