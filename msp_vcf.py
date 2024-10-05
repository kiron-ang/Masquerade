# This Python script was written by Kiron Ang
# This Python script takes four inputs to output a new VCF file
# This Python script assumes the following:
# 1) Both the VCF and MSP files are sorted by genetic coordinates
# 2) Both the VCF and MSP files contain the same number of people
# 3) The first line of the MSP file contains the subpopulation codes
# 4) The first column of both the VCF and MSP contains the chromosome number
# 5) People information begins in column/field #10 in the VCF file,
#    and in column/field #7 in the MSP file
# 6) Both the VCF and MSP files contain information for one chromosome
# 7) Both the VCF and MSP files contain information for the same chromosome
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

    # While loop: Keep advancing through MSP tracts until it is clear that
    # 1) the variant does NOT belong in a tract, or that
    # 2) the variant belongs in a tract
    keep_checking = True

    while keep_checking:

      # If pos less than spos
      if pos < spos:
        print("No tract corresponds to this variant:", spos, pos, epos)
        print("This entire line will be replaced with periods (.)")
        keep_checking = False

        # Replace all variant information with "."
        for column in range(9, len(vcf_line)):  

          # variants string
          variants = vcf_line[column]

          # Replace first variant with "."
          variants = "." + variants[1:]

          # Replace second variant with "." but check for newline
          # If newline in variants string
          if "\n" in variants:
            variants = variants[0:2] + "." + "\n"

          # Newline not in variants string
          else:
            variants = variants[0:2] + "."

          # Modify VCF line list directly
          vcf_line[column] = variants

      # pos greater than or equal to spos
      else:

        # If pos less than epos
        if pos < epos:
          print("A tract corresponds to this variant:", spos, pos, epos)
          keep_checking = False

          # Once it is clear that the variant belongs in a tract, match
          # the columns in the MSP file with the columns in the VCF file.
          # Information for each individual is stored in two ways:
          # 1) In VCF files, individual-level information is stored in one
          # column per person, starting with column #10
          # 2) in MSP files, individual-level information is stored in two
          # columns per person, starting with column #7
          # Note that with 0-based numbering, this is columns #9 and #6

          # For loop: Check every single column with an individual's data
          # and see if any values should be replaced with a ".", based on the
          # corresponding subpopulation code in the MSP line
          # MSP column integer
          msp_column = 6

          for column in range(9, len(vcf_line)):
            
            # variants string
            variants = vcf_line[column]

            # Check the MSP subpopulation for this person's first variant
            # If subpopulation code equals MSP value, leave variant untouched
            if subpopulation_code == msp_line[msp_column][0]:
              pass

            # Subpopulation code not equal, change first variant to "."
            else:
              variants = "." + variants[1:]

            # Increment MSP column number by one to move to the MSP value
            # that corresponds to the next variant for the same person
            msp_column += 1

            # Check the MSP subpopulation for the second variant
            # If subpopulation code equals MSP value, leave variant untouched
            if subpopulation_code == msp_line[msp_column][0]:
              pass

            # Subpopulation code not equal, change second variant to "."
            else:

              # If newline in variants string
              if "\n" in variants:
                variants = variants[0:2] + "." + "\n"

              # Newline not in variants string
              else:
                variants = variants[0:2] + "."

            # Increment MSP column number by one
            msp_column += 1
            
            # Modify VCF line list directly
            vcf_line[column] = variants

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