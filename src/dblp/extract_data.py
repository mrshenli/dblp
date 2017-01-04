# -*- coding: utf-8 -*-
from lxml import etree
import os, sys
from unidecode import unidecode
import itertools
from sets import Set
import re
import copy
import pickle

def get_time(year, name, vol, num, map):
    return year * 100

def get_area(name, ref):
    return 0

def to_string_dict(data_map):
    for key in data_map:
        sorted_values = sorted(data_map[key])
        cnt = 0
        data_map[key] = {}
        for value in sorted_values:
            data_map[key][value] = cnt
            cnt += 1

def user_community(fin, user_out, comm_out, author_out):
    user_out = open(user_out, 'w')
    comm_out = open(comm_out, 'w')
    parser = etree.XMLParser(load_dtd=True)
    tree = etree.parse(fin, parser)

    journal_map = {}
    author_map = {}
    vol_map = {}
    num_map = {}
    year = 0
    cnt = 0
    name = ''
    ref = ''
    authors = []
    vol = -1
    num = -1
    data = []
    for item in tree.getroot():
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt)

        if "publtype" in item.attrib and item.attrib["publtype"] == "edited publication":
            continue;

        for field in item:
            if field.tag == "year":
                year = int(field.text)
            elif field.tag == "author":
                author = unidecode(field.text)
                if author not in author_map:
                    author_map[author] = len(author_map)
                authors.append(author_map[author])
            elif field.tag in ['journal', 'booktitle']:
                name = unidecode(field.text)
            elif field.tag == "volume":
                vol = field.text
            elif field.tag == "crossref":
                ref = field.text
            elif field.tag == "number":
                num = field.text

        if vol >= 0 and num >= 0:
            # journal
            if year not in journal_map:
                journal_map[year] = {}
            if name not in journal_map[year]:
                journal_map[year][name] = Set()
            journal_map[year][name].add((vol, num))

        key = (year, name)

        if key not in vol_map:
            vol_map[key] = Set()
        if key not in num_map:
            num_map[key] = Set()

        vol_map[key].add(vol)
        num_map[key].add(num)

        data.append((year, vol, num, name, ref, copy.deepcopy(authors)))

        year = 0
        name = ''
        ref = ''
        num = -1
        vol = -1
        del authors[:]

    to_string_dict(vol_map)
    to_string_dict(num_map)

    with open(author_out, 'wb') as handle:
        pickle.dump(author_map, handle, protocol=pickle.HIGHEST_PROTOCOL)
    author_map.clear()


    data = sorted(data)
    user_comm = {}

    cnt = 0
    for item in data:
        cnt += 1
        if cnt % 10000 == 0:
            print ("+ cnt")
        (year, vol, num, name, ref, authors) = item
        vol = vol_map[(year, name)][vol]
        num = num_map[(year, name)][num]
        area = get_area(name, ref)
        time = get_time(year, name, vol, num, {})

        for pair in itertools.combinations(authors, 2):
            (a, b) = pair
            user_out.write("%d,%s,%s\n"%(time, a, b))

        for author in authors:
            if author not in user_comm:
                user_comm[author] = [0 for x in range(15)]

            user_comm[author][area] += 1
            comm_out.write("%d,%s,%s\n"%(time, author, ",".join(str(x) for x in user_comm[author])))


    user_out.close()
    comm_out.close()


if __name__ == "__main__":
    user_out = '../../data/user_link.csv'
    comm_out = '../../data/comm_truth.csv'
    author_out = '../../data/author_map.pickle'
    fin = '../../data/inproceedings_article.xml'
    #To use iterparse, we don't need to read all of xml.
    user_community(fin, user_out, comm_out, author_out)
