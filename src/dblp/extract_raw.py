from lxml import etree
import os, sys
from unidecode import unidecode

def extract_types(fin, fout, types):
    fout = open(fout, 'w')
    parser = etree.XMLParser(load_dtd=True)
    tree = etree.parse(fin, parser)

    fout.write('''<?xml version="1.0" encoding="ISO-8859-1"?>\n''' +
               '''<!DOCTYPE dblp SYSTEM "dblp.dtd">\n''' +
               '''<dblp>\n''');
    for item in tree.getroot():
        if item.tag in types:
            fout.write("%s\n"%(etree.tostring(item, pretty_print=True)));

    fout.write('''</dblp>\n''');
    fout.close()


if __name__=="__main__":
    types = ['inproceedings', 'article']
    fin = "../../data/dblp.xml"
    fout = "../../data/" + '_'.join(types) + '.xml'
    extract_types(fin, fout, types)
