"""Adiciona slides de BM25 e Data Augmentation na apresentação oficial PPTX."""
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PPTX_PATH = os.path.join(BASE_DIR, "docs", "APRESENTACAO_DEFESA_A3.pptx")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

prs = pptx.Presentation(PPTX_PATH)
blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category="PROJETO INTEGRADOR A3 • INTELIGÊNCIA ARTIFICIAL"):
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.4))
    tf_cat = tb_cat.text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(37, 99, 235)

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(8.4), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(15, 23, 42)

# Slide 18: BM25 vs TF-IDF
s18 = prs.slides.add_slide(blank_layout)
add_header(s18, "17. Teoria da Recuperação da Informação: Okapi BM25 vs TF-IDF")
tb_s18 = s18.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8.4), Inches(1.0))
tf_s18 = tb_s18.text_frame
p1 = tf_s18.paragraphs[0]
p1.text = "• Métricas de IR: P@1 de 90.0%, P@3 de 95.0% e Mean Reciprocal Rank (MRR) de 0.927 em suporte N1."
p1.font.size = Pt(11)
p1.font.color.rgb = RGBColor(51, 65, 85)
p2 = tf_s18.add_paragraph()
p2.text = "• Vantagem Estrutural: Saturação assintótica de termos (k1=1.5) e penalização de documentos longos (b=0.75)."
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(51, 65, 85)

img_bm25 = os.path.join(RESULTS_DIR, "grafico_benchmark_bm25_vs_tfidf.png")
if os.path.exists(img_bm25):
    s18.shapes.add_picture(img_bm25, Inches(1.5), Inches(2.4), width=Inches(6.8))

# Slide 19: Data Augmentation EDA & Active Learning (RLHF)
s19 = prs.slides.add_slide(blank_layout)
add_header(s19, "18. Data Augmentation Sintético EDA & Aprendizado Ativo (RLHF)")
tb_s19 = s19.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8.4), Inches(1.0))
tf_s19 = tb_s19.text_frame
p1 = tf_s19.paragraphs[0]
p1.text = "• Expansão Sintética EDA: Corpus ampliado de 110 para 247 frases (+20.5% em 5-Fold CV: de 75.45% para 95.94%)."
p1.font.size = Pt(11)
p1.font.color.rgb = RGBColor(51, 65, 85)
p2 = tf_s19.add_paragraph()
p2.text = "• Human-in-the-Loop: Curadoria de predições ambíguas e retreinamento a quente via API em <10 ms."
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(51, 65, 85)

img_eda = os.path.join(RESULTS_DIR, "grafico_impacto_data_augmentation.png")
if os.path.exists(img_eda):
    s19.shapes.add_picture(img_eda, Inches(1.5), Inches(2.4), width=Inches(6.8))

prs.save(PPTX_PATH)
print(f"[OK] Slides 18 e 19 adicionados com sucesso em {PPTX_PATH}! Total de slides: {len(prs.slides)}")
