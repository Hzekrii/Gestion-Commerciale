from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def generer_facture_pdf(facture, client, lignes):
    filename = f"facture_{facture.id}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    y = 28 * cm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, y, "FACTURE")
    y -= 1*cm

    c.setFont("Helvetica", 10)
    c.drawString(2*cm, y, f"Facture N° : {facture.id}")
    y -= 0.5*cm
    c.drawString(2*cm, y, f"Client : {client.nom}")
    y -= 1*cm

    # Tableau
    c.drawString(2*cm, y, "Article")
    c.drawString(10*cm, y, "Qté")
    c.drawString(12*cm, y, "PU")
    c.drawString(15*cm, y, "Total")
    y -= 0.5*cm

    for l in lignes:
        c.drawString(2*cm, y, str(l.article_id))
        c.drawString(10*cm, y, str(l.quantite))
        c.drawString(12*cm, y, str(l.prix_unitaire))
        c.drawString(15*cm, y, str(l.total_ligne))
        y -= 0.4*cm

    y -= 1*cm
    c.drawString(12*cm, y, f"Total HT : {facture.total_ht}")
    y -= 0.4*cm
    c.drawString(12*cm, y, f"TVA : {facture.total_tva}")
    y -= 0.4*cm
    c.drawString(12*cm, y, f"Total TTC : {facture.total_ttc}")

    c.save()
    return filename