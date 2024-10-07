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
"VCF_path" represents a relative or absolute path to the VCF file.
Similarly, "MSP_path" represents a path to the corresponding MSP file.
"subpopulation_code" must correspond to a code in the first line of the MSP file.
"output_path" represents the location of the new, masked VCF file.

This repository contains example files to demonstrate the proper function of *Masquerade* and its output.
To try the example, first clone the repository.
One way to do this is to use a command line interface:
```
git clone https://github.com/Kiron-Ang/Masquerade.git
```
Then, navigate into the new directory with the cloned repository files.
```
cd Masquerade
```
Now run the following command:
```
python masquerade.py example_msp.msp example_vcf.vcf 0 testing_output.vcf
```
The "testing_output.vcf" file should be created in the directory now.
The contents of "testing_output.vcf" should match the contests of "example_output.vcf"
