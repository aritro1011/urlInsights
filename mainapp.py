import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from nltk.tokenize import word_tokenize, sent_tokenize
import chardet
import syllapy


# Function to extract and clean text from URL
def extract_text_from_url(url, folder_name, index=1):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    domain_name = urlparse(url).netloc.split('.')[1]
    file_name = f"{domain_name}{index}.txt"
    file_path = os.path.join(folder_name, file_name)
    
    if os.path.exists(file_path):
        print(f"Text file already exists: {file_path}")
        return file_path
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = '\n'.join([para.get_text() for para in paragraphs])
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully extracted and saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None

# Function to load dictionaries for stop words and sentiment analysis
def load_dictionaries(folder_path):
    stop_words, positive, negative = set(), set(), set()
    
    for file_name, target_set in [('StopWords.txt', stop_words), ('positive-words.txt', positive), ('negative-words.txt', negative)]:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                encoding = chardet.detect(file.read())['encoding']
            with open(file_path, 'r', encoding=encoding) as file:
                target_set.update(word.strip().lower() for word in file if word.strip())
    
    return stop_words, positive, negative

# Function to calculate sentiment analysis metrics
def calculate_sentiment(text, stop_words, positive_words, negative_words):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word not in stop_words]

    positive_score = sum(1 for word in filtered_words if word in positive_words)
    negative_score = sum(1 for word in filtered_words if word in negative_words)
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(filtered_words) + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score

# Function to calculate readability metrics
def calculate_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    avg_sentence_length = len(words) / len(sentences) if len(sentences) > 0 else 0
    complex_words = sum(1 for word in words if len(word) > 6)
    percentage_complex = complex_words / len(words) if len(words) > 0 else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex)
    
    return fog_index, avg_sentence_length, complex_words

# Function to calculate other text-based metrics
def calculate_other_metrics(text):
    words = re.findall(r'\b\w+\b', text)
    syllable_count = sum(sum(1 for char in word if char in 'aeiou') for word in words)
    personal_pronouns = sum(1 for word in words if word in {'i', 'we', 'my', 'ours', 'us'})
    avg_word_length = sum(len(word) for word in words) / len(words) if len(words) > 0 else 0
    
    return len(words), syllable_count, personal_pronouns, avg_word_length

# Function to process multiple URLs from an input file
def process_urls(input_file, output_file, dictionaries_folder, folder_name):
    stop_words = load_dictionaries(dictionaries_folder)[0]
    positive_words = load_dictionaries(dictionaries_folder)[1]
    negative_words = load_dictionaries(dictionaries_folder)[2]

    urls = pd.read_excel(input_file)['URL'].tolist()
    analysis_results = []

    for i, url in enumerate(urls, start=1):
        print(f"Processing URL {i}: {url}")
        file_path = extract_text_from_url(url, folder_name, i)

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment(text, stop_words, positive_words, negative_words)
            fog_index, avg_sentence_length, complex_words = calculate_readability(text)
            word_count, syllable_count, personal_pronouns, avg_word_length = calculate_other_metrics(text)

            metrics = {
                'URL': url,
                'Positive Score': positive_score,
                'Negative Score': negative_score,
                'Polarity Score': polarity_score,
                'Subjectivity Score': subjectivity_score,
                'Fog Index': fog_index,
                'Average Sentence Length': avg_sentence_length,
                'Complex Word Count': complex_words,
                'Word Count': word_count,
                'Syllable Count': syllable_count,
                'Personal Pronouns': personal_pronouns,
                'Average Word Length': avg_word_length
            }
            analysis_results.append(metrics)
        else:
            analysis_results.append({'URL': url, 'Status': 'Failed to analyze'})

    df = pd.DataFrame(analysis_results)
    df.to_excel(output_file, index=False)
    print(f"Analysis results saved to {output_file}")

# Main function for program options
def main():
    import nltk
nltk.download('punkt')

# Your existing code below

    print("Welcome to the Text Analysis Program!")
    print("Choose an option:")
    print("1. Analyze a single URL")
    print("2. Analyze multiple URLs from an input file")

    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        url = input("Enter the URL: ").strip()
        folder_name = "extracted_texts"
        dictionaries_folder = "dictionaries"
        
        extracted_file_path = extract_text_from_url(url, folder_name)
        if extracted_file_path:
            stop_words, positive_words, negative_words = load_dictionaries(dictionaries_folder)
            with open(extracted_file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            report = {
                **dict(zip(['Positive Score', 'Negative Score', 'Polarity Score', 'Subjectivity Score'],
                           calculate_sentiment(text, stop_words, positive_words, negative_words))),
                **dict(zip(['Fog Index', 'Average Sentence Length', 'Complex Word Count'],
                           calculate_readability(text))),
                **dict(zip(['Word Count', 'Syllable Count', 'Personal Pronouns', 'Average Word Length'],
                           calculate_other_metrics(text)))
            }
            
            print("\nSummary Report:")
            for metric, value in report.items():
                print(f"{metric}: {value}")
        else:
            print("Failed to extract text from the URL.")

    elif choice == "2":
        input_file = input("Enter the input file name (with extension, e.g., input.xlsx): ").strip()
        output_file = input("Enter the output file name (with extension, e.g., output.xlsx): ").strip()
        dictionaries_folder = "dictionaries"
        folder_name = "extracted_texts"
        
        process_urls(input_file, output_file, dictionaries_folder, folder_name)
    else:
        print("Invalid choice! Please restart the program and choose either 1 or 2.")

if __name__ == "__main__":
    main()
