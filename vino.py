import pickle
import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from sklearn.feature_extraction.text import CountVectorizer
import re
import pymorphy2
from nltk.corpus import stopwords
import copy


class Bot:
    def __init__(self):
        self.annoy_model = AnnoyIndex(243, 'dot')
        self.annoy_model.load('annoy_model', prefault=False)
        self.data = pd.read_csv('final_alco.csv')
        with open('my_dumped_classifier.pkl', 'rb') as fid:
            self.vectorizer_model = pickle.load(fid)

    def find_buchlo(self, array):
        '''
        :param array: строка запроса пользователя
        :return: возвращаю массив bp 30 словарей, в каждом словаре лежат name-название,
        color-цвет вина(белое, красное, розовое),alcohol-количество алкоголя,description-описание(оно супер-длинное),
        sugar-какео оно по сахару(сладкое, полусладкое итд),rating-рейтинг данного винца по мнению людей


        или если я не нашел никаких совпадений запроса пользователя с имеющейся базой вкусов, я выбрасываю ValueError


        0-все сорта по близости к ответу
        1-онли красные вина
        2-белые вина
        3-онли розовые вина
        '''
        mas_regular = [array]
        for i in range(len(mas_regular)):  # юзаем регулярочек
            mas_regular[i] = re.sub(r"\W", " ", mas_regular[i], flags=re.U)
        array = mas_regular[0]
        array = array.split()
        morph = pymorphy2.MorphAnalyzer()
        for j in range(len(array)):  # нормализуем входную строку
            a = morph.parse(array[j])[0].normal_form
            array[j] = a
        stopword = stopwords.words('russian')
        stopword.append('вкус')
        stopword.append('вино')
        stopword = set(stopword)
        mas_st_wrd = []
        for j in range(len(array)):  # удаляем стоп-слова
            if array[j] not in stopword:
                mas_st_wrd.append(array[j])
        array = mas_st_wrd
        str_a = ' '.join(array)
        mas_vect = []
        mas_vect.append(str_a)
        vector = self.vectorizer_model.transform(mas_vect)  # трансформируем строку для CountVect
        if 1 not in vector.toarray()[0]:
            raise ValueError
        sim = self.annoy_model.get_nns_by_vector(vector.toarray()[0], 30, search_k=2000, include_distances=False)
        ap_dict = dict()
        mas_answers = list()
        all_vines = list()
        red_vine = list()
        white_vine = list()
        pink_vine = list()
        for i in sim:
            temp_dict = copy.deepcopy(ap_dict)
            temp_dict.update({'name': self.data['name'].loc[i]})
            temp_dict.update({'color': self.data['color'].loc[i]})
            temp_dict.update({'alcohol': self.data['alcohol'].loc[i]})
            temp_dict.update({'description': self.data['description'].loc[i]})
            temp_dict.update({'sugar': self.data['sugar'].loc[i]})
            temp_dict.update({'rating': self.data['final_rating'].loc[i]})
            if temp_dict['color'] == 'Красное':
                red_vine.append(temp_dict)
            if temp_dict['color'] == 'Белое':
                white_vine.append(temp_dict)
            if temp_dict['color'] == 'Розовое':
                pink_vine.append(temp_dict)
            all_vines.append(temp_dict)
        mas_answers.append(all_vines)
        mas_answers.append(red_vine)
        mas_answers.append(white_vine)
        mas_answers.append(pink_vine)
        return mas_answers
