import os
import csv
import re

# Path to the 'raw' directory
raw_dir = r'data/raw'

# Path to the output TSV file
output_file = 'unique_words.tsv'

# Set to store unique words
unique_words = set()

# Regular expression to extract words within <word-...>
word_pattern = re.compile(r'<word-([^>]+)>')

# Iterate through each 'word' folder inside 'raw'
for word_folder in sorted(os.listdir(raw_dir)):
    word_folder_path = os.path.join(raw_dir, word_folder)
    
    # Check if it's a directory (e.g., 'word1', 'word2', ...)
    if os.path.isdir(word_folder_path):
        # Iterate through each '.txt' file inside the word folder
        for txt_file in sorted(os.listdir(word_folder_path)):
            if txt_file.endswith('.txt'):
                txt_file_path = os.path.join(word_folder_path, txt_file)
                
                # Read the first line of the .txt file with UTF-8 encoding
                try:
                    with open(txt_file_path, 'r', encoding='utf-8') as file:
                        first_line = file.readline().strip()
                        
                        # Extract words using the regex pattern
                        match = word_pattern.search(first_line)
                        if match:
                            word = match.group(1).strip()
                            unique_words.add(word)
                
                except UnicodeDecodeError:
                    # If there's an error decoding with UTF-8, try another encoding or skip the file
                    print(f"Error decoding {txt_file_path}. Skipping this file.")
                    continue

# Sort the unique words
sorted_unique_words = sorted(unique_words)

# Write the unique words to a TSV file
with open(output_file, 'w', newline='', encoding='utf-8') as tsvfile:
    tsv_writer = csv.writer(tsvfile, delimiter='\t')
    # Write each word in a new row
    for word in sorted_unique_words:
        tsv_writer.writerow([word])

print(f"Unique words have been written to {output_file}")
