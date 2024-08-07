def find_start(path_to_file):
  """Function to find the column titles in an MSP/VCF file"""

  # Open the file for reading only
  opened_file = open(path_to_file, "r", encoding="utf-8")

  # First line is considered line number "0"
  start = 0

  # Iterate over every line in the file
  for line in opened_file:

    # VCF and MSP files start with a chromosome column    
    if "#c" == line[0:2].casefold():
      opened_file.close()
      print(path_to_file, "starts at line number", start)
      return start
    else:
      start += 1


def find_first_person(path_to_file, find_start_result):
  """
  Function to find the index of the first person when each row is
  converted to a list. Use this with find_start()
  """

  # Open the file for reading only
  opened_file = open(path_to_file, "r", encoding="utf-8")

  # First item in the list is considered item number "0"
  start = 0

  lines_list = opened_file.readlines()
  column_titles_list = lines_list[find_start_result].split("\t")

  # Iterate over every column title until you find a number
  for title in column_titles_list:
    # VCF and MSP files designate people with numbers
    # 0 or 1 should label the first person    
    # CHANGE SO IT USES FORMAT
    if ("FORMAT" in title) or ("snps" in title):
      opened_file.close()
      print(path_to_file, "begins people columns in", start + 1)
      return start + 1
    else:
      start += 1


def find_column_title(path_to_file, find_start_result, title_name):
  """
  Function to find the index of a column title when each row in
  a VCF or MSP is converted to a list. Use this with find_start()
  """

  # Open the file for reading only
  opened_file = open(path_to_file, "r", encoding="utf-8")

  # First item in the list is considered item number "0"
  start = 0

  lines_list = opened_file.readlines()
  column_titles_list = lines_list[find_start_result].split("\t")
  # Iterate over every column title until you find a number
  for title in column_titles_list:
    # VCF and MSP files designate people with numbers    
    if title_name.casefold() in title.casefold() :
      opened_file.close()
      print(path_to_file, f"has {title_name} in column", start)
      return start
    else:
      start += 1


def replace_dot_using_ancestry(path_to_vcf, path_to_msp, ancestry_in_msp, out_name):
  """
  Function to replace numbers in a VCF file with '.' given an MSP file
  and the number that represents the ancestry of interest in the MSP
  """

  # Open the two files in a mode for reading AND writing
  # Please use "r+" because "w" will replace the file
  opened_vcf = open(path_to_vcf, "r+", encoding="utf-8")
  opened_msp = open(path_to_msp, "r+", encoding="utf-8")

  # Open a new file that will contain the VCF modifications
  new_vcf = open(out_name, "w", encoding="utf-8")

  # Create lists where every item is a line
  vcf_lines_list = opened_vcf.readlines()
  msp_lines_list = opened_msp.readlines()

  # Call find_start() function to determine where to begin
  # This variable will change
  vcf_start = find_start(path_to_vcf)
  msp_start = find_start(path_to_msp)

  # Write the information lines and column titles in the new VCF file
  information_lines = vcf_lines_list[0:vcf_start + 1]
  for line in information_lines:
    new_vcf.write(line)

  # Figure out the index of the first person for both files
  # This variable will not change
  vcf_people = find_first_person(path_to_vcf, vcf_start)
  msp_people = find_first_person(path_to_msp, msp_start)

  # Figure out the index of the variant position in the VCF
  # This variable will not change
  vcf_pos = find_column_title(path_to_vcf, vcf_start, "pos")

  # Figure out the index of the start and end positions for the tracts in
  # the MSP file. This variable will not change
  msp_spos = find_column_title(path_to_msp, msp_start, "spos")
  msp_epos = find_column_title(path_to_msp, msp_start, "epos")

  # vcf_start and msp_start will represent the current line that the
  # program is looking at from this point on

  # Add one so we don't include the column titles
  vcf_start += 1
  msp_start += 1

  # Make lists where each item is a tract or a variant
  vcf_lines_list = vcf_lines_list[vcf_start:len(vcf_lines_list)]
  msp_lines_list = msp_lines_list[msp_start:len(msp_lines_list)]

  # Set these to 0 so we start at the beginning of the lines lists
  vcf_start = 0
  msp_start = 0

  # Keep going until all lines in VCF have been modified
  for line in vcf_lines_list:

    msp_line_now = msp_lines_list[msp_start].split("\t")
    msp_spos_value = int(msp_line_now[msp_spos])
    msp_epos_value = int(msp_line_now[msp_epos])
	
    vcf_line_now = line.split("\t")
    variant_position = int(vcf_line_now[vcf_pos])
    print("Variant at position", variant_position)

    # Some of the first tracts might not belong anywhere!
    if variant_position < msp_spos_value:
      print(f"Variant at position {variant_position} does not fit in",
          "the first tract:", msp_spos_value, "---", msp_epos_value)
      continue

    belongs = False
    # Keep checking to see which tract a variant belongs to
    # Note that we don't have to start from the beginning of the MSP
    # file every time because both the tracts and the variants
    # are sequentially listed. If you get a VCF/MSP that is not
    # ordered, just sort it in ascending order based on pos/spos
    while belongs is False:

      print(f"Tract between {msp_spos_value} & {msp_epos_value}") 
      if msp_spos_value <= variant_position <= msp_epos_value:
        print(f"Variant between {msp_spos_value} & {msp_epos_value}")
        belongs = True
      else:
        # Before moving onto the next tract range, we also have to see
        # whether the variant exists in between ranges (does not 
        # belong in any of the ranges)
        msp_start += 1
        try:
          msp_line_now = msp_lines_list[msp_start].split("\t")
          msp_spos_value = int(msp_line_now[msp_spos])
        except:
          print("End of MSP ranges reached! Function exiting now...")
          return
        # Does variant exist in a gap between tracts?
        if msp_epos_value < variant_position < msp_spos_value:
          print("This variant doesn't belong anywhere!")
          msp_start -= 1
          msp_line_now = msp_lines_list[msp_start].split("\t")
          msp_spos_value = int(msp_line_now[msp_spos])
          msp_epos_value = int(msp_line_now[msp_epos])
          break
        msp_epos_value = int(msp_line_now[msp_epos])

    if belongs is True:
      # TODO: Create a failsafe for situations where the VCF and MSP
      # files do not have the same number of people columns
      # You will get an index error when the number of people in the
      # VCF file is more than the number of people in the MSP
      # According to Fernanda, the best solution would be to compare
      # ID numbers because sometimes the missing people are scattered
      # throughout the columns and not just at the end!

      vcf_people_list = vcf_line_now[vcf_people:len(vcf_line_now)]
      msp_people_list = msp_line_now[msp_people:len(msp_line_now)]
      
      # You get an error if you have an extra item at the end of 
      # vcf_people_list
      if vcf_people_list[-1].isspace() or vcf_people_list[-1] == "":
        vcf_people_list.pop()
      
      print("People in this row of the VCF file: ", len(vcf_people_list))
      print("People in this row of the MSP file: ", len(msp_people_list) / 2)

      # Iterate through the vcf_people_list because that is what
      # we want to modify and write to a new file
      msp_person = 0
      vcf_person = 0
      for person in vcf_people_list:
        if msp_people_list[msp_person] != ancestry_in_msp:
          vcf_people_list[vcf_person] = "." + person[1:3]
        msp_person += 1
        if msp_people_list[msp_person] != ancestry_in_msp:
          vcf_people_list[vcf_person] = person[0:2] + "."
        msp_person += 1
        vcf_person += 1
      
      # Write same information
      new_vcf.write('\t'.join(vcf_line_now[0:vcf_people]))

      # Write new information
      new_vcf.write(f"\t{'\t'.join(vcf_people_list)}\n")

    # If the variant doesn't belong, just write the line without changes
    else:
      new_vcf.write(line)
    
  # Close the three files
  opened_vcf.close()
  opened_msp.close()
  new_vcf.close()


# Run the following code if this file is the file that is directly executed
if __name__ == "__main__":
  # Import the sys module for accessing command-line arguments
  import sys
  print("Importing sys")

  # Import the time module for timing execution
  import time
  print("Importing time")

  # Check if the required arguments were specified
  if len(sys.argv) < 5:
    print("Error: Please provide the VCF and MSP paths as arguments.")
    print("Please also provide the number in the MSP that represents")
    print("the ancestry of interest (0, 1, 2, etc...) and the desired")
    print("name of the new file")
    print("Usage: python main.py <VCF_path> <MSP_path> <anc_num> <out_name>")
    sys.exit(1)

  # Confirm the current Python version and the name of this script
  print(f"Executing the script named {sys.argv[0]} with Python "
      f"{sys.version_info[0]}.{sys.version_info[1]}."
      f"{sys.version_info[2]} {sys.version_info[3]} "
      f"{sys.version_info[4]}")

  # Print confirmation messages for VCF and MSP file paths
  vcf_path = sys.argv[1]
  msp_path = sys.argv[2]
  anc_num = sys.argv[3]
  out_name = sys.argv[4]
  print("The path of the VCF file you specified:", vcf_path)
  print("The path of the MSP file you specified:", msp_path)
  print("The ancestry number you specified:", anc_num)
  print("The output file will be named:", out_name)

  start_time = time.time()
  print("The start time is:", start_time)

  # Call the desired vcf-msp function
  replace_dot_using_ancestry(vcf_path, msp_path, anc_num, out_name)

  end_time = time.time()
  print("The end time is:", end_time)
  print("Total time elapsed in seconds:", end_time - start_time)
