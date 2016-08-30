from pyspark.mllib.linalg import SparseVector

def hiphenReplc(a):
    out = []
    for i in a:
        b = i
        if '-' in i:
            b = i.replace('-','_')
        if '_' in b:
            out.extend(b.split('_'))
        else:
            out.append(b)
    return out

def encoding(tokens, theDict):
    """Produce a one-hot-encoding from a list of tokens and an OHE dictionary.

    """
    tempList = []
    for item in tokens:
        if item in theDict.keys():
            tempList.append((theDict[item],1))

    tmpVec = SparseVector(len(theDict), tempList)
    return tmpVec.toArray()

