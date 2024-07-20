from flask import Flask, request, render_template
# Digunakan untuk operasi numerik.
import numpy as np
#Digunakan untuk operasi data.
import pandas as pd
#Digunakan untuk mengubah teks menjadi vektor fitur TF-IDF.
from sklearn.feature_extraction.text import TfidfVectorizer

# Mendeklarasikan aplikasi Flask.
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    
# Mengecek apakah metode permintaan adalah POST (artinya formulir dikirim).
    if request.method == "POST":

        # Mengambil nilai input dari formulir dengan kunci "query".
        q = request.form.get("query")
        #  Membaca data novel dari file CSV.
        docs = pd.read_csv('docs_novel.csv')

        # untuk menyimpan data teks yang telah dibersihkan.
        docs_clean = []
        #Membuka file judul_clean.txt dalam mode baca ('r'). File pointer fp digunakan untuk membaca isi file. 
        #Penggunaan with memastikan bahwa file akan ditutup secara otomatis setelah operasi selesai, bahkan jika terjadi kesalahan.
        with open(r'judul_clean.txt', 'r') as fp:
            # iterasi melalui setiap baris dalam file judul_clean.txt
            for item in fp:
                #Menghapus karakter newline (\n) di akhir setiap baris. 
                # Ini dilakukan dengan mengambil semua karakter kecuali yang terakhir ([:-1])
                x = item[:-1]
                # Menambahkan teks yang telah dibersihkan (yaitu tanpa karakter newline) ke list docs_clean.
                docs_clean.append(x)

        # vectorizer = TfidfVectorizer(): Membuat objek TfidfVectorizer
        vectorizer = TfidfVectorizer()
        #Melatih vektorizer pada data teks bersih.
        X = vectorizer.fit_transform(docs_clean)

        # Mengubah hasil transformasi menjadi DataFrame dengan fitur sebagai indeks.
        df = pd.DataFrame(X.T.toarray(), index = vectorizer.get_feature_names_out())

        #Mengubah query pengguna menjadi vektor TF-IDF.
        q = [q]
        q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
        #Mendeklarasikan dictionary untuk menyimpan hasil kemiripan.
        sim = {}
        #untuk menghitung kemiripan antara query dan setiap dokumen.
        for i in range(10):
            #Menghitung kemiripan kosinus antara query dan dokumen.
            sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
        #Mengurutkan hasil kemiripan.
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

        #Mendeklarasikan list untuk menyimpan hasil pencarian.
        result = []
        # melalui hasil kemiripan yang telah diurutkan.
        for k, v in sim_sorted:
            #Memeriksa apakah nilai kemiripan tidak nol.
            if v != 0.0:
                #Menambahkan informasi novel yang relevan ke list result
                result.append({
                    'sim' : v,
                    'title' : docs['Judul Novel'][k],
                    'author' : docs['Pencipta Novel'][k],
                    'deskripsi' : docs['Deskripsi Novel'][k],
                    'pembaca' : docs['Jumlah Pembaca'][k],
                    'img' : docs['Img'][k],
                    'link' : docs['Link'][k],
                })        
    else:
        result = []
        
    return render_template("website.html", outputs = result)

# Running the app
if __name__ == '__main__':
    app.run(debug = True)