import re
import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

# Function to read the corpus in chunks
def read_corpus_chunks(file_path, chunk_size=1024*1024):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Function to extract sentences containing a specific word from a chunk of text
def find_sentences_with_word(word, chunk):
    # Adjust the regex to handle sentences ending with '|' and a new line
    sentence_pattern = re.compile(r'([^\|]*?\b' + re.escape(word) + r'\b[^\|]*\|)', re.UNICODE)
    sentences = sentence_pattern.findall(chunk)
    return word, sentences

# Function to process each word across the entire corpus
def process_word(word, corpus_file, output_dir):
    try:
        print(f"Processing word: {word}")  # Debug statement
        sentences = []
        for chunk in read_corpus_chunks(corpus_file):
            _, chunk_sentences = find_sentences_with_word(word, chunk)
            sentences.extend(chunk_sentences)
        
        # Only write to file if sentences were found
        if sentences:
            output_file_path = os.path.join(output_dir, f"{word}.txt")
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write("\n".join(sentences))
            print(f"Sentences for '{word}' have been written to {output_file_path}")
        else:
            print(f"No sentences found for '{word}'. Skipping.")
    except Exception as e:
        print(f"Error processing word '{word}': {e}")

# Entry point of the script
if __name__ == '__main__':
    try:
        # Path to the TSV file containing Bengali words
        bengali_words_file = r'C:\Users\gangopsa\Documents\Bengali\word_list\unique_words1.tsv'

        # Path to the corpus text file
        corpus_file = r'C:\Users\gangopsa\Documents\Bengali\tokenized_sen_bn.txt'
        #print(corpus_file[10])

        # Path to the output directory where word-specific text files will be saved
        output_dir = r'C:\Users\gangopsa\Documents\Bengali\word_sentences_output'

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Read the Bengali words from the TSV file
        with open(bengali_words_file, 'r', encoding='utf-8') as bwf:
            bengali_words = [line.strip() for line in bwf]

        # Ensure the word list is not empty
        if not bengali_words:
            print("No words found in the TSV file. Exiting.")
        else:
            # Use ProcessPoolExecutor for parallel processing with multiple processes
            with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                # Passing both corpus_file and output_dir to process_word
                executor.map(process_word, bengali_words, [corpus_file] * len(bengali_words), [output_dir] * len(bengali_words))
    except Exception as e:
        print(f"An error occurred: {e}")
