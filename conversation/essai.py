
from .utils import resumer_texte

texte = """
Ce marketplace permet aux utilisateurs de consulter les produits en vente, 
de contacter les propriétaires pour discuter de la situation du produit, 
et de poser des questions avant l’achat.
"""

resume = resumer_texte(texte)
print("Résumé :", resume)
