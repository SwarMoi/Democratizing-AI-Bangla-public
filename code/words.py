import os
import csv
import re

# Path to the 'raw' directory
raw_dir = r'/data/raw'

# Path to the output CSV file
output_file = 'output.csv'

# List to store the results
results = []

# Function to extract the numeric part from the folder name
def extract_number(word_folder):
    match = re.search(r'(\d+)', word_folder)
    return int(match.group(1)) if match else float('inf')  # Return infinity if no number is found

# Iterate through each 'word' folder inside 'raw', sorted by the numeric value in the folder name
for word_folder in sorted(os.listdir(raw_dir), key=extract_number):
    word_folder_path = os.path.join(raw_dir, word_folder)
    
    # Check if it's a directory (e.g., 'word1', 'word2', ...)
    if os.path.isdir(word_folder_path):
        # Iterate through each '.txt' file inside the word folder, sorted in ascending order
        for txt_file in sorted(os.listdir(word_folder_path)):
            if txt_file.endswith('.txt'):
                txt_file_path = os.path.join(word_folder_path, txt_file)
                
                # Read the first line of the .txt file with UTF-8 encoding
                try:
                    with open(txt_file_path, 'r', encoding='utf-8') as file:
                        first_line = file.readline().strip()
                except UnicodeDecodeError:
                    # If there's an error decoding with UTF-8, try another encoding or skip the file
                    print(f"Error decoding {txt_file_path}. Skipping this file.")
                    continue
                
                # Get the sense name without the file extension
                sense_name = os.path.splitext(txt_file)[0]
                
                # Append the result in the desired format
                results.append((word_folder, sense_name, first_line))

# Sort the results first by word_folder (numerically), then by sense_name (lexicographically)
results.sort(key=lambda x: (extract_number(x[0]), x[1]))

# Write the results to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write the header
    csv_writer.writerow(['Word Folder', 'Sense Name', 'First Line'])
    
    # Write the data rows
    for result in results:
        csv_writer.writerow(result)

print(f"Results have been written to {output_file}")
