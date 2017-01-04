# -*- coding: utf-8 -*-
from lxml import etree
import os, sys
from unidecode import unidecode
from sets import Set


def conferences_by_year(context, fout):
    #xml categories
    author_array = []
    title = ''
    conf_name = ''
    year = 0
    data = {}
    cnt = 0

    for event, elem in context:

        if elem.tag == 'year':
            year = int(unidecode(elem.text))

        if elem.tag in ['journal', 'booktitle']:
            if elem.text:
                conf_name = unidecode(elem.text)

        if elem.tag in ['inproceedings', 'proceedings', 'article'] and len(conf_name) > 0:
            cnt += 1
            if cnt % 10000 == 0:
                print(cnt)
            if year not in data:
                data[year] = Set()
            
            data[year].add(conf_name)

            year = 0
            conf_name = ''
 
        elem.clear()
        while elem.getprevious() is not None and elem.getparent() is not None:
                del elem.getparent()[0]
    del context
    
    for year in data:
        for conf_name in data[year]:
            fout.write('%d,%s\n'%(year, conf_name))


def conferences_by_year(fin, fout):
    fout = open(fout, 'w')
    parser = etree.XMLParser(load_dtd=True)
    tree = etree.parse(fin, parser)

    data = {}
    year = 0
    cnt = 0
    name = ''
    for item in tree.getroot():
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt)
        for field in item:
            if field.tag == "year":
                year = int(field.text)
            if field.tag in ['journal', 'booktitle']:
                name = unidecode(field.text).replace(",", "")

        if year not in data:
            data[year] = Set()
            
        data[year].add(name)
        year = 0
        name = ''

    for year in data:
        for name in data[year]:
            fout.write('%d,%s\n'%(year, name))


if __name__=="__main__":
    fin = "../../data/inproceedings_proceedings_article.xml"
    fout = "../../data/conference_by_year.csv"
    conferences_by_year(fin, fout)


"""
if __name__ == "__main__":
    fout = open('conference_by_year.csv', 'w')
    context = etree.iterparse('../../data/small.xml', load_dtd=True,html=True)
    #To use iterparse, we don't need to read all of xml.
    conferences_by_year(context, fout)
    fout.close()
"""
