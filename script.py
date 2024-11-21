#!/usr/bin/env python3
import os
from lxml import etree

def transform_xml_to_html(xml_file, xslt_file, output_dir):
    try:
        # Llegeix l'XML complet
        with open(xml_file, 'r', encoding='utf-8') as xml_f:
            xml_tree = etree.parse(xml_f)
        
        # Llegeix el XSLT
        with open(xslt_file, 'r', encoding='utf-8') as xslt_f:
            xslt_tree = etree.parse(xslt_f)
        
        # Aplica la transformació XSLT
        transform = etree.XSLT(xslt_tree)
        
        # Troba totes les receptes
        receptes = xml_tree.findall("recepta")
        
        if not receptes:
            print("No s'han trobat receptes a l'arxiu XML.")
            return
        
        # Processa cada recepta
        for recepta in receptes:
            # Crea un nou arbre XML per incloure només aquesta recepta
            root = etree.Element("receptes")
            root.append(recepta)  # Afegim la recepta actual com a node fill
            recepta_tree = etree.ElementTree(root)
            
            # Aplica la transformació XSLT
            html_tree = transform(recepta_tree)
            
            # Obté el títol de la recepta per al nom del fitxer
            recepta_title = recepta.findtext("titol", "recepta").strip().replace(" ", "_")
            output_file = os.path.join(output_dir, f"{recepta_title}.html")
            
            # Escriu l'HTML generat al fitxer de sortida
            with open(output_file, 'w', encoding='utf-8') as html_f:
                html_f.write(str(html_tree))
            
            print(f"HTML creat: {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

# Configuració
xml_file_path = "recetas.xml"  # Canvia la ruta pel teu XML
xslt_file_path = "recetasXSLT.xml"  # Canvia la ruta pel teu XSLT
output_directory = "./nuevas_recetas"  # Directori on es guardaran els HTML generats

# Crea el directori de sortida si no existeix
os.makedirs(output_directory, exist_ok=True)

# Executa la transformació
transform_xml_to_html(xml_file_path, xslt_file_path, output_directory)
