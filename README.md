# Journal Site

This is a journal website made with HTML/CSS/JS and a Flask API using SQLite.

Currently, the site:
- Has a **Flask API** that successfully stores + retrieves entries from a SQLite DB.
- Front end and back end are connected using **AJAX**.

## 🚀 What I Learned
- How to make an API with Flask
- How to interact with SQLite in Python
- Handling CORS

## 🧠 How to Run
1. Clone the repository
2. In one terminal run
   ```bash
   python -m http.server 5500
   ```
3. In another terminal run
   ```bash
   main.py
   ```
4. Go to ```http://localhost:5500/index.html```
5. Now you can use the website!

## 🛣️ Next Steps
- [x] Connect the frontend to the API using `AJAX`
- [x] Replace localStorage with backend DB storage
- [ ] Add user accounts (maybe with MongoDB later)
- [x] Style it up with themes / better UI
