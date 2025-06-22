import os
import re
import unicodedata
from PyPDF2 import PdfReader
import ollama


# --------------------------------------------------------------------------------------------------


class RAG:
    def __init__(self, pdf_directory="pdfs"):
        """
        Initializeaza o instanta a clasei RAG, setand directorul in care sunt stocate fisierele PDF.
        """
        self.pdf_directory = pdf_directory
        self.context = []

    def is_faculty_question(self, question):
        """
        Determina daca intrebarea utilizatorului este legata de facultate sau este una generala.
        Trimite intrebarea catre un model LLM care raspunde cu 'facultate' sau 'generala'.

        Parametru:
            question (str): Intrebarea utilizatorului.

        Returneaza:
            str: 'facultate' sau 'generala'
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "Tu trebuie sa decizi daca intrebarea este legata de Facultatea de Inginerie Electrica si Stiinta Calculatoarelor "
                    "sau daca este o intrebare generala, care nu are legatura cu facultatea.\n\n"
                    "Intrebarile legate de facultate includ, dar nu se limiteaza la: proceduri administrative, documente necesare pentru burse, programari, examene, orar, structura facultatii, resurse si servicii oferite de facultate.\n"
                    "Intrebarile generale pot fi orice intrebare care nu tine de facultate, de exemplu: 'Cum il cheama pe creatorul Python?', 'Cat face 1+1?', 'Care este capitala Frantei?', 'Retine o anumita valoarea', 'Care sunt datele mele personale?' \n\n"
                    "Raspunde doar cu un singur cuvant:\n"
                    "- 'facultate' daca intrebarea este legata de facultate,\n"
                    "- 'generala' daca intrebarea este generala sau nu are legatura cu facultatea."
                ),
            },
            {"role": "user", "content": question},
        ]
        try:
            response = ollama.chat(model="llama3.2", messages=messages)
            verdict = response["message"]["content"].strip().lower()

            return verdict
        except Exception as e:
            return f"Eroare la functia is_faculty_question: {str(e)}"

    def extract_words_from_filename(self, filename):
        """
        Extrage cuvintele din numele unui fisier PDF, inlocuind separatorii comuni cu spatii.

        Parametru:
            filename (str): Numele fisierului.

        Returneaza:
            list: Lista de cuvinte extrase din numele fisierului.
        """
        words = re.sub(r"[-_]", " ", filename)
        words = words.replace(".pdf", "").split()

        return words

    def read_pdf_content(self, pdf_path):
        """
        Citeste continutul text dintr-un fisier PDF.

        Parametru:
            pdf_path (str): Calea catre fisierul PDF.

        Returneaza:
            str: Continutul text al fisierului, concatenat pe toate paginile.
        """
        try:
            reader = PdfReader(pdf_path)
            content = ""

            for page in reader.pages:
                content += page.extract_text()

            return content
        except Exception as e:
            return f"Eroare la functia read_pdf_content: {str(e)}"

    def find_matching_files(self, question):
        """
        Gaseste fisiere PDF al caror nume contine cuvinte care apar si in intrebare.

        Parametru:
            question (str): Intrebarea utilizatorului.

        Returneaza:
            list: Nume de fisiere relevante, ordonate descrescator dupa numarul de potriviri.
        """
        matching_files = []
        question_words = re.sub(r"[^\w\s]", "", question).lower().split()
        files_with_scores = []

        for filename in os.listdir(self.pdf_directory):
            if filename.endswith(".pdf"):
                file_words = (
                    re.sub(
                        r"[^\w\s]",
                        "",
                        " ".join(self.extract_words_from_filename(filename)),
                    )
                    .lower()
                    .split()
                )
                matched_words_count = sum(word in file_words for word in question_words)

                if matched_words_count > 0:
                    files_with_scores.append((filename, matched_words_count))

        files_with_scores.sort(key=lambda x: x[1], reverse=True)
        matching_files = [filename for filename, score in files_with_scores]

        return matching_files

    def get_context(self, filename):
        """
        Obtine continutul text dintr-un fisier PDF specificat.

        Parametru:
            filename (str): Numele fisierului PDF.

        Returneaza:
            str: Textul extras din fisier.
        """
        pdf_path = os.path.join(self.pdf_directory, filename)
        content = self.read_pdf_content(pdf_path)

        return content

    def get_response(self, question, user_profile_data=None, conversation_history=None):
        """
        Genereaza un raspuns pentru intrebarea utilizatorului, folosind documente relevante sau doar modelul LLM.

        Parametri:
            question (str): Intrebarea utilizatorului.
            conversation_history (list): Istoricul conversatiei, daca exista.

        Returneaza:
            str: Raspunsul generat de model.
        """
        tip_intrebare = self.is_faculty_question(question)

        if tip_intrebare == "facultate":
            matching_files = self.find_matching_files(question)
            question_no_diacritics = remove_diacritics(question).lower()
            question_words = re.findall(r"\w+", question_no_diacritics)

            for filename in matching_files:
                context = self.get_context(filename)

                if not context:
                    continue

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Cand oferi un raspuns, asigura-te ca este prezentat intr-un mod placut intregul mesaj: cu aliniere, italic, bold si alte elemente de formatare adecvate contextului. Stilul raspunsului ar trebui sa fie prietenos si primitor, pentru a face utilizatorul sa se simta confortabil."
                            "Te rog sa raspunzi in limba romana fara diacritice."
                            "Numele tau personal este „Alex” si esti asistentul virtual al Facultatii de Inginerie Electrica si Stiinta Calculatoarelor. "
                            "Iti poti spune care e numele tau doar daca te intreba cineva sau la mesaje de bun venit cand te prezinti. "
                            "Daca trebuie sa retii un lucru, vei raspunde cu un mesaj afirmativ si vei mentiona clar ceea ce trebuie sa retii."
                        ),
                    },
                    {
                        "role": "system",
                        "content": (
                            "Cand oferi un raspuns, asigura-te ca este prezentat intr-un mod placut intregul mesaj: cu aliniere, italic, bold si alte elemente de formatare adecvate contextului. Stilul raspunsului ar trebui sa fie prietenos si primitor, pentru a face utilizatorul sa se simta confortabil."
                            f"Datele personale ale utilizatorului sunt: {user_profile_data}\n"
                            "Foloseste **doar** informatiile din contextul pentru a raspunde. Respecta urmatoarele reguli stricte:\n"
                            "- Daca intrebarea contine o categorie (ex. bursa sociala ocazionala), raspunde **doar daca** acea categorie este mentionata **identic** sau ca titlu clar in context.\n"
                            "- Daca contextul se refera la o subcategorie (ex. bursa sociala ocazionala categoria bolnavi) dar intrebarea este generala, raspunde doar: NU.\n"
                            "- Nu raspunde daca informatia este partiala, lipseste, sau este pentru alt caz decat cel intrebat.\n"
                            "- Nu interpreta. Nu deduce. Nu extinde. Nu completa.\n"
                            "- Daca nu exista o potrivire perfecta intre intrebare si context, raspunde doar: NU.\n\n"
                            "Raspunde clar si complet cu toate informatiile gasite in limba romana, fara diacritice. Nu mentiona sursa informatiilor."
                            f"Contextul este: {context}"
                        ),
                    },
                ]

                if conversation_history:
                    for item in conversation_history:
                        messages.append({"role": "user", "content": item.question})
                        messages.append({"role": "assistant", "content": item.answer})

                messages.append({"role": "user", "content": question})

                try:
                    response = ollama.chat(model="llama3.2", messages=messages)
                    raspuns_text = response["message"]["content"].strip()
                    raspuns_text = remove_diacritics(raspuns_text)

                    negative_indicators = [
                        "nu exista",
                        "nu au fost",
                        "nu sunt suficiente",
                        "nu consider",
                        "nu pot raspunde",
                        "nu se poate",
                        "nu am gasit",
                        "nu sunt informatii",
                        "nu am suficiente",
                        "nu raspund",
                        "nu pot oferi",
                        "nu este suficienta",
                        "nu este suficient",
                    ]

                    if raspuns_text.lower() == "nu" or any(
                        phrase in raspuns_text.lower() for phrase in negative_indicators
                    ):
                        continue

                    if any(word in raspuns_text.lower() for word in question_words):
                        return raspuns_text
                    else:
                        continue

                except Exception as e:
                    return f"Eroare la functia get_response: {str(e)}"

            return "Imi pare rau, dar nu am gasit un raspuns la intrebarea ta."

        else:
            # Pentru intrebari generale, se foloseste doar modelul LLM, fara context.
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Cand oferi un raspuns, asigura-te ca este prezentat intr-un mod placut intregul mesaj: cu aliniere, italic, bold si alte elemente de formatare adecvate contextului. Stilul raspunsului ar trebui sa fie prietenos si primitor, pentru a face utilizatorul sa se simta confortabil."
                        f"Datele personale ale utilizatorului sunt: {user_profile_data}\n"
                        "Te rog sa raspunzi in limba romana fara diacritice."
                        "Numele tau personal este „Alex” si esti asistentul virtual al Facultatii de Inginerie Electrica si Stiinta Calculatoarelor. "
                        "Iti poti spune care e numele tau doar daca te intreba cineva sau la mesaje de bun venit cand te prezinti. "
                        "Daca trebuie sa retii un lucru, vei raspunde cu un mesaj afirmativ si vei mentiona clar ceea ce trebuie sa retii dar doar acel lucru."
                    ),
                }
            ]

            if conversation_history:
                for item in conversation_history:
                    messages.append({"role": "user", "content": item.question})
                    messages.append({"role": "assistant", "content": item.answer})

            messages.append({"role": "user", "content": question})

            try:
                response = ollama.chat(model="llama3.2", messages=messages)
                raspuns_text = response["message"]["content"].strip()
                raspuns_text = remove_diacritics(raspuns_text)

                return raspuns_text
            except Exception as e:
                return f"Eroare la functia get_response: {str(e)}"


def remove_diacritics(text):
    """
    Elimina diacriticele dintr-un text, folosind normalizarea Unicode.

    Parametru:
        text (str): Textul de procesat.

    Returneaza:
        str: Textul fara diacritice.
    """
    nfkd_form = unicodedata.normalize("NFD", text)
    only_ascii = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    return only_ascii


# --------------------------------------------------------------------------------------------------
