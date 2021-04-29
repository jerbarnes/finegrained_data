import json


class Opinion:
    """
    An Opinion is a tuple which contains a holder, target, expression,
    which are lists of type [str, offsets], where str is the tokens that are included and offsets are the character offsets of these with respect to the text. Note that these can be discontinuous, i.e. 13:15;20:35.

    The label is the sentiment/emotion label which is used to characterize the relationship between the holder, target, expression triplets. It can be positive, negative, or neutral.

    The intensity modifies the label and can be strong, normal, or weak.
    """
    #
    def __init__(self,
                 text,
                 holder=None,
                 target=None,
                 expression=None,
                 label=None,
                 intensity=None,
                 ):
        #
        self.data = {"text": text,
                     "holder": holder,
                     "target": target,
                     "expression": expression,
                     "label": label,
                     "intensity": intensity}
    #
    def __repr__(self):
        return str(self.data)
    def __str__(self):
        return str(self.data)
    def to_json(self):
        return {}


class Dataset:
    """
    A dataset object is used to import and export data saved as json files.
    It returns a list of {idx, text, opinions} dictionaries.
    """

    def __init__(self, file):
        with open(file) as o:
            self.data = json.load(o)
