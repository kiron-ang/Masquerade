# This Python script takes four inputs to output a new VCF file
# with valid allele frequencies for SNPs from only one
# ancestry subpopulation

# Command line arguments from sys library
import sys

# Command line arguments list
argv = sys.argv

# MSP path string
msp_path = argv[1]

# Test: MSP path string last three characters not equal "msp"
if msp_path[-3:] != "msp":
  print("ERROR: File extension is not msp!")
  exit()

# VCF path string
vcf_path = argv[2]

# Test: VCF path string last three characters not equal "vcf"
if vcf_path[-3:] != "vcf":
  print("ERROR: File extension is not vcf!")
  exit()

# Subpopulation code string
subpopulation_code = argv[3]

# Test: Subpopulation code string not in MSP first line string
msp = open(msp_path)
msp_first_line = next(msp)
msp.close()

if subpopulation_code not in msp_first_line:
  print("ERROR: Not a valid subpopulation code!")
  exit()

int(subpopulation_code)

# Output path string
output_path = argv[4]

# MSP file contents TextIOWrapper
msp = open(msp_path)

# Read only one line at a time from each file
# This prevents reading in a large file all at once
while True:
  try:
    msp_line = next(msp)
  except:
    break

msp.close()