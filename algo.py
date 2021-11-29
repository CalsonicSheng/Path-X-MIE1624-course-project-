from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import warnings
import sys
import ast
warnings.filterwarnings("ignore")


def remove_words_notimportant(text):
    # add based on your preference
    business_skills = ['communication', 'presentation', 'management', 'consulting', 'leadership', 'quality',
                       'creativity']
    subject = ['financial', 'finance', 'portfolio', 'business', 'analyst', 'analysis', 'statistical', 'numerical', 'modeling',
               'control', 'probability', 'statictic', 'transportation', 'traffic', 'robotics', 'automotive', 'risk',
               'medical', 'engineer', 'scientist']
    programming_skills = ['excel', 'python', 'java', 'matlab', 'sas', 'sql', 'spss', 'tableau', 'bi', 'hadoop', 'spark',
                          'c++', 'r']
    ai = ['optimization', 'regression', 'learning', 'deep', 'machine', 'supervised', 'unsupervised', 'vision',
          'reinforced', 'neural', 'cloud', 'data']
    title = ['ECE', 'APS', 'MIE', 'MSE', 'CHE', 'CIV', 'CEM']
    important_keywords = business_skills + subject + programming_skills + ai + title
    text = [words for words in text if words in important_keywords]
    return text


def remove_punc(text):
    new_text = []
    for words in text:
        new_words = words.replace(',', '')
        new_words = new_words.replace('.', '')
        new_words = new_words.replace(':', '')
        new_words = new_words.replace(';', '')
        new_words = new_words.replace('@', '')
        new_words = new_words.replace('?', '')
        new_words = new_words.replace('!', '')
        new_words = new_words.replace("'", '')

        new_text.append(new_words)
    return new_text


def main_function(file, input_dictionary):
    """# **Import data and data clean**"""
    df_elec = pd.read_csv(file)

    df_elec['Course'] = df_elec['Department'] + df_elec['Number'].astype(str)
    df_elec['clean_text'] = df_elec['Description'].str.lower()
    df_elec['clean_title'] = df_elec['Title'].str.lower()
    df_elec['clean_text'] = df_elec['clean_text'].str.replace('[^\w\s]', '')
    df_elec['clean_text'] = df_elec['clean_text'].str.split()
    df_elec['clean_title'] = df_elec['clean_title'].str.split()
    df_elec['clean_text'] = df_elec['clean_text'].apply(remove_punc)

    """## unsupervised learning data."""
    elec_data = df_elec.drop(['Description', 'Order', 'Title'], axis=1)
    elec_data['clean_text'] = elec_data['clean_text'].apply(
        remove_words_notimportant)

    """## Make a dataframe with only 1 and 0"""
    business_skills = ['communication', 'presentation', 'management',
                       'consulting', 'leadership', 'quality', 'creativity']
    subject = ['financial', 'finance', 'portfolio', 'business', 'analyst', 'analysis', 'statistical', 'numerical', 'modeling',
               'control', 'probability', 'statictic', 'transportation', 'traffic', 'robotics', 'automotive', 'risk',
               'medical', 'engineer', 'scientist']
    programming_skills = ['excel', 'python', 'java', 'matlab', 'sas', 'sql', 'spss', 'tableau', 'bi', 'hadoop', 'spark',
                          'c++', 'r']
    ai = ['optimization', 'regression', 'learning', 'deep', 'machine', 'supervised', 'unsupervised', 'vision', 'reinforced',
          'neural', 'cloud', 'data']
    title = ['ECE', 'APS', 'MIE', 'MSE', 'CHE', 'CIV', 'CEM']
    important_keywords = business_skills + subject + programming_skills + ai + title
    important_keywords = set(important_keywords)

    feature_list = important_keywords
    df_text = pd.DataFrame(
        np.zeros((elec_data.shape[0], len(feature_list))), columns=feature_list)

    for index in elec_data.index:
        text = elec_data.loc[index, 'clean_text']
        text = set(text)
        if len(text) != 0:
            df_text.loc[index, text] = 1
        dep = elec_data.loc[index, 'Department']
        df_text.loc[index, dep] = 2

    """Then the title:  since the title is more important, add a weight of 5 to the dataframe"""
    bow = CountVectorizer()
    elec_data['clean_title'] = elec_data['clean_title'].str.join(" ")
    target = elec_data['clean_title']

    # fit the x
    bow_elec_title = bow.fit_transform(target).toarray()
    # array mapping from feature integer indices to feature name.
    word_col = bow.get_feature_names()
    # array to dataframe
    df_title = pd.DataFrame(bow_elec_title * 5, columns=word_col)

    """Then the department of the course"""
    df_elec_model = pd.concat([df_text, df_title], axis=1)

    """# model"""
    X = df_elec_model

    """31 PCs are used."""
    pca_final = PCA(n_components=31, svd_solver='full')
    scores = pca_final.fit_transform(X)

    """## K_means"""
    k_means = KMeans(n_clusters=3)
    k_means_clusters = k_means.fit_predict(scores)

    df_elec['Topic'] = k_means_clusters

    """# Final Implementation
    Input from the users:
    *   Future Career Path: Data Scientist, Machine Learnin
    *   Interested Skill/Subject To learn#
    *   Length of Program: 2/4 terms
    """

    # Example input:
    if type(input_dictionary['Career Path Choice']) == str:
        career = [input_dictionary['Career Path Choice']]
    else:
        career = input_dictionary['Career Path Choice']

    if type(input_dictionary['Skills Tree']) == str:
        skills = [input_dictionary['Skills Tree']]
    else:
        skills = input_dictionary['Skills Tree']

    # all lower case:
    career = [element.lower().split() for element in career]
    skills = [each_string.lower().split() for each_string in skills]

    proglen = input_dictionary['Program Length']

    feature_list = df_elec_model.columns.values
    df_user_input = pd.DataFrame(
        np.zeros((1, len(feature_list))), columns=feature_list)
    df_user_input.head()

    # For the career path:
    df_user_input.loc[0, career[0]] = 5
    # For the skills:
    df_user_input.loc[0, skills[0]] = 1

    # model fitting
    input_score = pca_final.transform(df_user_input)
    predict_cat = k_means.predict(input_score)[0]

    df_courses = df_elec[df_elec['Topic'] == predict_cat].sample(
        n=8).sort_values(by=['Order'])
    if proglen == 2:
        term1 = ['APS1070', 'MIE1624', df_courses.iloc[0, 5],
                 df_courses.iloc[1, 5], df_courses.iloc[2, 5]]
        term2 = [df_courses.iloc[3, 5], df_courses.iloc[4, 5], df_courses.iloc[5, 5], df_courses.iloc[6, 5],
                 df_courses.iloc[7, 5]]
        output_courses = [[1, term1], [2, term2]]
    elif proglen == 3:
        term1 = ['APS1070', 'MIE1624',
                 df_courses.iloc[0, 5], df_courses.iloc[1, 5]]
        term2 = [df_courses.iloc[2, 5], df_courses.iloc[3, 5],
                 df_courses.iloc[4, 5], df_courses.iloc[5, 5]]
        term3 = [df_courses.iloc[6, 5], df_courses.iloc[7, 5]]
        output_courses = [[1, term1], [2, term2], [3, term3]]
    else:
        term1 = ['APS1070', 'MIE1624', df_courses.iloc[0, 5]]
        term2 = [df_courses.iloc[1, 5],
                 df_courses.iloc[2, 5], df_courses.iloc[3, 5]]
        term3 = [df_courses.iloc[4, 5], df_courses.iloc[5, 5]]
        term4 = [df_courses.iloc[6, 5], df_courses.iloc[7, 5]]
        output_courses = [[1, term1], [2, term2], [3, term3], [4, term4]]
    return output_courses


# # just some try here
# file = sys.argv[1]
# # 'mie1624Proj_part4_data.csv'
# input_dictionary = ast.literal_eval(sys.argv[2])
# # {'Career Path Choice': 'data scientist',
# #  'Skills': ['excel', 'python', 'r', 'java', 'C++', 'data analytics', 'deep learning'],
# #  'Program Length': 4}
# print(main_function(file, input_dictionary))


# just some try here
# file = 'mie1624Proj_part4_data.csv'
# input_dictionary = {'Career Path Choice': 'data scientist',
#                     'Skills Tree': ['excel', 'python', 'r', 'java', 'C++', 'data analytics', 'deep learning'],
#                     'Program Length': 4}

print(main_function(sys.argv[1], ast.literal_eval(sys.argv[2])))
