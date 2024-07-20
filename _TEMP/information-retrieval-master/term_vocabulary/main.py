import re
import os
import collections
import time
import json
import string

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
matrix = {}
# This is the map of docId to input file name
docIdMap = {}

namaDokumen = ""

class index:
    def __init__(self, path):
        self.path = path
        pass

    def proses_pertama(self):       
        docId = 1
        """
            Membuat pengulangan sesuai jumlah data txt pada suatu folder
        """
        fileList = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        """
            membuat 2 file txt
            frekuensi.txt untuk menampilkan frekuensi kemunculan suatu kata
            matrix.txt untuk menampilkan kata tersebut masuk kedalam file dokumen .txt mana
        """
        fileobj = open('frekuensi.txt', 'w')
        fileobj1 = open('matrix.txt', 'w')
        for eachFile in fileList:
            position = 1
            count = 0
            # docName = "Doc_Id_" + str(docId)
            # docName =  str(docId)
            """
            Di variable bawah ini nanti akan dimasukkan id File dan nama File txtnya
            """
            docIdMap[docId] = eachFile
            """
            DI variable bawah ini kita akan mendapatkan kalimat dari tiap barisnya
            """
            lines = [line.rstrip('\n') for line in open(self.path + "/" + eachFile)]
            # print(lines) #pembuktian
            for eachLine in lines:
                """
                Di variable bawah ini kita akan memisahkan tiap kata-kata dalam 1 baris kalimat tersebut
                """
                wordList = re.split('\W+', eachLine)
                # print(wordList) #pembuktian
                while '' in wordList:
                    wordList.remove('')
                    # print("kita hapus spasi/tanda lain ", wordList) #pembuktian
                
                for word in wordList:
                    """
                    Jika kata ada di 'dictionary', cari ID dokumen.
                    Jika document id sama dengan doc id saat ini, tambahkan posisi kata ke daftar posting yang lain, buat map baru dengan docId sebagai key dan posisi sebagai value.
                    Jika kata tidak ada dalam dictionary, buat entri baru di map dengan kata sebagai key, docId dan posisinya sebagai value
                    """
                    if (word.lower() in dictionary):
                        postingList = dictionary[word.lower()]
                        if (docId in postingList):
                            postingList[docId].append(position)
                            position = position + 1
                        else:
                            postingList[docId] = [position]
                            position = position + 1
                    else:
                        dictionary[word.lower()] = {docId: [position]}
                        position = position + 1
            docId = docId + 1
        length_dict = {key: len(value) for key, value in dictionary.items()}
        """
        Membuat file frekuensi.txt
        """
        for w in length_dict:
            # ini nanti dibuat menangkap jumlah kata di suatu file txt
            # if str(w) == 'red':
            #     fileobj.write(w +"   |   "+str(length_dict[w]))
            #     fileobj.write("\n")
            fileobj.write(w +"   |   "+str(length_dict[w]))
            fileobj.write("\n")
        fileobj.close()

        """
            Membuat file matrix.txt
        """
        
        firstLine = "          **|**   "
        for d in docIdMap:
            firstLine = firstLine + " | " +str(d)
        fileobj1.write(firstLine+"   **|** ")
        fileobj1.write('\n')
        fileobj1.write('\n')
        for t in dictionary:
            poList = dictionary[t]
            kList = []
            for keys in poList:
                kList.append(keys)
            line = "       "

            for d in docIdMap:
                """
                    disini menggunakan boolean yang dimana kita cek apakah dari
                    kata tersebut masuk kedalam doc txt yang mana
                    contoh:
                    inisebuahkata  **|**        | 1 | 1 | 1 | 0 | 0
                    yang artinya
                    dari kata "inisebuahkata" itu ada di file .txt ke 1,2,3
                """
                if d in kList:
                    line = line + " | " + "1"
                else:
                    line = line + " | " + "0"

            fileobj1.write(t+"  **|**"+line)
            fileobj1.write('\n')
        fileobj1.close()
    
    def lihat_jumlah(self, nama_file, query):
        docId = 1
        temp_dictionary = {}
        lines = [line.rstrip('\n') for line in open(self.path + "/" + nama_file)]
            # print(lines) #pembuktian
        position = 1
        for eachLine in lines:
            wordList = re.split('\W+', eachLine)
            """
            Di variable bawah ini kita akan memisahkan tiap kata-kata dalam 1 baris kalimat tersebut
            """
                
                # print(wordList) #pembuktian
            while '' in wordList:
                wordList.remove('')
                    # print("kita hapus spasi/tanda lain ", wordList) #pembuktian
                
            for word in wordList:
                if (word.lower() in temp_dictionary):
                    postingList = temp_dictionary[word.lower()]
                    if (docId in postingList):
                        postingList[docId].append(position)
                        position = position + 1
                    else:
                        postingList[docId] = [position]
                        position = position + 1
                else:
                    temp_dictionary[word.lower()] = {docId: [position]}
                    position = position + 1
                   
                
            docId = docId + 1
        length_dict = {key: len(value) for key, value in temp_dictionary.items()}
        
        for key in temp_dictionary:
            # print(key + " --> " + str(temp_dictionary[key])) # pembuktian
            # print(str(temp_dictionary[key]))
            """
            	disini proses stemming buat pencocokan dari stemming inputan dengan stemming dari dokumen
            """
            if str(key) == query:
                # print(len(temp_dictionary[key]))
                # print(key + " --> " + str(temp_dictionary[key])) # pembuktian
                for s, value in temp_dictionary[key].items():
                    # print(s)
                    print("Ditemukan di line "+str(s)+" dengan frekuensi jumlah katanya "+str(len(temp_dictionary[key][s])))
                    # print(temp_dictionary[key][s])
                    # print(len(temp_dictionary[key][s]))
                    pass
                
        for key, value in temp_dictionary.items():
            if str(key) == query:
                # print(value)
                pass
                # print(json.dumps(value, indent = 4))
                for a in value:
                    pass
                    # print(json.dumps(a, indent = 4))
                # print(key +"   |   "+str(length_dict[key]))
        for w in length_dict:
            # ini nanti dibuat menangkap jumlah kata di suatu file txt
            if str(w) == query:
                print("Kesimpulan, Kata '"+w +"' terdapat "+str(length_dict[w])+" baris pada file",nama_file)
            
        

    def and_query(self, query_terms):
        # print(len(query_terms))
        if query_terms:            
            """
            Jika ada lebih dari 1 item di query_terms, itu akan mendapatkan posting list untuk istilah/kata pertama dan kedua. 
            Kemudian panggil mergePostingList () dengan meneruskan posting list term0 dan term1. 
            Hasil penggabungan akan digunakan untuk mendapatkan perpotongan dari posting list term3. 
            Ini akan diulangi untuk semua istilah kueri berikutnya.
            """
            or_operator = 'or'
            and_operator = 'and'

            clauses = query_terms.split(and_operator)
            or_terms = clauses[0].split(or_operator)

            # resultList = []
            doc_ids = set()
            for term in or_terms:
                try:
                    # print(term.replace(" ", ""))
                    a = term.replace(" ", "")
                    doc_ids.update(self.getPostingList(self.filter_string(a)))
                # print(term)
                except KeyError:
                    pass
            # print(len(clauses))
            
            for i in range(1, len(clauses)):
                or_terms = clauses[i].split(or_operator)
                # print("orr ",or_terms)
                clause_ids = set()

                for term in or_terms:
                    try:
                        # print(term)
                        a = term.replace(" ", "")
                        clause_ids.update(self.getPostingList(self.filter_string(a)))
                    except KeyError:
                        pass

                doc_ids = doc_ids.intersection(clause_ids)
            # print(doc_ids)
            
            """
            Kodingan lama
            """

            # for i in range(1, len(query_terms)):
            #     if (len(resultList) == 0):
            #         resultList = self.mergePostingList(self.getPostingList(query_terms[0]),
            #                                            self.getPostingList(query_terms[i]))
            #     else:
            #         resultList = self.mergePostingList(resultList, self.getPostingList(query_terms[i]))
            # print(resultList)
            # print("")
            # printString = "Hasil untuk Query (AND query) :"
            # i = 1
            # for keys in query_terms:
            #     if (i == len(query_terms)):
            #         printString += " " + str(keys)
            #     else:
            #         printString += " " + str(keys) + ""
            #         i = i + 1

            # print(printString)
            print("Total dokumen yang diambil : " + str(len(doc_ids)))
            # print(resultList)
            for items in doc_ids:
                namaDokumen = docIdMap[items]
                print("Nama Dokumennya:",docIdMap[items])
                self.lihat_jumlah(docIdMap[items], self.filter_string(query_terms))  

    """
            Kodingan baru
    """
    def filter_string(self, in_string):
        """ Convert the data to lowercase and remove punctuation.
            Input:
                in_string: A string.
            Output:
                out_string: The in_string converted to lowercase and stripped
                    of punctuation.
        """
        in_string = in_string .lower()

        table = str.maketrans({key: None for key in string.punctuation})
        out_string = in_string.translate(table)

        return out_string

    def getPostingList(self, term):
        if (term in dictionary):
            print("\nterm", term) #pembuktian
            postingList = dictionary[term]
            keysList = []
            for keys in postingList:
                keysList.append(keys)
            print("Id Dokumennya=",keysList) #pembuktian
            keysList.sort()
            
            return keysList
        else:
            return None

    def mergePostingList(self, list1, list2):
        print(list1, list2) #pembuktian list
        mergeResult = list(set(list1) & set(list2))
        print("sort",mergeResult) #pembuktian hasil sort
        mergeResult.sort()
        return mergeResult

    def print_dict(self):
        """
            Fungsi ini menampilkan kata berapa kali dalam sebuah dokumen dan list posting yang ada di index
        """
        fileobj = open("invertedIndex.txt", 'w')
        for key in dictionary:
            # print(key + " --> " + str(dictionary[key])) # pembuktian
            fileobj.write(key + " --> " + str(dictionary[key]))
            fileobj.write("\n")
        fileobj.close()

    def print_doc_list(self):
        for key in docIdMap:
            print("Doc ID: " + str(key) + " ==> " + str(docIdMap[key]))

def main():
    # AlamatDir = input("Masukkan nama direktori text / datasetnya  : ")
    # queryFile = input("Masukkan nama file untuk querynya : ")
    AlamatDir = "test"
    queryFile = "query"
    indexObj = index(AlamatDir)
    indexObj.proses_pertama()

    # print("")
    # print("Inverted Index :")
    # indexObj.print_dict()

    print("")
    print("List Dokumen :")
    indexObj.print_doc_list()
    print("")

    QueryLines = [line.rstrip('\n') for line in open(queryFile)]
    # print(QueryLines)
    for eachLine in QueryLines:
        """
            Kodingan lama
        """
        wordList = re.split('\W+', eachLine)

        while '' in wordList:
            wordList.remove('')

        wordsInLowerCase = []
        for word in wordList:
            wordsInLowerCase.append(word.lower())
        """
            Kodingan baru
            nnati dignati variable wordsInLowerCase kalo ingin kembali lagi
        """
        print(wordsInLowerCase)
        for kata in wordsInLowerCase:
            # print(kata)
            indexObj.and_query(kata)
        # indexObj.and_query(eachLine)

if __name__ == '__main__':
    main()
