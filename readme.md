# Masquerade

*Masquerade* is a simple Python script for Python 3.12.6.
It is named *masquerade.py* in this repository.
It masks Variant Call Format (VCF) files with phased genotypes for genomic analyses.
Typically, VCF files with phased genotypes contain information in the following format:

```
(Pretend there are some lines of metadata above these lines.)
##fileformat=VCFv4.1
##source=gnomix.py
##FORMAT=<ID=GT,Number=1,Type=String,Description="Phased	Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample_1	Sample_2	Sample_3
1	500	rs1	A	G	PASS	.	GT	x	0|0	0|1	1|0
1	2240540	rs2	A	G	PASS	.	GT	x	1|1	0|0	1|0
1	2242069	rs3	A	G	PASS	.	GT	x	0|1	1|1	0|0
1	2242070	rs4	A	G	PASS	.	GT	x	1|0	0|1	1|1
1	2885700	rs5	A	G	PASS	.	GT	x	0|0	0|0	0|0
1	3193970	rs6	A	G	PASS	.	GT	x	1|1	1|1	1|1
(Usually there are more lines of data below these lines.)
```

*Masquerade* masks VCF files using a corresponding MSP file.
Typically, MSP files with ancestry information for samples contain information in the following format:

```
#Subpopulation	order/codes:	EUR=0	EAS=1	SAS=2
#chm	spos	epos	sgpos	egpos	snps	Sample_1.0	Sample_1.1	Sample_2.0	Sample_2.1	Sample_3.0	Sample_3.1
1	874496	1625951	0.62083	1.47449	8	0	0	1	1	2	1
1	1665535	2240544	1.53107	2.4004	8	0	1	1	0	2	0
1	2242065	2881291	2.40076	3.64002	8	0	2	1	2	2	1
1	2885647	3192587	3.66003	4.52723	8	1	1	2	2	0	0
1	3193915	3412095	4.54026	5.50877	8	1	0	2	0	0	1
1	3413826	3720895	5.52792	6.97766	8	1	2	2	1	0	2
1	3721049	3953937	6.97785	7.64991	8	2	2	0	0	1	1
1	3955322	4121478	7.65555	8.183	8	2	0	0	1	1	0
(Usually there are more lines of data below these lines.)
```

Before using *Masquerade* on real-world data, please ensure all data conforms to these assumptions:

1) The VCF file contains phased genotypes for at least one individual.
2) The MSP file corresponds to the VCF file and contains information for the exact same individuals that are present in the VCF file.
3) Both the VCF and MSP files are sorted by genetic coordinates.
4) Both the VCF and MSP files contain the same number of people.
5) The first line of the MSP file contains the subpopulation codes.
6) The first column of both the VCF and MSP contains the chromosome number.
7) People information begins in column/field #10 in the VCF file, and in column/field #7 in the MSP file.
8) Both the VCF and MSP files contain information for one chromosome.
9) Both the VCF and MSP files contain information for the same chromosome.
10) Individual-level information in the VCF is stored in one column in the format "?|?" or "?|?\n", where "?" is a single character.
11) Individual-level information in the MSP file is stored in two columns.

*Masquerade* is intended for command line usage:
```
python masquerade.py [MSP_path] [VCF_path] [subpopulation_code] [output_path]
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
The contents of "testing_output.vcf" should match the contents of "example_output.vcf".

Please contact Kiron Ang at kiron_ang1@baylor.edu for any suggestions, questions, or bug reports.