from lxml import etree
from lxml.etree import fromstring
import os
import json
import re
import argparse

from nltk.tokenize import WhitespaceTokenizer

eparser = etree.XMLParser(recover=True, encoding='utf8')

def get_sent_num(opinion_expression, sents):
    for subelement in opinion_expression:
        if subelement.tag == "span":
            for token in subelement:
                tidx = token.get("id")
                idx = "w" + tidx[1:]
                return sents[idx]

def get_token_offsets(sents2tokens, tokens):
    tokenizer = WhitespaceTokenizer()
    idx_example = list(tokens.keys())[0]
    token_offsets = {}
    i = 1
    for sent_idx, text in sents2tokens.items():
        offsets = list(tokenizer.span_tokenize(text))
        for tok in offsets:
            if "_" in idx_example:
                wid = "w_{0}".format(i)
            else:
                wid = "w{0}".format(i)
            i += 1
            token_offsets[wid] = tok
    return token_offsets

def get_sent_tokens(sents, tokens):
    flipped = {}
    for x, i in sents.items():
        if i in flipped:
            tok = tokens[x]
            flipped[i].append(tok)
        else:
            tok = tokens[x]
            flipped[i] = [tok]
    final = {}
    for sent_idx, toks in flipped.items():
        final[sent_idx] = " ".join(toks)
    return final

def get_polar_expression(opinion_expression, tokens, token_offsets):
    texts = ""
    offsets = []
    intensity = "Standard"
    polarity = "Neutral"
    for subelement in opinion_expression:
        if subelement.tag == "span":
            for token in subelement:
                idx = "w" + token.get("id")[1:]
                text = tokens[idx]
                bidx, eidx = token_offsets[idx]
                texts += text + " "
                offsets.append((bidx, eidx))
    new_bidx = sorted(offsets)[0][0]
    new_eidx = sorted(offsets)[-1][-1]
    offset = "{0}:{1}".format(new_bidx, new_eidx)
    texts = texts.strip()
    #
    label = opinion_expression.get("polarity")
    if "Strong" in label:
        intensity = "Strong"
    if "Positive" in label:
        polarity = "Positive"
    if "Negative" in label:
        polarity = "Negative"
    return [[texts], [offset]], polarity, intensity

def get_target_holder(opinion_target, tokens, token_offsets):
    texts = ""
    offsets = []
    for subelement in opinion_target:
        if subelement.tag == "span":
            for token in subelement:
                idx = "w" + token.get("id")[1:]
                text = tokens[idx]
                bidx, eidx = token_offsets[idx]
                texts += text + " "
                offsets.append((bidx, eidx))
    if len(offsets) > 0:
        new_bidx = sorted(offsets)[0][0]
        new_eidx = sorted(offsets)[-1][-1]
        offset = "{0}:{1}".format(new_bidx, new_eidx)
        texts = texts.strip()
        return [[texts], [offset]]
    else:
        return [[], []]

def get_opinions(xml_file):
    all_opinions = []
    #
    mark_xml = open(xml_file).read().encode('utf8')
    base_root = fromstring(mark_xml, eparser)
    #
    tokens = {}
    sents = {}
    opinions = {}
    for annotation in base_root:
        if annotation.tag == "text":
            for token in annotation:
                token_idx = token.get("id")
                if token_idx == None:
                    token_idx = token.get("wid")
                tok = token.text
                sent = token.get("sent")
                tokens[token_idx] = tok
                sents[token_idx] = sent
            sentidx_to_tokens = get_sent_tokens(sents, tokens)
            token_offsets = get_token_offsets(sentidx_to_tokens, tokens)
            #
            for sentidx in sentidx_to_tokens.keys():
                full_sent_idx  = xml_file[:-4] + "-" + str(sentidx)
                text = sentidx_to_tokens[sentidx]
                opinions[sentidx] = {"sent_id": full_sent_idx,
                                     "text": text,
                                     "opinions": []
                                     }
        #
        if annotation.tag == "opinions":
            for opinion_ann in annotation:
                opinion = {"Source": [[], []],
                           "Target": [[], []],
                           "Polar_expression": [[], []],
                           "Polarity": "",
                           "Intensity": ""
                           }
                for element in opinion_ann:
                    if element.tag == "opinion_expression":
                        sent_num = get_sent_num(element, sents)
                        pol_exp, polarity, intensity = get_polar_expression(element, tokens, token_offsets)
                        text = sentidx_to_tokens[sent_num]
                        #
                        opinion["Polar_expression"] = pol_exp
                        opinion["Polarity"] = polarity
                        opinion["Intensity"] = intensity
                    if element.tag == "opinion_holder":
                        source = get_target_holder(element, tokens, token_offsets)
                        opinion["Source"] = source
                    if element.tag == "opinion_target":
                        target = get_target_holder(element, tokens, token_offsets)
                        opinion["Target"] = target
                opinions[sent_num]["opinions"].append(opinion)
    return list(opinions.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir")
    parser.add_argument("--outdir")
    parser.add_argument("--datasplit")

    args = parser.parse_args()

    with open(args.datasplit) as infile:
        datasplit = json.load(infile)

    train, dev, test = [], [], []

    for file in os.listdir(args.indir):
        opinions = get_opinions(os.path.join(args.indir, file))
        for opinion in opinions:
            if os.path.basename(opinion["sent_id"]) in datasplit["train"]:
                train.append(opinion)
            elif os.path.basename(opinion["sent_id"]) in datasplit["dev"]:
                dev.append(opinion)
            elif os.path.basename(opinion["sent_id"]) in datasplit["test"]:
                test.append(opinion)
            else:
                print("{} not found in splits!!!!".format(opinions["sent_id"]))


    for name, data in [("train.json", train),
                       ("dev.json", dev),
                       ("test.json", test)]:
        with open(os.path.join(args.outdir, name), "w") as outfile:
            json.dump(data, outfile)
