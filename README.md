# ComplSeq Utils

### Description
Utility to determine complementary subsequences contained into a main sequence.

For example:
* input RNA sequence: `AUGCCGAUUGCAUUUCAUACGGC`
* subsequence length: `5`
* output:
```text
Subsequence: CGAUU
Positions: 5-9
Set of complementary sequences: AGUUG, AGUCG, AAUUG, AAUCG, GGUUG, GGUCG, GAUUG, GAUCG
Complementary: GAUUG
Locations: 6-10

Subsequence: GAUUG
Positions: 6-10
Set of complementary sequences: CGGUU, CGGUC, CGAUU, CGAUC, CAGUU, CAGUC, CAAUU, CAAUC, UGGUU, UGGUC, UGAUU, UGAUC, UAGUU, UAGUC, UAAUU, UAAUC
Complementary: CGAUU
Locations: 5-9
```

**NOTE**: the output may contains complementary subsequences that overlap (see the example above).


### Usage
```text
usage: compl_seq_utils.py [-h] -i IN_FILE [-o OUT_FILE] -n N -t {dna,rna}

Complementary sequences utils

optional arguments:
  -h, --help            show this help message and exit
  -i IN_FILE, --input-file IN_FILE
                        Input file
  -o OUT_FILE, --output-file OUT_FILE
                        Output file
  -n N, --num-chars N   Number of characters in subsequence
  -t {dna,rna}, --seq-type {dna,rna}
                        Sequence type
```
