#SCRAPPING
#untuk membuka URL dan mengembalikan objek yang mewakili respons dari server web. 
from urllib.request import urlopen,Request
#untuk mem-parsing dokumen HTML atau XML dan menavigasi, mencari, dan memodifikasi parse tree . 
from bs4 import BeautifulSoup
import requests

# link informasi Semua Novel populer
url= 'https://www.wattpad.com/stories/baca/hot?locale=id_ID'
# membuat objek permintaan HTTP untuk URL yang diberikan.
useragent= Request(url, headers={'User-Agent':'Mozilla/5.0'})

#Mengirimkan permintaan HTTP menggunakan objek useragent
response1=urlopen(useragent)


# Mengurai HTML menggunakan BeautifulSoup.
soup= BeautifulSoup(response1, "html.parser")
#Mencari semua div yang berisi informasi novel.
html= soup.find("div", {"class":"browse-results"}).find_all("div")

#Mendeklarasikan list untuk menyimpan data yang diekstraksi.
TitleName = []
Pencipta = []
Deskripsi = []
Dibaca=[]
Img_List=[]
links_List=[]


for row in html:
  #Mencari elemen HTML yang berisi judul novel.
  title = row.find("a", {"class": "title meta on-story-preview"})
  #Mencari elemen HTML yang berisi nama penulis.
  author=row.find("a", {"class": "username meta on-navigate"})
  #Mencari elemen HTML yang berisi deskripsi novel.
  deskripsi=row.find("div", {"class": "description"})
  #Mencari elemen HTML yang berisi jumlah pembaca.
  dibaca=row.find("span", {"class": "read-count"})
  #Mencari semua elemen HTML a yang berisi link.
  link = row.find_all('a')

# Mengambil href dari setiap tag <a>
  for a_tag in link:
        href = a_tag.get('href')
        #Mencari elemen HTML yang berisi gambar.
        img_container = row.find("div", "fixed-ratio fixed-ratio-cover")
        #Mengecek apakah elemen gambar ditemukan.
        if img_container:
            #Mencari elemen img dalam kontainer gambar.
              img = img_container.find("img")
              #Mengecek apakah elemen img ditemukan.
              if img:
                  #Mengambil URL gambar.
                  img_src = img["src"]
              else:
                  pass
        else:
              pass
        
        #Mengecek apakah elemen judul, penulis, dan deskripsi ditemukan.
        if title and author and deskripsi:
          # Mengambil dan membersihkan teks judul.
          title_text = title.text.strip()
          #Mengambil dan membersihkan teks penulis.
          author_text = author.text.strip()
          #Menghapus kata "oleh" dari teks penulis.
          author_text=author_text.replace('oleh ', '')
          #Mengambil dan membersihkan teks deskripsi.
          deskripsi_text = deskripsi.text.strip()
          #Mengambil dan membersihkan teks jumlah pembaca.
          dibaca_text= dibaca.text.strip()
          # Menyimpan URL gambar.
          img_text = img_src
          # Menyimpan URL lengkap novel.
          links= "https://www.wattpad.com"+href
          # print("href b",links)

          # Cek duplikasi judul, jika tidak ada tambahkan ke list
          if title_text not in TitleName:
              #Menambahkan data yang diekstraksi ke dalam list.
              TitleName.append(title_text)
              Pencipta.append(author_text)
              Deskripsi.append(deskripsi_text)
              Dibaca.append(dibaca_text)
              Img_List.append(img_text)
              links_List.append(links)



# Save Documents to csv
import pandas as pd

judul_novel = []
pencipta_novel = []
deskripsi_novel = []
dibaca_novel=[]
img_novel=[]
links_novel=[]

#Menambahkan Data ke List Baru:
for title, pencipta, deskripsi, img, baca,link in zip(TitleName, Pencipta, Deskripsi, Img_List, Dibaca, links_List):
    judul_novel.extend([title])
    pencipta_novel.extend([pencipta])
    deskripsi_novel.extend([deskripsi])
    dibaca_novel.extend([baca])
    img_novel.extend([img])
    links_novel.extend([link])

# Membuat DataFrame menggunakan variabel yang sudah didefinisikan sebelumnya
df = pd.DataFrame({'Judul Novel': judul_novel, 'Pencipta Novel': pencipta_novel, 'Deskripsi Novel': deskripsi_novel, 'Jumlah Pembaca': dibaca_novel, 'Img': img_novel, 'Link': links_novel})
#Menyimpan DataFrame ke file CSV docs_novel.csv.
df.to_csv('docs_novel.csv', index = False, encoding = 'utf-8')






# PREPROCESSING
#untuk operasi pencocokan pola menggunakan ekspresi reguler 
import re
#menyediakan berbagai konstanta dan kelas yang berguna untuk memanipulasi string.
import string
#membuat stemmer bahasa Indonesia
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
#untuk membuat stopword remover bahasa Indonesia.
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Membuat objek pabrik stemmer dan stopword remover.
Stemmer  = StemmerFactory()
StopWord = StopWordRemoverFactory()

#Membuat objek stemmer dan stopword remover.
stemmer  = Stemmer.create_stemmer()
stopword = StopWord.create_stop_word_remover()

#Mendeklarasikan list untuk menyimpan teks yang telah dibersihkan.
documents_clean = []
#Loop melalui setiap judul novel
for d in judul_novel:
    # Case Folding : Menghilangkan karakter non-ASCII / karakter not printable 
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
    #Menghilangkan mention (misalnya @username).
    document_test = re.sub(r'@\w+', '', document_test)
    # Mengubah teks menjadi huruf kecil.
    document_test = document_test.lower()
    # Case Folding : Menghilangkan Tanda Baca (Remove punctuation)
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    # Case Folding : Menghapus Angka 
    document_test = re.sub(r'[0-9]', '', document_test)
    #Menghilangkan spasi berlebih.
    document_test = re.sub(r'\s{2,}', ' ', document_test)
    # Melakukan stemming pada teks.
    document_test = stemmer.stem(document_test)
    # Menghilangkan stopword dari teks.
    document_test = stopword.remove(document_test)
    #Menambahkan teks yang telah dibersihkan ke list.
    documents_clean.append(document_test)

#Membuka file judul_clean.txt untuk menulis.
with open(r'judul_clean.txt', 'w') as fp:
    #Loop melalui setiap teks yang telah dibersihkan.
    for item in documents_clean:
        # Menulis teks yang telah dibersihkan ke file.
        fp.write("%s\n" % item)
