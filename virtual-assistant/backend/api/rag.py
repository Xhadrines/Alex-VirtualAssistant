import os
import re
from PyPDF2 import PdfReader
import ollama

# ----------------------------------------------------------------------------------------------------

class RAG:
    def __init__(self, pdf_directory='pdfs'):
        """
        Initializeaza clasa RAG cu directorul pentru fisiere PDF
        """
        self.pdf_directory = pdf_directory
        self.context = []
        # print(f"Initializare RAG cu directorul: {pdf_directory}")

    def extract_words_from_filename(self, filename):
        """
        Extrage cuvintele din numele fisierului folosind separatorii specificati
        """
        # print(f"Procesez numele fisierului: {filename}")
        words = re.sub(r'[-_]', ' ', filename)
        words = words.replace('.pdf', '').split()
        # print(f"Cuvintele extrase: {words}")
        return words

    def read_pdf_content(self, pdf_path):
        """
        Citeste continutul unui fisier PDF
        """
        # print(f"Incerc sa citesc fisierul: {pdf_path}")
        try:
            reader = PdfReader(pdf_path)
            content = ''
            for page in reader.pages:
                content += page.extract_text()
            # print(f"Am citit cu succes {len(content)} caractere din {pdf_path}")
            return content
        except Exception as e:
            # print(f"Eroare la citirea fisierului {pdf_path}: {str(e)}")
            return ''

    def find_matching_files(self, question):
        """
        Gaseste fisierele care contin cuvinte similare cu intrebarea
        """
        # print(f"Caut fisiere pentru intrebarea: {question}")
        matching_files = []
        question_words = re.sub(r'[^\w\s]', '', question).lower().split()
        # print(f"Cuvintele din intrebare: {question_words}")

        for word in question_words:
            for filename in os.listdir(self.pdf_directory):
                if filename.endswith('.pdf'):
                    # print(f"Verific fisierul: {filename}")
                    file_words = re.sub(r'[^\w\s]', '', ' '.join(self.extract_words_from_filename(filename))).lower().split()
                    if word in file_words:
                        if filename not in matching_files:
                            matching_files.append(filename)
                            # print(f"Am gasit potrivire pentru: {filename}")

        # print(f"Am gasit {len(matching_files)} fisiere potrivite")
        return matching_files

    def get_context(self, question):
        """
        Genereaza contextul pentru intrebare din fisierele PDF
        """
        # print(f"Generez context pentru intrebarea: {question}")
        self.context = []
        matching_files = self.find_matching_files(question)

        for filename in matching_files:
            pdf_path = os.path.join(self.pdf_directory, filename)
            content = self.read_pdf_content(pdf_path)
            if content:
                # print(f"Am adaugat continut din {filename} in context")
                self.context.append(content)

        # print(f"Context generat cu {len(self.context)} documente")
        return self.context

    def get_response(self, question, conversation_history=None):
        """
        Obtine raspunsul de la Llama3.2 folosind contextul generat
        """
        # print(f"Procesez intrebarea: {question}")
        context = self.get_context(question)

        messages = [
            {
                "role": "system",
                "content": "Te rog să răspunzi în limba română. Pe tine te cheamă „Alex” și ești asistentul virtual al Facultății de Inginerie Electrică și Știința Calculatoarelor. Nu trebuie să îți spui numele de fiecare dată, ci doar când ești întrebat. Dacă trebuie să reții un lucru, vei răspunde cu un mesaj afirmativ și vei menționa clar ceea ce trebuie să reții."
            }
        ]

        if context:
            messages.append(
                {
                    "role": "system",
                    "content": "Analizeaza urmatorul context si genereaza un raspuns scurt, direct si la obiect pe baza intrebarii: " + " ".join(context)
                },
            )
        
        # Integrează istoricul conversației în prompt
        if conversation_history:
            for item in conversation_history:
                messages.append({"role": "user", "content": item.question})
                messages.append({"role": "assistant", "content": item.answer})


        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # print("Trimit intrebarea catre Llama3.2")
        try:
            response = ollama.chat(model="llama3.2", messages=messages)
            # print("Am primit raspuns de la Llama3.2")
            return response['message']['content']
        except Exception as e:
            # print(f"Eroare la generarea raspunsului: {str(e)}")
            return f"Eroare la generarea raspunsului: {str(e)}"

# ----------------------------------------------------------------------------------------------------
