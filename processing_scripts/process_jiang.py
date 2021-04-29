from lxml import etree
from lxml.etree import fromstring
import os
import json

parser = etree.XMLParser(recover=True, encoding='utf8')

def get_opinions(markable_file):

    preprocessed = []

    xml = open(markable_file).read().encode('utf8')
    root = fromstring(xml, parser)

    for i, sent in enumerate(root):
        new = {}
        new["sent_id"] = i

        text, aspect_terms = sent.getchildren()
        new["text"] = text.text

        opinions = []
        for aspect in aspect_terms.getchildren():
            off1 = aspect.get("from")
            off2 = aspect.get("to")
            target_tokens = aspect.get("term")
            target = [target_tokens, "{0}:{1}".format(off1, off2)]
            label = aspect.get("polarity")


            opinions.append({"holder": None,
                             "target": target,
                             "expression": None,
                             "label": label,
                             "intensity": "normal"})
        new["opinions"] = opinions

        preprocessed.append(new)
    return preprocessed

if __name__ == "__main__":

    corpora = [("train", "../jiang-et-al/data/MAMS-ATSA/raw/train.xml"),
               ("dev", "../jiang-et-al/data/MAMS-ATSA/raw/val.xml"),
               ("test", "../jiang-et-al/data/MAMS-ATSA/raw/test.xml"),
               ]
    os.makedirs(os.path.join("../processed", "MAMS"), exist_ok=True)

    for name, corpus in corpora:
        processed = get_opinions(corpus)

        with open(os.path.join("../processed", "MAMS", "{0}.json".format(name)), "w") as out:
            json.dump(processed, out)
