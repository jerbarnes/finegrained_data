from lxml import etree
from lxml.etree import fromstring
import os
import json

parser = etree.XMLParser(recover=True, encoding='utf8')

def process(file):
    xml = open(file).read().encode('utf8')
    root = fromstring(xml, parser)

    processed = []

    for sent in root:
        new = {}
        new["sent_id"] = sent.get("id")
        new["opinions"] = []
        for info in sent:
            if info.tag == "text":
                new["text"] = info.text
            elif info.tag == "aspectTerms":
                for aspect in info:
                    target = aspect.get("term")
                    label = aspect.get("polarity")
                    bidx = aspect.get("from")
                    eidx = aspect.get("to")
                    new["opinions"].append({
                                            "holder": None,
                                            "target": [target, "{0}:{1}".format(bidx, eidx)],
                                            "expression": None,
                                            "label": label,
                                            "intensity": "normal"
                                    })
        processed.append(new)
    return processed


if __name__ == "__main__":

    for name, data in [("laptops_train",
                        "../SemEval/data/official_data/SemEval-2014/Laptops_Train.xml"),
                        ("laptops_test",
                         "../SemEval/data/official_data/SemEval-2014/ABSA_Gold_TestData/Laptops_Test_Gold.xml"),
                        ("restaurants_train",
                        "../SemEval/data/official_data/SemEval-2014/Restaurants_Train.xml"),
                        ("restaurants_test",
                         "../SemEval/data/official_data/SemEval-2014/ABSA_Gold_TestData/Restaurants_Test_Gold.xml")
                       ]:

        os.makedirs(os.path.join("../processed", "semeval_restaurant"), exist_ok=True)
        os.makedirs(os.path.join("../processed", "semeval_laptop"), exist_ok=True)

        p = process(data)
        if "train" in name:
            dev_idx = int(len(p) * .1)
            dev = p[:dev_idx]
            train = p[dev_idx:]
            if "laptop" in name:
                with open(os.path.join("../processed", "semeval_laptop", "train.json"), "w") as out:
                    json.dump(train, out)
                with open(os.path.join("../processed", "semeval_laptop", "dev.json"), "w") as out:
                    json.dump(dev, out)
            if "restaurant" in name:
                with open(os.path.join("../processed", "semeval_restaurant", "train.json"), "w") as out:
                    json.dump(train, out)
                with open(os.path.join("../processed", "semeval_restaurant", "dev.json"), "w") as out:
                    json.dump(dev, out)
        else:
            if "laptop" in name:
                with open(os.path.join("../processed", "semeval_laptop", "test.json"), "w") as out:
                    json.dump(p, out)
            if "restaurant" in name:
                with open(os.path.join("../processed", "semeval_restaurant", "test.json"), "w") as out:
                    json.dump(p, out)
