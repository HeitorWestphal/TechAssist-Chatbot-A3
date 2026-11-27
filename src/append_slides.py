"""Adiciona slides científicos de alto impacto à apresentação PowerPoint."""
import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PPTX_PATH = os.path.join(BASE_DIR, "docs", "APRESENTACAO_DEFESA_A3.pptx")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

prs = pptx.Presentation(PPTX_PATH)
blank_layout = prs.slide_layouts[6] # layout em branco

def add_header(slide, title_text, category="PROJETO INTEGRADOR A3 • INTELIGÊNCIA ARTIFICIAL"):
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.4))
    tf_cat = tb_cat.text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(37, 99, 235) # Blue-600

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(8.4), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(15, 23, 42) # Slate-900

# Slide 14: Estudo de Ablação e Eficiência Amostral
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "13. Estudo Científico de Ablação e Eficiência Amostral")
tb_s14 = s14.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8.4), Inches(1.0))
tf_s14 = tb_s14.text_frame
p1 = tf_s14.paragraphs[0]
p1.text = "• Decomposição em 6 estágios: Normalização NFKD + Stopwords eleva a acurácia de 84% para 96% (+12%)."
p1.font.size = Pt(11)
p1.font.color.rgb = RGBColor(51, 65, 85)
p2 = tf_s14.add_paragraph()
p2.text = "• Curva de Aprendizado: Saturação e estabilidade atingidas a partir de 60 amostras sob 5-Fold CV."
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(51, 65, 85)

img_abl = os.path.join(RESULTS_DIR, "grafico_estudo_ablacao.png")
if os.path.exists(img_abl):
    s14.shapes.add_picture(img_abl, Inches(0.8), Inches(2.4), width=Inches(4.0))

img_lrn = os.path.join(RESULTS_DIR, "grafico_curva_aprendizado.png")
if os.path.exists(img_lrn):
    s14.shapes.add_picture(img_lrn, Inches(5.1), Inches(2.4), width=Inches(4.0))

# Slide 15: Significância Estatística de McNemar e ECE
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "14. Teste de Significância de McNemar e Calibração (ECE)")
tb_s15 = s15.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8.4), Inches(1.0))
tf_s15 = tb_s15.text_frame
p1 = tf_s15.paragraphs[0]
p1.text = "• Teste de McNemar (N=60 Casos de Estresse): chi^2 = 9.3333, p = 0.0023 (< 0.01) — Rejeita H0 com 99% de certeza!"
p1.font.size = Pt(11)
p1.font.bold = True
p1.font.color.rgb = RGBColor(30, 64, 175)
p2 = tf_s15.add_paragraph()
p2.text = "• Confiabilidade Probabilística: Expected Calibration Error (ECE) de 0.260 e Brier Score de 0.223."
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(51, 65, 85)

img_mcn = os.path.join(RESULTS_DIR, "grafico_significancia_estatistica_mcnemar.png")
if os.path.exists(img_mcn):
    s15.shapes.add_picture(img_mcn, Inches(0.8), Inches(2.4), width=Inches(4.0))

img_ece = os.path.join(RESULTS_DIR, "grafico_curva_calibracao_ece.png")
if os.path.exists(img_ece):
    s15.shapes.add_picture(img_ece, Inches(5.1), Inches(2.4), width=Inches(4.0))

# Slide 16: Robustez sob Ruído Adversarial e Análise de ROI vs LLMs
s16 = prs.slides.add_slide(blank_layout)
add_header(s16, "15. Robustez Adversarial a Typos e Análise de ROI Corporativo")
tb_s16 = s16.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8.4), Inches(1.0))
tf_s16 = tb_s16.text_frame
p1 = tf_s16.paragraphs[0]
p1.text = "• Tolerância a Erros: Levenshtein confere vantagem de +20% em acurácia sob 20% de ruído textual severo."
p1.font.size = Pt(11)
p1.font.color.rgb = RGBColor(51, 65, 85)
p2 = tf_s16.add_paragraph()
p2.text = "• Eficiência Operacional: TechAssist consome 14.8 MB RAM e 0.48 ms (1.700x mais veloz e R$ 0 de custo em API)."
p2.font.size = Pt(11)
p2.font.color.rgb = RGBColor(51, 65, 85)

img_rob = os.path.join(RESULTS_DIR, "grafico_robustez_adversarial_ruido.png")
if os.path.exists(img_rob):
    s16.shapes.add_picture(img_rob, Inches(0.8), Inches(2.4), width=Inches(4.0))

img_roi = os.path.join(RESULTS_DIR, "grafico_comparativo_recursos_roi.png")
if os.path.exists(img_roi):
    s16.shapes.add_picture(img_roi, Inches(5.1), Inches(2.4), width=Inches(4.0))

# Slide 17: Disponibilização como Skill Autônoma para Agentes de IA
s17 = prs.slides.add_slide(blank_layout)
add_header(s17, "16. Integração Corporativa: Skill para Agentes e MCP Server")
tb_s17 = s17.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(8.4), Inches(5.0))
tf_s17 = tb_s17.text_frame

p_itens = [
    ("Model Context Protocol (MCP JSON-RPC 2.0)", "Servidor stdio pronto para Claude Code, Cursor, Codex e Antigravity com 5 ferramentas exportadas."),
    ("Marketplace Agensi.io", "Manifesto agensi.json pronto para publicação e distribuição como Skill autônoma de helpdesk corporativo."),
    ("Governança e Proteção LGPD", "Módulo security_guardrails com mascaramento automático de CPF, cartões e bloqueio de SQLi/Jailbreaks."),
    ("Observabilidade e Monitoramento", "Exportador Prometheus em /metrics e health check corporativo em /health com Docker containerization.")
]

for title, desc in p_itens:
    p_t = tf_s17.add_paragraph()
    p_t.text = f"• {title}:"
    p_t.font.bold = True
    p_t.font.size = Pt(12)
    p_t.font.color.rgb = RGBColor(30, 64, 175)
    
    p_d = tf_s17.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = RGBColor(71, 85, 105)

prs.save(PPTX_PATH)
print(f"[OK] Slides adicionados com sucesso em {PPTX_PATH}!")
