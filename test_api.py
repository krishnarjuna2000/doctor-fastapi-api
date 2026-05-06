"""
Test script to verify all API endpoints.
Requires: pip install requests
Run: python test_api.py
"""
import requests
import json
from typing import Dict, Optional

BASE_URL = "http://127.0.0.1:8001"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(test_name: str):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}{Colors.END}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_response(response: requests.Response):
    try:
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

def test_root_endpoint():
    """Test GET /"""
    print_test("Root Endpoint (GET /)")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    if response.status_code == 200:
        print_success("Root endpoint working")
        return True
    else:
        print_error("Root endpoint failed")
        return False

def test_health_check():
    """Test GET /health"""
    print_test("Health Check (GET /health)")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    if response.status_code == 200:
        print_success("Health check passed")
        return True
    else:
        print_error("Health check failed")
        return False

def test_login(email: str, password: str) -> Optional[str]:
    """Test POST /auth/login"""
    print_test(f"Login (POST /auth/login)")
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print_response(response)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print_success(f"Login successful for {email}")
        return token
    else:
        print_error(f"Login failed for {email}")
        return None

def test_get_doctors(token: str):
    """Test GET /doctors"""
    print_test("Get All Doctors (GET /doctors)")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/doctors", headers=headers)
    print_response(response)
    if response.status_code == 200:
        doctors = response.json()
        print_success(f"Retrieved {len(doctors)} doctors")
        return doctors
    else:
        print_error("Failed to get doctors")
        return None

def test_get_doctor(token: str, doctor_id: int):
    """Test GET /doctors/{id}"""
    print_test(f"Get Doctor by ID (GET /doctors/{doctor_id})")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/doctors/{doctor_id}", headers=headers)
    print_response(response)
    if response.status_code == 200:
        print_success(f"Retrieved doctor {doctor_id}")
        return response.json()
    else:
        print_error(f"Failed to get doctor {doctor_id}")
        return None

def test_create_doctor(token: str) -> Optional[Dict]:
    """Test POST /doctors (Admin only)"""
    print_test("Create Doctor (POST /doctors)")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Dr. Test Doctor",
        "email": "test.doctor@hospital.com",
        "specialization": "General Practice",
        "phone": "555-9999",
        "experience": 5,
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/doctors", json=payload, headers=headers)
    print_response(response)
    if response.status_code == 200:
        print_success("Doctor created successfully")
        return response.json()
    else:
        print_error("Failed to create doctor")
        return None

def test_get_patients(token: str):
    """Test GET /patients"""
    print_test("Get All Patients (GET /patients)")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/patients", headers=headers)
    print_response(response)
    if response.status_code == 200:
        patients = response.json()
        print_success(f"Retrieved {len(patients)} patients")
        return patients
    else:
        print_error("Failed to get patients")
        return None

def test_get_patient(token: str, patient_id: int):
    """Test GET /patients/{id}"""
    print_test(f"Get Patient by ID (GET /patients/{patient_id})")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/patients/{patient_id}", headers=headers)
    print_response(response)
    if response.status_code == 200:
        print_success(f"Retrieved patient {patient_id}")
        return response.json()
    else:
        print_error(f"Failed to get patient {patient_id}")
        return None

def test_create_patient(token: str, doctor_id: int) -> Optional[Dict]:
    """Test POST /patients (Admin only)"""
    print_test("Create Patient (POST /patients)")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Test Patient",
        "age": 40,
        "phone": "555-1234567890",
        "doctor_id": doctor_id
    }
    response = requests.post(f"{BASE_URL}/patients", json=payload, headers=headers)
    print_response(response)
    if response.status_code == 200:
        print_success("Patient created successfully")
        return response.json()
    else:
        print_error("Failed to create patient")
        return None

def test_get_doctor_patients(token: str, doctor_id: int):
    """Test GET /doctors/{doctor_id}/patients"""
    print_test(f"Get Doctor's Patients (GET /doctors/{doctor_id}/patients)")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/doctors/{doctor_id}/patients", headers=headers)
    print_response(response)
    if response.status_code == 200:
        patients = response.json()
        print_success(f"Retrieved {len(patients)} patients for doctor {doctor_id}")
        return patients
    else:
        print_error(f"Failed to get patients for doctor {doctor_id}")
        return None

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.YELLOW}")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  DOCTOR API - COMPREHENSIVE TEST SUITE".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    print(f"{Colors.END}")

    results = {
        "passed": 0,
        "failed": 0
    }

    try:
        # Test health endpoints
        if test_root_endpoint():
            results["passed"] += 1
        else:
            results["failed"] += 1

        if test_health_check():
            results["passed"] += 1
        else:
            results["failed"] += 1

        # Test authentication
        admin_token = test_login("admin@hospital.com", "admin123")
        if admin_token:
            results["passed"] += 1
        else:
            results["failed"] += 1
            print_error("Cannot proceed without authentication token")
            return results

        doctor_token = test_login("doctor1@hospital.com", "doctor1123")
        if doctor_token:
            results["passed"] += 1
        else:
            results["failed"] += 1

        # Test doctor endpoints
        doctors = test_get_doctors(admin_token)
        if doctors:
            results["passed"] += 1
        else:
            results["failed"] += 1

        if doctors:
            test_get_doctor(admin_token, doctors[0]["id"])
            results["passed"] += 1

        created_doctor = test_create_doctor(admin_token)
        if created_doctor:
            results["passed"] += 1
        else:
            results["failed"] += 1

        # Test patient endpoints
        patients = test_get_patients(admin_token)
        if patients:
            results["passed"] += 1
        else:
            results["failed"] += 1

        if patients:
            test_get_patient(admin_token, patients[0]["id"])
            results["passed"] += 1

        first_doctor_id = doctors[0]["id"] if doctors else 1
        created_patient = test_create_patient(admin_token, first_doctor_id)
        if created_patient:
            results["passed"] += 1
        else:
            results["failed"] += 1

        # Test doctor-patient endpoints
        doctor_patients = test_get_doctor_patients(admin_token, first_doctor_id)
        if doctor_patients is not None:
            results["passed"] += 1
        else:
            results["failed"] += 1

    except Exception as e:
        print_error(f"Test error: {str(e)}")
        results["failed"] += 1

    # Print summary
    print(f"\n{Colors.YELLOW}")
    print("╔" + "="*58 + "╗")
    print("║" + "  TEST SUMMARY".center(58) + "║")
    print("╠" + "="*58 + "╣")
    print(f"║ {Colors.GREEN}Passed: {results['passed']:<50}{Colors.YELLOW}║")
    print(f"║ {Colors.RED}Failed: {results['failed']:<50}{Colors.YELLOW}║")
    print("╚" + "="*58 + "╝")
    print(f"{Colors.END}")

    return results

if __name__ == "__main__":
    run_all_tests()
