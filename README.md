# New Project

This repository will host a web application currently in the planning stages.

## Purpose

The site will provide a simple interface for managing personal notes and tasks. Users will be able to create, edit, and organize their notes, similar to a lightweight personal productivity tool.

## Planned Stack

- **Python 3.10** with **Flask** for the backend API
- **React** with **Vite** for the frontend interface
- **PostgreSQL** for persistent storage

## Local Development

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd new_project
   ```
2. **Set up the Python environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install flask psycopg2-binary
   ```
3. **Set up the frontend**
   ```bash
   npm install -g yarn
   yarn install
   ```
4. **Run the application**
   ```bash
   # Start the Flask API
   FLASK_APP=app.py flask run

   # In another terminal, start the React dev server
   yarn dev
   ```

The above commands assume that `app.py` and the frontend `package.json` will be added later as development progresses.
