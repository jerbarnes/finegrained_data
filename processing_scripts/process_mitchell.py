import json
import os


def get_opinions(conll_file):

    preprocessed = []

    sent = []
    opinions = []

    target_tokens = []
    polarity = ""
    in_target = False

    for line in open(conll_file):
        if line.startswith("##"):
            idx = line.split()[-1]
        elif line.strip() == "":
            if len(target_tokens) > 0:
                in_target = False
                target_exp = " ".join(target_tokens)
                s = " ".join(sent)
                off1 = s.find(target_exp)
                off2 = off1 + len(target_exp)
                target = [target_exp, "{0}:{1}".format(off1, off2)]

                opinion = {"holder": None,
                           "target": target,
                           "expression": None,
                           "label": polarity,
                           "intensity": "normal"}
                opinions.append(opinion)

                target_tokens = []
                polarity = ""
            new = {

            }
            new["sent_id"] = idx
            new["text"] = " ".join(sent)
            new["opinions"] = opinions

            preprocessed.append(new)
            sent = []
            opinions = []
        else:
            try:
                token, ner, pol = line.strip().split("\t")
                sent.append(token)
            except:
                print(line)
                print(conll_file)


            if "B" in ner and pol != "_" and in_target == False:
                in_target = True
                target_tokens.append(token)
                polarity = pol
            elif "I" in ner and in_target == True:
                target_tokens.append(token)
            elif (ner == "O" and in_target == True) or ("B" in ner and in_target == True):
                in_target = False
                target_exp = " ".join(target_tokens)
                s = " ".join(sent)
                off1 = s.find(target_exp)
                off2 = off1 + len(target_exp)
                target = [target_exp, "{0}:{1}".format(off1, off2)]

                opinion = {"holder": None,
                           "target": target,
                           "expression": None,
                           "label": polarity,
                           "intensity": "normal"}
                opinions.append(opinion)

                target_tokens = []
                polarity = ""

    return preprocessed

if __name__ == "__main__":

    trainfile = "/home/jeremy/Exps/finegrained_data/mitchell/en/10-fold/train.1"
    testfile = "/home/jeremy/Exps/finegrained_data/mitchell/en/10-fold/test.1"

    train = get_opinions(trainfile)
    dev_idx = int(len(train) * .1)
    dev = train[:dev_idx]
    train = train[dev_idx:]
    test = get_opinions(testfile)

    os.makedirs(os.path.join("../processed", "twitter_targeted"), exist_ok=True)
    with open(os.path.join("../processed", "twitter_targeted", "train.json"), "w") as out:
            json.dump(train, out)
    with open(os.path.join("../processed", "twitter_targeted", "dev.json"), "w") as out:
            json.dump(dev, out)
    with open(os.path.join("../processed", "twitter_targeted", "test.json"), "w") as out:
            json.dump(test, out)
