# Masquerade

*Masquerade* is a simple Python script for Python 3.12.6.
It is named *masquerade.py* in this repository.
It masks VCF files with phased genotypes for genomic analyses.
Typically, VCF files with phased genotypes contain information in the following format:

| #CHROM |   POS    |   ID   | REF | ALT | QUAL | FILTER | INFO | FORMAT | Sample_1 | Sample_2 | Sample_3 |
|--------|----------|--------|-----|-----|------|--------|------|--------|----------|----------|----------|
|   1    | 3193970  |  rs6   |  A  |  G  | PASS |   .    |  GT  |    x   |   1\|1   |   1\|1   |   1\|1   |
|   1    | 3413823  |  rs7   |  A  |  G  | PASS |   .    |  GT  |    x   |   0\|1   |   0\|1   |   0\|1   |
|   1    | 3721063  |  rs8   |  A  |  G  | PASS |   .    |  GT  |    x   |   1\|0   |   1\|0   |   1\|0   |

*Masquerade* is intended for command line usage:
```
python masquerade.py [VCF_path] [MSP_path] [subpopulation_code] [output_path]
```
"VCF_path" must be a relative or absolute path to the VCF file.
"MSP_path" must be a relative or absolute path to the corresponding MSP file.
If those files are in the same directory as the current directory, just type the name of the files. 
"subpopulation_code" must correspond to a code in the first line of the MSP file.
"output_path" must be a relative or absolute path to where the output file should be created.