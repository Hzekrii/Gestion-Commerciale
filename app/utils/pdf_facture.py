from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generer_pdf_facture(facture, lignes):
    c = canvas.Canvas(f"facture_{facture.id}.pdf", pagesize=A4)
    c.drawString(50, 800, f"Facture n° {facture.id}")
    c.drawString(50, 780, f"Total TTC : {facture.total_ttc} DH")
    c.save()