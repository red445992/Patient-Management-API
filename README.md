# Patient Management API

This project is a FastAPI-based RESTful API for managing patient data. It allows you to view, retrieve, and sort patient information stored in a JSON file.

## Features
- Retrieve all patients
- Get details of a specific patient by ID
- Sort patients by height, weight, age, or BMI
- View basic information about the API


## Available API Endpoints

### 1. Home
- `GET /`
  - Returns a welcome message.

### 2. About
- `GET /about`
  - Returns information about the API.

### 3. Get All Patients
- `GET /patients`
  - Returns all patient data.

### 4. Get Patient by ID
- `GET /patients/{patient_id}`
  - Returns details for a specific patient.

### 5. Sort Patients
- `GET /sort?sort_by={attribute}&order={asc|desc}`
  - Sorts patients by `height`, `weight`, `age`, or `bmi` in ascending or descending order.

### 6. Create Patient
- `POST /create_patient`
  - Creates a new patient. Requires a JSON body with patient details.

### 7. Update Patient
- `PUT /edit/{patient_id}`
  - Updates an existing patient's details. Requires a JSON body with fields to update.

### 8. Delete Patient
- `DELETE /delete/{patient_id}`
  - Deletes a patient by ID.
  

## Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn

## How to Run
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
3. Access the API at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Notes
- Patient data is stored in `patients.json`.
- The API expects gender values to be lowercase: `male`, `female`, or `other`.

---
For any issues, please refer to the FastAPI and Pydantic documentation.
