# from flask import Flask, request, render_template
# import pandas as pd
# import joblib

# # Declare a Flask app
# app = Flask(__name__)

# # Main function here
# @app.route('/', methods=['GET', 'POST'])
# def main():
#     # If a form is submitted
#     if request.method == "POST":
        
#         # Unpickle classifier
#         nb = joblib.load("nb.pkl")
        
#         # Unpickle classifier
#         knn = joblib.load("knn.pkl")

#         # Get values through input bars
#         height = request.form.get("height")
#         weight = request.form.get("weight")
        
#         # Put inputs to dataframe
#         X = pd.DataFrame([[height, weight]], columns = ["Height", "Weight"])
        
#         # Get prediction
#         pred_nb = nb.predict(X)[0]
#         pred_knn = knn.predict(X)[0]
        
#     else:
#         pred_nb = ""
#         pred_knn = ""
        
#     return render_template("website.html", output = [pred_nb, pred_knn])

# # Running the app
# if __name__ == '__main__':
#     app.run(debug = True)

import re
import string
import requests
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer



def get_similar_articles(q, df):
    docs = []
    with open(r'dokumen.txt', 'r') as fp:
        for item in fp:
            x = item[:-1]
            docs.append(x)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)

    # Create a DataFrame
    df = pd.DataFrame(X.T.toarray(), index = vectorizer.get_feature_names_out())

    print("query:", q)
    print("Berikut artikel dengan nilai cosine similarity tertinggi: ")
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    sim = {}
    for i in range(10):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

    for k, v in sim_sorted:
        if v != 0.0:
            print("Nilai Similaritas:", v)
            print(docs[k])
            print()


df = pd.read_csv('dataset.csv', index_col=0)

print(df.head(100))
query = input('Masukan Kata Kunci : ')
get_similar_articles(query, df)
print('-'*100)