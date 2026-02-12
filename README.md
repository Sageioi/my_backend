🚀 FastAPI Backend Learning Project
This is a backend API built with FastAPI, following the Tech With Tim tutorials. This project serves as a hands-on exploration of building modern, high-performance web APIs with Python.

🛠 Features
Automatic Documentation: Interactive API docs via Swagger UI and ReDoc.

Type Safety: Data validation using Pydantic.

Asynchronous Support: Built to handle async/await for high performance.

RESTful Endpoints: Basic CRUD (Create, Read, Update, Delete) functionality.

🏗 Project Structure
Plaintext

.
├── main.py            # Entry point of the FastAPI application
├── requirements.txt   # Project dependencies
├── .gitignore         # Files excluded from GitHub
└── README.md          # Project documentation
⚙️ Getting Started
1. Clone the repository
Bash

git clone https://github.com/Sageioi/my_backend.git
cd my_backend
2. Set up a Virtual Environment (Optional but Recommended)
Bash

python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Run the Server
Bash

uvicorn main:app --reload
The server will start at http://127.0.0.1:8000.

API Documentation
Once the server is running, you can access the interactive documentation at:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

What I Learned
How to define API routes and methods (GET, POST, PUT, DELETE).

Using Pydantic models for request body validation.

Working with Query Parameters and Path Parameters.

Handling status codes and API exceptions.

License
This project is for educational purposes.

