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

    #read chunk line by line
    #we focus author and title
    for event, elem in context:

        if elem.tag == 'year':
            year = int(unidecode(elem.text))

        if elem.tag in ['journal', 'booktitle']:
            if elem.text:
                conf_name = unidecode(elem.text)

        if elem.tag in [u'proceedings', u'article'] and len(conf_name) > 0:
            if year not in data:
                data[year] = Set()
            
            data[year].add(conf_name)
            print("%d,%s"%(year, conf_name))

            year = 0
            conf_name = ''
 
        elem.clear()
        while elem.getprevious() is not None and elem.getparent() is not None:
            del elem.getparent()[0]
    del context
    
    for year in data:
        for conf_name in data[year]:
            fout.write('%d,%s\n'%(year, conf_name))



if __name__ == "__main__":
    fout = open('conference_by_year.csv', 'w')
    context = etree.iterparse('../../data/small.xml', load_dtd=True,html=True)
    #To use iterparse, we don't need to read all of xml.
    conferences_by_year(context, fout)
    fout.close()
