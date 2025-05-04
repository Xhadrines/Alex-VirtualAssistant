# Frontend
Aceasta este **partea de frontend** a aplicației, construită folosind framework-ul **React + Vite**.

## Cerințe
Pentru a rula aplicația, trebuie să ai instalat:
* **Node.js** (v22.13.1 sau o versiune mai mare)
* **npm** (v10.9.2 sau o versiune mai mare)

## Instalare
1. Asigură-te că te afli în directorul `frontend`

2. Creează un fișier `.env` și adaugă următoarea linie:
```bash
VITE_CHAT_API=http://<IP_BACKEND>:<PORT_BACKEND>
```
*Note: Înlocuiește `<IP_BACKEND>` și `<PORT_BACKEND>` cu valorile corespunzătoare pe care le obții de la backend.*

3. Instalează dependențele folosind comanda:
```bash
npm install
```

4. Rulează proiectul folosind comanda:
```bash
npm run dev
```

5. Proiectul rulează pe `http://127.0.0.1:2002/`.
