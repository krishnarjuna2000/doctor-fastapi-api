<<<<<<< HEAD
# Doctor API

A beginner-friendly FastAPI project for managing doctor records with MySQL.

## Setup

1. Ensure MySQL is installed and running on your system.

2. The app can now create the database automatically on startup if it does not exist.

3. Create a `.env` file in the project root or set environment variables.

   Example `.env` file:
   ```env
   MYSQL_USER=root
   MYSQL_PASSWORD=Chintu@2000
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DB=doctor_db
   ```

   Or set the same values in PowerShell:
   ```powershell
   $env:MYSQL_USER = "root"
   $env:MYSQL_PASSWORD = "Chintu@2000"
   $env:MYSQL_HOST = "localhost"
   $env:MYSQL_PORT = "3306"
   $env:MYSQL_DB = "doctor_db"
   ```

4. Activate the virtual environment:
   ```bash
   .\venv\Scripts\Activate.ps1  # On Windows PowerShell
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:
   ```bash
   python -m uvicorn main:app --reload
   ```

7. Open your browser to `http://127.0.0.1:8000/docs` for the interactive API documentation.

## API Endpoints

- `POST /doctors` - Create a new doctor
- `GET /doctors` - Get all doctors
- `GET /doctors/{id}` - Get a doctor by ID
- `PUT /doctors/{id}` - Update a doctor
- `DELETE /doctors/{id}` - Delete a doctor

## Validation

- Email must be unique
- Experience must be >= 0
- Proper error handling for not found and duplicates

##Screenshots 
 screenshots/
- swagger_home.png
- post_doctor.png
-get_doctors.png
- get_doctor_by_id.png
-update_doctor.png
-delete_doctor.png
-value error.png
-Duplicate Email.png
- mysql_data
    
