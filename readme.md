# Masquerade

This repository contains Python and R scripts to mask VCF files using information from MSP and FB files. First use an FB file to process its corresponding MSP file, and then use that MSP file to process the corresponding VCF file.

There are currently two scripts: ``fb_msp.r`` and ``msp_vcf.py``. Both of them are intended for command line usage:
- ``python msp_vcf.py <MSP_path> <VCF_path> <ancestry_number_to_replace_with_.> <name_of_new_VCF_file>``
- ``rscript fb_msp.r <FB_path> <MSP_path> <name_of_new_MSP_file>``

# Contributors

- Kiron Ang: https://github.com/Kiron-Ang, kiron_ang1@baylor.edu
- Fernanda Mirón: https://github.com/fernanda-miron, fernanda_miron1@baylor.edu
- Reynolds Lab: https://www.reynoldslab.org
