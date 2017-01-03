from lxml import etree, objectify
from sets import Set

class DBLP:
    pass

class Parser:

    def fromfile(self, filename):
        f = open(filename, "r")
        tree = ET.parse(filename)
        root = tree.getroot()


def show_tag_formats(xmlfile, dtdfile):
    dtd = etree.DTD(open(dtdfile, 'r'))
    tree = objectify.parse(open(xmlfile, 'r'))
    print dtd.validate(tree)
    root = tree.getroot()

    tags = Set()
    for child in root:
        if child.tag not in tags:
            tags.add(child.tag)
            etree.tostring(child, pretty_print=True)

if __name__=="__main__":
    show_tag_formats("../../data/dblp.xml", "../../data/dblp.dtd")

