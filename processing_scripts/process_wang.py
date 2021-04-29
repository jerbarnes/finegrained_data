import json
import os

def get_opinions(tweet_json, anns_json):
    tweet = json.load(open(tweet_json))
    anns = json.load(open(anns_json))


    idx = tweet_json[:-5].rsplit("/")[-1]
    new = {}
    new["sent_id"] = idx
    new["text"] = tweet["content"]

    opinions = []

    for entity in tweet["entities"]:
        target_toks = entity["entity"]
        off1 = entity["offset"]
        off2 = off1 + len(target_toks)
        target = [target_toks, "{0}:{1}".format(off1, off2)]

        ent_idx = str(entity["id"])
        polarity = anns["items"][ent_idx]

        opinion = {"holder": None,
                   "target": target,
                   "expression": None,
                   "label": polarity,
                   "intensity": "normal"}

        opinions.append(opinion)

    new["opinions"] = opinions
    return new

if __name__ == "__main__":



    train_idxs = [l.strip() for l in open("../wangetal/train_id.txt")]
    test_idxs = [l.strip() for l in open("../wangetal/test_id.txt")]

    os.makedirs(os.path.join("../processed", "tdparse"), exist_ok=True)

    for name, corpus in [("train", train_idxs), ("test", test_idxs)]:
        processed = []

        for fname in corpus:
            tweet_file = os.path.join("../wangetal/tweets", "5{0}.json".format(fname))
            ann_file = os.path.join("../wangetal/annotations", "5{0}.json".format(fname))
            processed.append(get_opinions(tweet_file, ann_file))

        if name is "train":
            dev_idx = int(len(processed) * .1)
            dev = processed[:dev_idx]
            train = processed[dev_idx:]
            with open(os.path.join("../processed", "tdparse", "train.json"), "w") as out:
                json.dump(train, out)
            with open(os.path.join("../processed", "tdparse", "dev.json"), "w") as out:
                json.dump(dev, out)
        else:
            with open(os.path.join("../processed", "tdparse", "{0}.json".format(name)), "w") as out:
                json.dump(processed, out)

