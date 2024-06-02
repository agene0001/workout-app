import numpy as np
import pandas as pd
from nltk import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import mysql.connector

class Recommender:
    def __init__(self, database, name):
        try:
            self.db = pd.read_csv(database)
            print(self.db)
            # print(self.db[self.db['name'] == 'Noodles with Tofu'])
            # print(self.db.columns)
            # print(self.db.size)
            self.similarity_distance = []
            # print(self.db['name'])
            # self.setup('name')
        except Exception as e:
            self.db = pd.read_csv(database)
            print(self.db)
            # print(self.db[self.db['name'] == 'Noodles with Tofu'])
            # print(self.db.columns)
            # print(self.db.size)
            self.similarity_distance = []

    def tokenize_and_stem(self, text):
        # Tokenize by sentence, then by word

        stemmer = SnowballStemmer("english")
        tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]

        # Filter out raw tokens to remove noise
        filtered_tokens = [token for token in tokens if re.search('[a-zA-Z]', token)]
        # print('filtered tokens ')
        # print(filtered_tokens)

        # Stem the filtered_tokens
        stems = [stemmer.stem(word) for word in filtered_tokens]

        return stems

    def setup(self, *args):
        for arg in args:
            if 'query' not in self.db:
                self.db['query'] = ''
            self.db['query'] += (self.db[arg].astype(str)+' \n ')
        # print(self.db['query'])
        tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                            tokenizer=self.tokenize_and_stem,
                                           )

        tfidf_matrix = tfidf_vectorizer.fit_transform([x for x in self.db['query']])
        # print(tfidf_matrix)
        self.similarity_distance = 1 - cosine_similarity(tfidf_matrix)
        # df.to_csv('similarity_distance_name.csv', index=False)
        #

        # df.to_csv('similarity_distance_name.csv', index=False)
    def find_ksimilar(self, title: str, k, titleCol):
        index = self.db[self.db[titleCol].str.lower() == title.lower()]
        # print(self.db[self.db[titleCol].str.lower() == title.lower()])
        # print(index)
        index = self.db[self.db[titleCol].str.lower() == title.lower()].index[0]
        # print(index)
        vector = self.similarity_distance[index]
        # print(vector)
        most_similar = self.db.iloc[np.argsort(vector)[1:k + 1]]
        df = pd.DataFrame(most_similar,columns=most_similar.columns)
        # Debugging prints
        df.columns = df.columns
        df.drop('query',axis=1,inplace=True)
        df.replace(to_replace=np.nan, value=None, inplace=True)
#         print(df)
        return df

    def get_recipes_by_category(self,query):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="LexLuthern246!!??",
            database='automation'
        )
        # mycursor=mydb.cursor()
        # mycursor.execute(f"SELECT recipes.name FROM recipes WHERE name LIKE ? INNER JOIN ",(query,))


    # print(find_similar('Braveheart'))
    # print(find_ksimilar('Braveheart', 10))
def main():
    dbPath = 'recipes.csv'
    recipeRecommender = Recommender(dbPath, 'recipes')
    recipeRecommender.setup('name')
    print(recipeRecommender.find_ksimilar('Noodles With Tofu', 10,'name'))
    # recipeRecommender.setup('imdb_plot', 'wiki_plot')
def main1():
    dbPath = './datasets/movies.csv'
    recipeRecommender = Recommender(dbPath, 'movies')
    # recipeRecommender.setup('name', 'ingredients')
    recipeRecommender.setup('wiki_plot','imdb_plot')
    sys = recipeRecommender.find_ksimilar('Braveheart', 10, 'title')
    print(sys)

if __name__ == '__main__':
    main()