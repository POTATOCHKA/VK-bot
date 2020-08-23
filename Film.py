import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from gensim.models.word2vec import Word2Vec
from nltk.stem import WordNetLemmatizer
import re


class film_advice:
    def __init__(self):
        self.data = pd.read_csv("./best_film.csv")
        self.annoy = AnnoyIndex(100, 'angular')
        self.annoy.load('annoy_for_films.ann')
        self.model = Word2Vec.load('w2v_for_films')
        self.lem = WordNetLemmatizer()

    def give_film(self, line):
        flag = False
        line = re.sub(r"\W", " ", line, flags=re.U)
        line = line.lower()
        mas = line.split()
        ve = np.zeros((100,))
        if len(mas) == 0:
            return ['incorrect request']
        for i in range(len(mas)):
            for tag in ['a', 's', 'r', 'n', 'v']:
                mas[i] = self.lem.lemmatize(mas[i], tag)
            if mas[i] in self.model:
                flag = True
                v = self.model[mas[i]]
                ve += v
        if not flag:
            return ['incorrect request']
        ve = ve / len(mas)
        sim = self.annoy.get_nns_by_vector(ve, 5, search_k=1500, include_distances=False)
        films = list()
        for i in range(len(sim)):
            name = self.data[self.data['id'] == sim[i]]['original_title'].values[0]
            films.append(name)
        return films
