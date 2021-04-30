## Fine-grained sentiment datasets

This repo contains code to download and preprocess the following sentiment datasets

1. Fine-grained
    1. [MPQA](https://link.springer.com/article/10.1007/s10579-005-7880-9): An English corpus of NewsWire annotated for structured sentiment
    2. [DarmStadt Service Review Corpus](https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/2448): An English corpus of online service reviews
    3. [NoReC Fine-grained](https://www.aclweb.org/anthology/2020.lrec-1.618/)
    4. [MultiBooked EU and CA](https://www.aclweb.org/anthology/L18-1104/): Hotel reviews in Basque and Catalan
    5. [OpeNER](http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/article/view/4891): Hotel reviews in English and Spanish
2. Targeted
    1. [SemEval 2014 Task 4](https://github.com/jiangqn/aspect_extraction): Restaurant and Laptop reviews in English.
    2. [Open Domain Targeted Sentiment](https://www.aclweb.org/anthology/D13-1171/): twitter dataset with various targets
    3. [TDParse](https://www.aclweb.org/anthology/E17-1046/): twitter election tweets with multiple targets per tweet.
    4. [MAMS](https://www.aclweb.org/anthology/D19-1654/): Restaurant reviews with multiple targets in each sentence.


## Requirements


## Downloading and preprocessing the data

Running the following scripts will download and process all the data. The only exception is MPQA. You will need to get the [MPQA 2.0 dataset](http://mpqa.cs.pitt.edu/corpora/mpqa_corpus/mpqa_corpus_2_0), agree to the license, download the dataset directly, and then place it in this repo before running 'get_finegrained_data.sh'

```
./get_finegrained_data.sh
./get_targeted_data.sh
./process_finegrained.sh
./process_targeted.sh
```

This will create a directory called 'processed', and in each of the subdirectories, you will find three json files (train.json, dev.json, test.json). Each json file contains a list of sentences, where each sentence is a dictionary with the following

Each sentence has a dictionary with the following keys and values:

* 'sent_id': unique NoReC identifier for document + paragraph + sentence which lines up with the identifiers from the document and sentence-level NoReC data

* 'text': raw text

* 'opinions': list of all opinions (dictionaries) in the sentence

Additionally, each opinion in a sentence is a dictionary with the following keys and values:

* 'Source': a list of text and character offsets for the opinion holder

* 'Target': a list of text and character offsets for the opinion target

* 'Polar_expression': a list of text and character offsets for the opinion expression

* 'Polarity': sentiment label ('Negative', 'Positive')

* 'Intensity': sentiment intensity ('Standard', 'Strong', 'Slight')


```
{
    'sent_id': '202263-20-01',
    'text': 'Touchbetjeningen brukes også til å besvare innkomne mobilanrop , og Sennheiser skryter av å ha doble mikrofoner i øreklokkene for å kutte ned på støyen .',
    'opinions': [
                    {
                     'Source': [['Sennheiser'], ['68:78']],
                     'Target': [['øreklokkene'], ['114:125']],
                     'Polar_expression': [['skryter av å ha doble mikrofoner i øreklokkene for å kutte ned på støyen'], ['79:151']],
                     'Polarity': 'Positive',
                     'Intensity': 'Standard'
                     }
                 ]
}
```

Note that a single sentence may contain several annotated opinions. At the same time, it is common for a given instance to lack one or more elements of an opinion, e.g. the holder (source) or target. In this case, the value for that element is [[],[]].

## Importing the data
We include train.json, dev.json, and test.json in this directory.

You can import them by using the json library in python:

```
>>> import json
>>> data = {}
>>> for name in ["train", "dev", "test"]:
        with open("{0}.json".format(name)) as infile:
            data[name] = json.load(infile)
```

## Cite
If you use this script, please cite the following paper, as well as the corresponding citations from the appropriate datasets:

```
@inproceedings{barnes-etal-2021-youve,
    title = "If you{'}ve got it, flaunt it: Making the most of fine-grained sentiment annotations",
    author = "Barnes, Jeremy  and
      {\O}vrelid, Lilja  and
      Velldal, Erik",
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume",
    month = apr,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2021.eacl-main.5",
    pages = "49--62"
}

```
