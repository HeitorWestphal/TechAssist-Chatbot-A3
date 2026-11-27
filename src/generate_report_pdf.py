"""Gera a versão PDF e DOCX do Relatório Técnico da A3 com todas as 14 figuras científicas."""
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from src.update_full_reports import generate_docx, generate_pdf

def build_pdf():
    generate_docx()
    generate_pdf()

if __name__ == "__main__":
    build_pdf()
