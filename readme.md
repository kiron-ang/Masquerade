# Masquerade

This repository contains Python and R scripts to mask VCF files using information from MSP and FB files. First use an FB file to process its corresponding MSP file, and then use that MSP file to process the corresponding VCF file.

There are currently two scripts: ``fb_msp.r`` and ``msp_vcf.py``. Both of them are intended for command line usage:
- ``python msp_vcf.py <MSP_path> <VCF_path> <ancestry_integer> <output_name>``
  - MSP_path: Path to the MSP file.
  - VCF_path: Path to the VCF file.
  - ancestry_integer: Integer in the MSP file that represents the ancestry of focus for your work. All SNPs that are attributed to that ancestry will be kept in the final VCF file. The other SNPs from other ancestry lineages will still be kept, but they will be replaced with "." in each person's genotype in the final VCF file. This will end up looking something like "0|.", ".|0", or ".|.".
  - output_name: Name of the new, masked VCF file.
- ``rscript fb_msp.r <FB_path> <MSP_path> <output_name>``
  - FB_path: Path to the FB file.
  - MSP_path: Path to the MSP file.
  - output_name: Name of the new, modified MSP file.

# Contributors

- Kiron Ang: https://github.com/Kiron-Ang, kiron_ang1@baylor.edu
- Fernanda Mirón: https://github.com/fernanda-miron, fernanda_miron1@baylor.edu
- Reynolds Lab: https://www.reynoldslab.org
