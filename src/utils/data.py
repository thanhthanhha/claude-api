import re
import string
from bs4 import BeautifulSoup
import contractions
from spellchecker import SpellChecker
from typing import Optional, List, Dict, Callable
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer, WordNetLemmatizer
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


def clean_text(text: str):
    text = text.lower()  # Lowercase
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = re.sub(r'\W', ' ', text)  # Remove special characters
    text = BeautifulSoup(text, "html.parser").get_text()  # Remove HTML tags
    return text


def convert_token(text: str):
    tokenized_text = word_tokenize(text)
    return tokenized_text

