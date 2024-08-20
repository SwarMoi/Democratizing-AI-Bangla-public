import re
import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

# Function to read the corpus in chunks
def read_corpus_chunks(file_path, chunk_size=1024*1024):
    """Read the corpus file in chunks."""
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Function to extract sentences containing a specific word from a chunk of text
def find_sentences_with_word(word, chunk):
    """Find and return sentences containing the specified Bengali word in a chunk of text."""
    # Regex pattern to find sentences with the specific Bengali word
    # Sentence boundaries include period (.), Bengali Danda (।), and other punctuation.
    sentence_pattern = re.compile(rf'([^.।!?]*?\b{re.escape(word)}\b[^.।!?]*[.।!?])', re.UNICODE)
    sentences = sentence_pattern.findall(chunk)
    #print(sentences)
    return sentences

# Function to process each word across the entire corpus
def process_word(word, corpus_file, output_dir):
    """Process each word in the corpus, extracting and saving sentences containing that word."""
    try:
        print(f"Processing word: {word}")  # Debug statement
        sentences = []
        for chunk in read_corpus_chunks(corpus_file):
            chunk_sentences = find_sentences_with_word(word, chunk)
            print(chunk_sentences)
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
        bengali_words_file = r'unique_words.tsv'

        # Path to the corpus text file
        corpus_file = r'tokenized_sen_bn.txt'

        # Path to the output directory where word-specific text files will be saved
        output_dir = r'word_sentences_output'

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
                futures = [
                    executor.submit(process_word, word, corpus_file, output_dir)
                    for word in bengali_words
                ]

                # Optionally, wait for all futures to complete
                for future in futures:
                    try:
                        future.result()  # This will raise any exceptions that occurred
                    except Exception as e:
                        print(f"Error in future: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
