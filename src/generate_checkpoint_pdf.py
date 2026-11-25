"""Gera a versão PDF oficial do Checkpoint Técnico da A3 a partir dos dados do DOCX."""
import docx
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    doc_docx = docx.Document("Atividade_Checkpoint_Preenchida.docx")
    pdf_filename = "Atividade_Checkpoint_Preenchida.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        alignment=1
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b')
    )
    cell_style = ParagraphStyle(
        'Cell',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0f172a')
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold'
    )

    story = []

    story.append(Paragraph("CHECKPOINT TÉCNICO — PROJETO A3", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Inteligência Artificial | Desenvolvimento de Chatbots | TechAssist AI Solutions", subtitle_style))
    story.append(Spacer(1, 10))

    # Identificação da Equipe
    ident_data = [
        [Paragraph("<b>Equipe:</b> TechAssist AI Solutions", body_style), Paragraph("<b>Chatbot:</b> TechAssist AI (Helpdesk TI N1)", body_style)],
        [Paragraph("<b>Integrantes:</b><br/>• Heitor Della Barba Westphal (RA: 1072410915)<br/>• Bruno Hudson Siebert Costa (RA: 1072419878)<br/>• Ian Santiago Silveira (RA: 1072410937)<br/>• João Víctor Muniz da Silva (RA: 1072413992)", body_style),
         Paragraph("<b>Repositório GitHub:</b><br/>https://github.com/HeitorWestphal/TechAssist-Chatbot-A3<br/><br/><b>Status:</b> 100% Concluído (10/10 itens 'C')", body_style)]
    ]
    t_ident = Table(ident_data, colWidths=[260, 260])
    t_ident.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ident)
    story.append(Spacer(1, 10))

    # Diagnóstico dos 10 itens
    story.append(Paragraph("1. Diagnóstico de Progresso da Equipe (10 Itens)", h2_style))
    t1 = doc_docx.tables[1]
    t1_data = []
    for r_idx, r in enumerate(t1.rows):
        row_cells = []
        for c in r.cells:
            st = cell_bold if r_idx == 0 else cell_style
            row_cells.append(Paragraph(c.text.replace("\n", " "), st))
        t1_data.append(row_cells)
    
    table_diag = Table(t1_data, colWidths=[120, 28, 70, 302])
    table_diag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(table_diag)
    story.append(Spacer(1, 10))

    # Desafios Práticos A-E
    story.append(Paragraph("2. Resolução dos Desafios Práticos de PLN (A até E)", h2_style))
    t2 = doc_docx.tables[2]
    t2_data = []
    for r_idx, r in enumerate(t2.rows):
        row_cells = []
        for c in r.cells:
            st = cell_bold if r_idx == 0 else cell_style
            row_cells.append(Paragraph(c.text.replace("\n", " "), st))
        t2_data.append(row_cells)
    
    table_desafios = Table(t2_data, colWidths=[100, 150, 120, 150])
    table_desafios.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(table_desafios)
    story.append(Spacer(1, 10))

    # Contribuições Individuais
    story.append(Paragraph("3. Contribuições Individuais e Evidências Técnicas", h2_style))
    t3 = doc_docx.tables[3]
    t3_data = []
    for r_idx, r in enumerate(t3.rows):
        row_cells = []
        for c in r.cells:
            st = cell_bold if r_idx == 0 else cell_style
            row_cells.append(Paragraph(c.text.replace("\n", " "), st))
        t3_data.append(row_cells)

    table_contrib = Table(t3_data, colWidths=[130, 240, 150])
    table_contrib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(table_contrib)
    story.append(Spacer(1, 10))

    # Plano de Ação
    story.append(Paragraph("4. Plano de Ação para a Entrega Final", h2_style))
    t4 = doc_docx.tables[4]
    t4_data = []
    for r_idx, r in enumerate(t4.rows):
        row_cells = []
        for c in r.cells:
            st = cell_bold if r_idx == 0 else cell_style
            row_cells.append(Paragraph(c.text.replace("\n", " "), st))
        t4_data.append(row_cells)

    table_plano = Table(t4_data, colWidths=[180, 140, 200])
    table_plano.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(table_plano)

    doc.build(story)
    print(f"[OK] Gerado {pdf_filename} com sucesso!")

if __name__ == "__main__":
    generate_pdf()
