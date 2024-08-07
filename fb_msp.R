# Load libraries
library("vroom")
library("dplyr")
library("tidyr")

# Read command line arguments
args <- commandArgs(trailingOnly = T)
msp_file <- args[1]
fb_file <- args[2]
final_file <- args[3]

# Read MSP and FB files into dataframes
msp.df <- vroom(msp_file)
fb.df <- vroom(fb_file)

# Remove info columns
only_props <- fb.df[,5:ncol(fb.df)]
filtered_msp <- msp.df[,7:ncol(msp.df)]

# Get values for proportions
sequence_prop <- seq(0, (ncol(only_props)-4), 4)

# Create an empty dataframe to store the results
result_df <- data.frame(matrix(NA, nrow = nrow(filtered_msp), ncol = 0))

# Loop through every single row in the sequence_prop dataframe
count = 1
for (i in sequence_prop) {
  filtered.tmp <- only_props[,((i+1):(i+4))]
  filtered_na_ancestry <- filtered.tmp %>% 
    mutate(ancestry_uncertainty = apply(filtered.tmp, 1, max)) %>%
    mutate(dummy = as.numeric(row.names(filtered.tmp))) %>% 
    filter(ancestry_uncertainty < 0.65) %>% 
    pull(dummy)
  filtered_msp.tmp <- filtered_msp[,count]
  for (x in filtered_na_ancestry) {
    filtered_msp.tmp[x,] <- 4
  }
  result_df <- cbind(result_df, filtered_msp.tmp)
  count = count + 1
}

# Add the metadata info that was excluded earlier
metadata.df <- msp.df[,1:6]
modified_msp <- cbind(metadata.df,result_df)

# Save results to a file
write.table(x = modified_msp, file = final_file, quote = F, sep = "\t")
