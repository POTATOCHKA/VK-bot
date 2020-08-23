# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 01:19:10 2019

@author: User
"""



from annoy import AnnoyIndex
import gensim
import pandas as pd
from functools import reduce


class FoodGetter:
    def __init__(self): pass
    def load(self, data_path, doc2vec_path, annoy_path):
        """
            Обучатся не в состоянии, 
            можно только загрузить готовые модельки с диска
            
            Загружается секунд 5 - 7, это нормально
        """
        self.data = pd.read_csv(data_path)
        self.data.ingredients = self.data.ingredients.apply(eval)
        self.data.steps = self.data.steps.apply(eval)
        
        self.doc2vec_model = gensim.models.doc2vec.Doc2Vec.load(doc2vec_path)
        self.length = len(self.doc2vec_model.infer_vector([" "]))
        
        self.annoy_model = AnnoyIndex(self.length, 'angular')
        self.annoy_model.load(annoy_path)
    def find(self, _input, N = 5):
        """
            На вход: строка с ингредиентами
            Выход: генерируем кортеж из имени, список ингредиентов и индекс
            Если ничего не найдено возвращается пустой массив
        """
        _input = _input.split(" ")
        _res = set(_input)
        idx = self.annoy_model.get_nns_by_vector(
                self.doc2vec_model.infer_vector(_input), 1000, search_k = 2000)
        res = filter(
                lambda index: 
                    (lambda x: len(_res & x) / len(x) > 0.55)
                    (set(self.data.ingredients[index])),
                idx
                )
        ans = []
        for i, index in enumerate(res):
            if i == N:
                return ans
            temp = self.data.loc[index]
            ans.append((temp["name"], " ".join(temp.ingredients), index))
        return ans
    def get_steps(self, idx):
        "Для понравившегося индекса возвращаем инструкцию по приготовлению и номер шага"
        return enumerate(self.data.loc[idx].steps)
