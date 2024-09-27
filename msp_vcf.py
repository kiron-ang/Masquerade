# This Python script takes four inputs to output a new VCF file
# with valid allele frequencies for SNPs from only one
# ancestry subpopulation. Author: Kiron Ang

import sys

# Version info tuple
version_info = sys.version_info[:3]

# Test: Version info tuple not equal (3, 12, 6)
if version_info != (3, 12, 6):
  print("ERROR: Python 3.12.6 is required!")
  exit()

# Command line arguments list
argv = sys.argv

# Test: Command line arguments list length not equal five
if len(argv) != 5:
  print("ERROR: Incorrect number of command line arguments!")
  exit()

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

# Test: Output path string last three characters not equal "vcf"
if output_path[-3:] != "vcf":
  print("ERROR: Output file extension should end in .vcf!")
  exit()

# Test: Output file _io.TextIOWrapper created correctly
try:
  output = open(output_path, "w")
except:
  print("ERROR: Output file could not be created; is the path valid?")

# MSP file _io.TextIOWrapper
msp = open(msp_path)

# Read only one line at a time from each file
# This prevents reading in a large file all at once
while True:
  try:
    msp_line = next(msp)
  except:
    break

msp.close()
output.close()