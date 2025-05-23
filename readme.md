# Sports Forum Project

## Team Info:

| Name                | Email                       | Role          |
|---------------------|-----------------------------|---------------|
| Aruv Dand           | aadand2@illinois.edu        | Frontend      |
| Amaan Bakshi        | amaanhb2@illinois.edu       | Frontend      |
| Ethan Manivannan    | rm56@illinois.edu           | Backend       |
| Rishabh Mendiratta  | ethanm7@illinois.edu        | Backend / DB  |

# Team 34 Project Description

A full-stack web application with Next.js frontend and Flask backend. Join our forum to join and discuss in trending sports topics! Create discussions by making a post, and join others in discussion by making comments on their posts. Upvote and downvote posts to promote favorable behavior that you want in your community. 

Our project has three main components: Frontend, Backend, and the Database. The frontend allows users to interact with the application in a user friendly environment. You can login, create posts, comment, etc. by pressing buttons that link to functions in the backend, and create / modify objects in the database.


## Prerequisites

- Python 3.x
- Node.js and npm
- Git

## Setup Instructions

### Backend Setup

1. Create and activate virtual environment:
```bash
# From the root directory
cd flask_app
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

2. Install Python dependencies:
```bash
# From the flask directory (with venv activated)
pip install -r requirements.txt
```

3. Initialize the database and categories:
```bash
# From the flask directory (with venv activated)
python -m app.init_db
python -m app.init_categories
```

4. Run the Flask backend:
```bash
# From the flask directory (with venv activated)
python run.py
```

The backend will run on http://localhost:5000

### Frontend Setup

1. Install Node.js dependencies:
```bash
# From the root directory
cd next_frontend
npm install
cd ..
```

2. Run the Next.js development server:
```bash
# From the root directory
cd next_frontend
npm run dev
```

The frontend will run on http://localhost:3000

## Running the Application

1. Start the backend:
```bash
# From the root directory
cd flask_app
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
python run.py
```

2. In a new terminal, start the frontend:
```bash
# From the root directory
cd next_frontend
npm run dev
```

## Development

- Backend API endpoints are available at http://localhost:5000
- Frontend development server runs at http://localhost:3000
- The application uses hot-reloading for both frontend and backend

## Project Structure

```
.
├── flask_app/              # Backend Flask application
│   ├── app/           # Main application code
│   ├── requirements.txt
│   ├── run.py
│   └── venv/         # Python virtual environment
├── next_frontend/          # Frontend Next.js application
│   ├── src/          # Source code
│   ├── public/       # Static files
│   └── package.json
```

## Quick Start (All commands from root directory)

```bash
# 1. Set up virtual environment and backend
cd flask_app
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python -m app.init_db
python -m app.init_categories

# 2. Install frontend dependencies
cd ../next_frontend
npm install
cd ..

# 3. Start the application (in separate terminals)
# Terminal 1 - Backend:
cd flask_app
source venv/bin/activate
python run.py

# Terminal 2 - Frontend:
cd next_frontend
npm run dev

