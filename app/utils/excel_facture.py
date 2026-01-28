import pandas as pd

def exporter_facture_excel(facture, client, lignes):
    data = []
    for l in lignes:
        data.append({
            "Article": l.article_id,
            "Quantité": l.quantite,
            "Prix unitaire": l.prix_unitaire,
            "Total": l.total_ligne
        })

    df = pd.DataFrame(data)

    filename = f"facture_{facture.id}.xlsx"
    df.to_excel(filename, index=False)

    return filename