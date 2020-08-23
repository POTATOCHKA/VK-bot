import numpy as np
import pandas as pd
from annoy import AnnoyIndex
import re
from gensim.models.word2vec import Word2Vec


class wise_bot:
    def __init__(self):
        self.answers = pd.read_csv("./ans_for_mail.csv")
        self.questions = pd.read_csv("./norm_mail.csv")
        self.annoy = AnnoyIndex(200, 'angular')
        self.annoy.load('annoy.ann')
        self.model = Word2Vec.load('w2v_for_mail')

    def give_answer(self, line):
        flag = False
        line = re.sub(r"\W", " ", line, flags=re.U)
        line = line.lower()
        mas = line.split()
        if len(mas) == 0:
            return ['incorrect request']
        ve = np.zeros((200,))
        for i in range(len(mas)):
            if mas[i] in self.model:
                flag = True
                v = self.model[mas[i]]
                ve += v
        if not flag:
            return ['incorrect request']
        ve = ve / len(mas)
        sim = self.annoy.get_nns_by_vector(ve, 3, search_k=5000, include_distances=False)
        answer = list()
        for i in range(3):
            ind = sim[i]
            answer.append(self.answers['---'][ind])
        return answer
