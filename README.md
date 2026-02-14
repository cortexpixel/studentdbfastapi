# Student Management FastAPI App

## Prerequisites
- Python 3.12
- PostgreSQL database (Supabase connection string)

## Setup

1. **Clone the repository or copy the code.**
2. **Create and activate a virtual environment (recommended):**
   
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install dependencies:**
   
  ```bash
  pip install -r requirements.txt
  ```

4. **Update the database connection string:**
   
  In `main.py`, replace `[YOUR-PASSWORD]` in the `DATABASE_URL` with your actual Supabase password.

4. **Run the FastAPI app:**
   
   ```bash
   uvicorn main:app --reload
   ```
   The app will be available at http://127.0.0.1:8000

## API Endpoints

### 1. Insert Student
- **POST** `/students/`

**Curl Example:**
```bash
curl -X POST "http://127.0.0.1:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "date_of_birth": "2000-01-01", "gender": "male"}'
```
- **Body:**
  ```json
  {
    "name": "John Doe",
    "date_of_birth": "2000-01-01",
    "gender": "male"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "date_of_birth": "2000-01-01",
    "gender": "male"
  }
  ```

### 2. Read All Students
- **GET** `/students/`

**Curl Example:**
```bash
curl "http://127.0.0.1:8000/students/"
```
- **Response:**
  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "date_of_birth": "2000-01-01",
      "gender": "male"
    },
    ...
  ]
  ```

## Notes
- The database table is created automatically on first run.
- Use the interactive docs at http://127.0.0.1:8000/docs
