import nltk
import string
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Download the necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN 

def clean_text(text):
    # Remove numbers, symbols, and single-letter words
    words = [word.lower() for word in nltk.word_tokenize(text) if len(word) > 1 and not any(char.isdigit() or char in string.punctuation for char in word)]
    
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    tagged = nltk.pos_tag(words)
    words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos)) for word, pos in tagged]
    
    return words

# Read in text_file.txt
with open('text_file.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Clean the text by removing numbers and symbols, and lemmatizing the words
cleaned_words = clean_text(text)

# Remove words that have appeared in oxford_3000.txt
with open('oxford_3000.txt', 'r') as oxford_file:
    oxford_words = set([word.strip() for word in oxford_file])
    
filtered_words = []
for word in cleaned_words:
    if word not in oxford_words:
        filtered_words.append(word)

# Get the frequency of occurrence of all words
word_freq = {}
for word in filtered_words:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

# Convert the word frequency dictionary to a list of tuples
word_freq_list = [(word, freq) for word, freq in word_freq.items()]

# Sort the words according to the number of occurrences from highest to lowest
word_freq_list_sorted = sorted(word_freq_list, key=lambda x: x[1], reverse=True)

# Convert the sorted list back to a dictionary
word_freq_dict_sorted = {word: freq for word, freq in word_freq_list_sorted}

# Create a DataFrame from the sorted word frequency data
df_freq = pd.DataFrame({'Word': list(word_freq_dict_sorted.keys()), 'Count': list(word_freq_dict_sorted.values())})

# Export words with frequency to an Excel file on Sheet1
with pd.ExcelWriter('word_freq.xlsx') as writer:
    df_freq.to_excel(writer, sheet_name='Sheet1', index=False)
