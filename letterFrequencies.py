# Approximate frequencies of letters in English. From Wikipedia.
# This includes and entry for space, and the sums with and without it.
# Divide as needed.
#
# sjd, based on sjdUtils.py. CCLI at-sa.
#
letterFreqs = [
    ( ' ',  17000 ), # Estimate for non-word chars
    ( 'e',  12702 ),
    ( 't',   9056 ),
    ( 'a',   8167 ),
    ( 'o',   7507 ),
    ( 'i',   6966 ),
    ( 'n',   6749 ),
    ( 's',   6327 ),
    ( 'h',   6094 ),
    ( 'r',   5987 ),
    ( 'd',   4253 ),
    ( 'l',   4025 ),
    ( 'c',   2782 ),
    ( 'u',   2758 ),
    ( 'm',   2406 ),
    ( 'w',   2360 ),
    ( 'f',   2228 ),
    ( 'g',   2015 ),
    ( 'y',   1974 ),
    ( 'p',   1929 ),
    ( 'b',   1492 ),
    ( 'v',    978 ),
    ( 'k',    772 ),
    ( 'j',    153 ),
    ( 'x',    150 ),
    ( 'q',     95 ),
    ( 'z',     74 ),
]

sumWithSpace = sum([ f[1] for f in letterFreqs ])

partialSums = []
ps = 0.0
for pair in letterFreqs:
    ps += pair[1]
    partialSums.append(ps)
    
def randomWeightedLetter() -> str:
    import random
    rgen = random.Random()
    r = rgen.randint(1, sumWithSpace)
    for i, tup in enumerate(partialSums):
        r -= tup[1]
        if (r<1): return(letterFreqs[i][0])
    return(' ')
