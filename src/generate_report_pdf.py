"""Gera a versão PDF do Relatório Técnico da A3 com todas as figuras científicas e formatação ABNT."""
import os
import docx
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCX_PATH = os.path.join(BASE_DIR, "docs", "RELATORIO_TECNICO_A3.docx")
PDF_PATH = os.path.join(BASE_DIR, "docs", "RELATORIO_TECNICO_A3.pdf")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

def build_pdf():
    doc_docx = docx.Document(DOCX_PATH)
    doc_pdf = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontSize=13, leading=16, textColor=colors.HexColor('#0f172a'),
        alignment=1, fontName='Helvetica-Bold', spaceAfter=8
    )
    inst_style = ParagraphStyle(
        'InstTitle', parent=styles['Normal'],
        fontSize=8.5, leading=11, textColor=colors.HexColor('#475569'),
        alignment=1, fontName='Helvetica-Bold', spaceAfter=6
    )
    meta_style = ParagraphStyle(
        'DocMeta', parent=styles['Normal'],
        fontSize=8.5, leading=12, textColor=colors.HexColor('#1e293b'),
        alignment=0, spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Heading2'],
        fontSize=11, leading=14, textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4
    )
    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Heading3'],
        fontSize=9.5, leading=12.5, textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=8.5, leading=12, textColor=colors.HexColor('#1e293b'),
        alignment=4, spaceAfter=6
    )
    caption_style = ParagraphStyle(
        'Caption', parent=styles['Normal'],
        fontSize=7.5, leading=10, textColor=colors.HexColor('#475569'),
        alignment=1, fontName='Helvetica-Oblique', spaceAfter=6
    )

    fig_map = {
        "Figura 1": "grafico_benchmark_modelos.png",
        "Figura 2": "grafico_latencia_modelos.png",
        "Figura 3": "grafico_pca_espaco_vetorial.png",
        "Figura 4": "grafico_feature_importance_tfidf.png",
        "Figura 5": "grafico_calibracao_threshold.png",
        "Figura 6": "grafico_curva_precision_recall.png",
        "Figura 7": "grafico_matriz_confusao.png",
        "Figura 8": "grafico_impacto_operacional_helpdesk.png"
    }

    story = []

    for i, p in enumerate(doc_docx.paragraphs):
        text = p.text.strip()
        if not text:
            continue

        if i == 0:
            story.append(Paragraph(text.replace("\n", "<br/>"), inst_style))
            story.append(Spacer(1, 4))
        elif i == 1:
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 6))
        elif i == 2:
            story.append(Paragraph(text.replace("\n", "<br/>"), meta_style))
            story.append(Spacer(1, 8))
        elif text.startswith("1. ") or text.startswith("2. ") or text.startswith("3. ") or text.startswith("4. ") or text.startswith("5. ") or text.startswith("6. ") or text.startswith("7. ") or text.startswith("8. "):
            story.append(Paragraph(text, h1_style))
        elif any(text.startswith(f"{n}.") for n in ["2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "4.3", "5.1", "5.2", "6.1", "6.2", "6.3"]):
            story.append(Paragraph(text, h2_style))
        elif text.startswith("Figura "):
            story.append(Paragraph(text, caption_style))
            for fig_key, img_name in fig_map.items():
                if text.startswith(fig_key):
                    img_path = os.path.join(RESULTS_DIR, img_name)
                    if os.path.exists(img_path):
                        story.append(Image(img_path, width=420, height=210))
                        story.append(Spacer(1, 6))
                    break
        else:
            story.append(Paragraph(text.replace("\n", "<br/>"), body_style))

    # Adiciona as novas figuras 9, 10 e 11 no final da seção técnica
    story.append(Spacer(1, 8))
    story.append(Paragraph("Figura 9 — Análise Multicritério de Decisão Arquitetural (Radar de Trade-offs AHP).", caption_style))
    f9_path = os.path.join(RESULTS_DIR, "grafico_radar_tradeoffs.png")
    if os.path.exists(f9_path):
        story.append(Image(f9_path, width=320, height=320))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Figura 10 — Benchmark de Carga, Estresse e Throughput (RPS) sob Concorrência.", caption_style))
    f10_path = os.path.join(RESULTS_DIR, "grafico_benchmark_estresse.png")
    if os.path.exists(f10_path):
        story.append(Image(f10_path, width=420, height=210))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Figura 11 — Validação Cruzada Estratificada em 5 Folds (5-Fold Stratified CV).", caption_style))
    f11_path = os.path.join(RESULTS_DIR, "grafico_cross_validation_kfold.png")
    if os.path.exists(f11_path):
        story.append(Image(f11_path, width=420, height=210))
        story.append(Spacer(1, 6))

    doc_pdf.build(story)
    print(f"[OK] Gerado {PDF_PATH} com sucesso!")

if __name__ == "__main__":
    build_pdf()
