# Doctor FastAPI Backend

A production-ready FastAPI application for managing healthcare providers and patients with comprehensive JWT authentication and role-based access control.

## 🚀 Features

✅ **JWT Authentication** - Secure token-based authentication with OAuth2  
✅ **Role-Based Access Control** - Admin and Doctor roles with proper authorization  
✅ **Production Structure** - Clean separation of concerns (routers, services, schemas, models, auth)  
✅ **Comprehensive APIs** - Full CRUD operations for doctors and patients  
✅ **Data Validation** - Pydantic v2 validation with custom validators  
✅ **Database Seeding** - Pre-loaded with sample data for testing  
✅ **Complete Test Suite** - 11 comprehensive tests covering all endpoints  
✅ **API Documentation** - Interactive Swagger UI and API guide  

## 📋 Project Structure

```
doctor_api/
├── app/
│   ├── auth/
│   │   ├── dependencies.py    # JWT and authorization helpers
│   │   └── utils.py           # Token generation and password hashing
│   ├── models/
│   │   ├── user.py            # User model with relationships
│   │   ├── doctor.py          # Doctor model
│   │   └── patient.py         # Patient model
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── doctors.py         # Doctor management endpoints
│   │   └── patients.py        # Patient management endpoints
│   ├── schemas/
│   │   ├── auth.py            # Authentication schemas
│   │   ├── user.py            # User response schemas
│   │   ├── doctor.py          # Doctor CRUD schemas
│   │   └── patient.py         # Patient schemas
│   ├── services/
│   │   ├── user_service.py    # User business logic
│   │   ├── doctor_service.py  # Doctor business logic
│   │   └── patient_service.py # Patient business logic
│   ├── config.py              # Environment configuration
│   ├── database.py            # SQLAlchemy setup
│   └── main.py                # FastAPI app initialization
├── main.py                    # Application entry point
├── seed.py                    # Database seeding script
├── test_api.py                # Comprehensive test suite
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── API_GUIDE.md              # Detailed API documentation
```

## 🔐 Authentication

- **Register**: `POST /auth/register` - Create new user account
- **Login**: `POST /auth/login` - Get JWT access token
- **Token Format**: Bearer token in Authorization header

### User Roles

- **Admin**: Can manage doctors and see all patients
- **Doctor**: Can manage own patients and assign new ones

## 📊 Database Models

### User Model
- Email (unique)
- Hashed password
- Full name
- Role (admin/doctor)
- Timestamp fields

### Doctor Model
- Name
- Specialization
- Experience
- Contact info
- User relationship

### Patient Model
- Name
- Age
- Phone
- Condition
- Doctor relationship

## 🔧 Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MySQL 5.7+
- Git

### 2. Clone Repository
```bash
git clone https://github.com/krishnarjuna2000/doctor-fastapi-api.git
cd doctor_api
```

### 3. Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate     # Linux/Mac
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
Create `.env` file in the project root:
```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=doctor_db
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
```

### 6. Start MySQL Service
Ensure MySQL is running on your system.

### 7. Run Application
```bash
python main.py
```

The API will start on `http://localhost:8000`

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token

### Doctors (Requires Auth)
- `POST /doctors` - Create doctor (Admin only)
- `GET /doctors` - Get all doctors (Admin only)
- `GET /doctors/{doctor_id}` - Get doctor details
- `PUT /doctors/{doctor_id}` - Update doctor (Admin only)
- `DELETE /doctors/{doctor_id}` - Delete doctor (Admin only)

### Patients (Requires Auth)
- `POST /patients` - Create patient
- `GET /patients` - Get patients (filtered by role)
- `GET /patients/{patient_id}` - Get patient details
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient
- `POST /patients/{patient_id}/assign-doctor` - Assign doctor to patient

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

This will test all 11 endpoints with various scenarios including:
- User registration and login
- Token generation and validation
- Authorization checks
- CRUD operations
- Error handling

## 🌱 Database Seeding

Populate the database with sample data:
```bash
python seed.py
```

This creates:
- 1 Admin user (credentials in seed.py)
- 1 Doctor user (credentials in seed.py)
- 4 Doctors with details
- 8 Patients assigned to doctors

## 📖 Detailed API Documentation

See [API_GUIDE.md](API_GUIDE.md) for:
- Complete endpoint documentation
- Request/response examples
- Error codes
- Authentication flow
- Test credentials

## 🖼️ Screenshots

### Task 1 Screenshots
Original project screenshots available in `Screenshots task 1/` directory

### Task 2 Screenshots
Updated production implementation screenshots available in `ScreenShots T2/` directory

## ⚙️ Key Dependencies

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic v2** - Data validation
- **PyJWT** - JWT token handling
- **bcrypt** - Password hashing
- **python-dotenv** - Environment configuration
- **PyMySQL** - MySQL connector

## 🐛 Error Handling

The API includes comprehensive error handling for:
- Invalid credentials (401 Unauthorized)
- Insufficient permissions (403 Forbidden)
- Resource not found (404)
- Duplicate email (400 Bad Request)
- Invalid input data (422 Unprocessable Entity)

## 📝 Validation

- **Email**: Unique, valid format
- **Password**: Securely hashed with bcrypt
- **Phone**: Proper format validation
- **Age**: Valid positive integer
- **Experience**: Non-negative for doctors

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based authorization
- CORS protection
- Input validation
- SQL injection prevention (via SQLAlchemy ORM)

## 📞 Support

For issues or questions, please check:
1. [API_GUIDE.md](API_GUIDE.md) for API details
2. The test suite in [test_api.py](test_api.py) for usage examples
3. Environment configuration in `.env.example`

## 📄 License

This project is open source and available for educational purposes.

