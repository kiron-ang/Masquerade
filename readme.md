# Masquerade

*Masquerade* is a simple Python script for Python 3.12.6.
It masks VCF files with phased genotypes for genomic analyses.
Typically, VCF files with phased genotypes contain information in the following format:

| #CHROM |   POS    |   ID   | REF | ALT | QUAL | FILTER | INFO | FORMAT | Sample_1 | Sample_2 | Sample_3 |
|--------|----------|--------|-----|-----|------|--------|------|--------|----------|----------|----------|
|   1    | 3193970  |  rs6   |  A  |  G  | PASS |   .    |  GT  |    x   |   1\|1   |   1\|1   |   1\|1   |
|   1    | 3413823  |  rs7   |  A  |  G  | PASS |   .    |  GT  |    x   |   0\|1   |   0\|1   |   0\|1   |
|   1    | 3721063  |  rs8   |  A  |  G  | PASS |   .    |  GT  |    x   |   1\|0   |   1\|0   |   1\|0   |
