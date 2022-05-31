"""
Load Inverted Index
"""

# Dependencies
import pandas as pd
from src.inverted_index import InvertedIndex


class LoadInvertedIndex:
    """
    Load Inverted Index
    -------------------
    input_filename -> str : filename of the dataset
    """

    def __init__(self, input_filename: str) -> None:
        self.input_filename = input_filename
        self.inverted_index = None
        self.df = None

    # Load the inverted index
    def load(self) -> None:
        self.df = pd.read_csv(self.input_filename).drop(["Unnamed: 0"], axis=1)
        self.df['title_content'] = self.df.title + " " + self.df.content
        self.inverted_index = InvertedIndex(self.input_filename)
        self.inverted_index.building(self.df)
    def get_inverted_index(self):
        return self.inverted_index

# # Filename of the dataset
# archive_filename = './data/archive.csv'
# news = pd.read_csv(archive_filename).drop(["Unnamed: 0"],axis=1)
# news['title_content'] = news.title + " " + news.content
# indice = indice_invertido("NEWS")
# indice.building(news)
