import nltk
import string

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
with open('text_file.txt', 'r') as file:
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

# Get the frequency of occurrence of all words and sort the words according to the number of occurrences from highest to lowest
word_freq = {}
for word in filtered_words:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

sorted_list = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)

# Keep only words that have occurrences between 10 and 5
filtered_list = [item for item in sorted_list if item[1] >= 5 and item[1] <= 10]

# Export words with frequency to a new file
with open('word_freq_filtered.txt', 'w') as outfile:
    for item in filtered_list:
        outfile.write("{}: {}\n".format(item[0], item[1]))
