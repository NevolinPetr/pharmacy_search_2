def find_spn(toponym):
    lc = toponym['boundedBy']['Envelope']['lowerCorner'].split()
    uc = toponym['boundedBy']['Envelope']['upperCorner'].split()
    return str(float(uc[0]) - float(lc[0])), str(float(uc[1]) - float(lc[1]))
