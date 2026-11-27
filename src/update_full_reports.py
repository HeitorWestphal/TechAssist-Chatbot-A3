"""Script para sincronizar e compilar RELATORIO_TECNICO_A3.docx e RELATORIO_TECNICO_A3.pdf com 14 figuras científicas."""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MD_PATH = os.path.join(DOCS_DIR, "RELATORIO_TECNICO_A3.md")
DOCX_PATH = os.path.join(DOCS_DIR, "RELATORIO_TECNICO_A3.docx")
PDF_PATH = os.path.join(DOCS_DIR, "RELATORIO_TECNICO_A3.pdf")

FIG_MAP = {
    "Figura 1": "grafico_benchmark_modelos.png",
    "Figura 2": "grafico_latencia_modelos.png",
    "Figura 3": "grafico_pca_espaco_vetorial.png",
    "Figura 4": "grafico_feature_importance_tfidf.png",
    "Figura 5": "grafico_calibracao_threshold.png",
    "Figura 6": "grafico_curva_precision_recall.png",
    "Figura 7": "grafico_matriz_confusao.png",
    "Figura 8": "grafico_impacto_operacional_helpdesk.png",
    "Figura 9": "grafico_radar_tradeoffs.png",
    "Figura 10": "grafico_benchmark_estresse.png",
    "Figura 11": "grafico_cross_validation_kfold.png",
    "Figura 12": "grafico_estudo_ablacao.png",
    "Figura 13": "grafico_curva_aprendizado.png",
    "Figura 14": "grafico_comparativo_recursos_roi.png"
}

def generate_docx():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = docx.Document()
    
    # Configurar margens
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith("# "):
            heading_text = line[2:].strip()
            p = doc.add_paragraph()
            run = p.add_run(heading_text)
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 64, 175) # Blue-800
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
        elif line.startswith("## "):
            heading_text = line[3:].strip()
            p = doc.add_paragraph()
            run = p.add_run(heading_text)
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42) # Slate-900
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
        elif line.startswith("Figura "):
            p = doc.add_paragraph()
            run = p.add_run(line)
            run.font.size = Pt(9)
            run.font.italic = True
            run.font.color.rgb = RGBColor(71, 85, 105)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)

            # Inserir imagem correspondente
            matched_img = None
            for fig_key, img_file in FIG_MAP.items():
                if line.startswith(fig_key):
                    matched_img = img_file
                    break
            
            if matched_img:
                img_path = os.path.join(RESULTS_DIR, matched_img)
                if os.path.exists(img_path):
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    # Se for radar, mantém proporção quadrada
                    if "radar" in matched_img:
                        p_img.add_run().add_picture(img_path, width=Inches(4.0))
                    else:
                        p_img.add_run().add_picture(img_path, width=Inches(5.5))
                    p_img.paragraph_format.space_after = Pt(8)
        else:
            p = doc.add_paragraph()
            run = p.add_run(line)
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(30, 41, 59)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(4)

        i += 1

    doc.save(DOCX_PATH)
    print(f"[OK] Gerado {DOCX_PATH} com 14 figuras incorporadas!")

def generate_pdf():
    doc_pdf = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontSize=12, leading=15, textColor=colors.HexColor('#0f172a'),
        alignment=1, fontName='Helvetica-Bold', spaceAfter=8
    )
    inst_style = ParagraphStyle(
        'InstTitle', parent=styles['Normal'],
        fontSize=8.5, leading=11, textColor=colors.HexColor('#475569'),
        alignment=1, fontName='Helvetica-Bold', spaceAfter=6
    )
    meta_style = ParagraphStyle(
        'DocMeta', parent=styles['Normal'],
        fontSize=8.0, leading=11, textColor=colors.HexColor('#1e293b'),
        alignment=0, spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Heading2'],
        fontSize=10.5, leading=13.5, textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4
    )
    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Heading3'],
        fontSize=9.0, leading=12.0, textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=8.0, leading=11.0, textColor=colors.HexColor('#1e293b'),
        alignment=4, spaceAfter=4
    )
    caption_style = ParagraphStyle(
        'Caption', parent=styles['Normal'],
        fontSize=7.5, leading=9.5, textColor=colors.HexColor('#475569'),
        alignment=1, fontName='Helvetica-Oblique', spaceAfter=4
    )

    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    story = []
    lines = md_text.split("\n")
    i = 0
    first_p = True

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if first_p and line.startswith("CURSO"):
            story.append(Paragraph(line, inst_style))
            story.append(Spacer(1, 4))
            first_p = False
        elif line.startswith("# TECHASSIST:"):
            story.append(Paragraph(line[2:], title_style))
            story.append(Spacer(1, 6))
        elif line.startswith("# "):
            story.append(Paragraph(line[2:], h1_style))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], h2_style))
        elif line.startswith("Figura "):
            story.append(Paragraph(line, caption_style))
            matched_img = None
            for fig_key, img_file in FIG_MAP.items():
                if line.startswith(fig_key):
                    matched_img = img_file
                    break
            if matched_img:
                img_path = os.path.join(RESULTS_DIR, matched_img)
                if os.path.exists(img_path):
                    if "radar" in matched_img:
                        story.append(Image(img_path, width=280, height=280))
                    else:
                        story.append(Image(img_path, width=420, height=200))
                    story.append(Spacer(1, 6))
        elif line.startswith("• ") or line.startswith("Equipe:") or line.startswith("Repositório:") or line.startswith("Data"):
            story.append(Paragraph(line, meta_style))
        else:
            story.append(Paragraph(line, body_style))

        i += 1

    doc_pdf.build(story)
    print(f"[OK] Gerado {PDF_PATH} com 14 figuras em alta resolução!")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()
