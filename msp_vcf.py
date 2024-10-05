# This Python script takes four inputs to output a new VCF file
# with valid allele frequencies for SNPs from ONLY ONE
# ancestry subpopulation. Author: Kiron Ang
print("START")

# Import libraries
import sys

# Version info tuple
version_info = sys.version_info[:3]

# Test: Version info tuple not equal (3, 12, 6)
if version_info != (3, 12, 6):
  print("ERROR: Python 3.12.6 is required!")
  exit()

# Command line arguments list
argv = sys.argv

# Test: Command line arguments list length not equal 5
if len(argv) != 5:
  print("ERROR: Incorrect number of command line arguments!")
  exit()

# MSP path string
msp_path = argv[1]

# Test: MSP path string last three characters not equal "msp"
if msp_path[-3:] != "msp":
  print("ERROR: File extension is not '.msp'!")
  exit()

# Test: Open MSP path
try:
  # MSP file _io.TextIOWrapper
  msp = open(msp_path)
except:
  print("ERROR: Unable to open MSP file! Is the path correct?")
  exit()

# VCF path string
vcf_path = argv[2]

# Test: VCF path string last three characters not equal "vcf"
if vcf_path[-3:] != "vcf":
  print("ERROR: File extension is not '.vcf'!")
  exit()

# Test: Open VCF path
try: 
  # VCF file _io.TextIOWrapper
  vcf = open(vcf_path)
except:
  print("ERROR: Unable to open VCF file! Is the path correct?")
  exit()

# Subpopulation code string
subpopulation_code = argv[3]

# Test: Subpopulation code string not in MSP first line string
if subpopulation_code not in next(msp):
  print("ERROR: Not a valid subpopulation code!")
  exit()

# Subpopulation code is now an integer
int(subpopulation_code)

# Output path string
output_path = argv[4]

# Test: Output path string last three characters not equal "vcf"
if output_path[-3:] != "vcf":
  print("ERROR: Output file extension should end in .vcf!")
  exit()

# Test: Open output path
try:
  # Output file _io.TextIOWrapper
  output = open(output_path, "x")
except:
  print("ERROR: Output file exists already or the output path is invalid.")
  exit()

#### Get the first MSP tract range! Fencepost Problem ####

# Skip column names
next(msp)

# MSP line string
msp_line = next(msp)

# MSP line list
msp_line = msp_line.split("\t")

# spos integer
spos = int(msp_line[1])

# epos integer
epos = int(msp_line[2])

# While loop: Read VCF lines until next() raises an exception
while True:
  try:
    # VCF line string
    vcf_line = next(vcf)
  except:
    break

  # VCF line list
  vcf_line = vcf_line.split("\t")

  # If VCF line list first item consists only of digits
  if vcf_line[0].isdigit():
    
    # pos integer
    pos = int(vcf_line[1])

    # While loop: Keep advancing through MSP tracts until we know that
    # 1) the variant does NOT belong in a tract, or that
    # 2) the variant belongs in a tract
    keep_checking = True

    while keep_checking:

      # If pos less than spos
      if pos < spos:
        print("No tract corresponds to this variant:", spos, pos, epos)
        keep_checking = False

      # pos greater than or equal to spos
      else:

        # If pos less than epos
        if pos < epos:
          print("A tract corresponds to this variant:", spos, pos, epos)
          keep_checking = False

        # pos greater than epos, move to next tract
        else:

          # MSP line string
          msp_line = next(msp)

          # MSP line list
          msp_line = msp_line.split("\t")

          # spos integer
          spos = int(msp_line[1])

          # epos integer
          epos = int(msp_line[2])

  # Write VCF line in the output file
  output.write("\t".join(vcf_line))


# Close files
msp.close()
vcf.close()
output.close()
print("END")