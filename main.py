
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel,computed_field,Field
from typing import Annotated, Literal
from fastapi.responses import JSONResponse
import json
app = FastAPI()

class Patient(BaseModel):
    """
    Patient data model for FastAPI.
    """
    id: Annotated[str, Field(..., description="The unique identifier for the patient")]
    name: Annotated[str, Field(..., description="The name of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=100, description="The age of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in centimeters")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms")]
    city: Annotated[str, Field(..., description="The city where the patient resides")]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="The gender of the patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI from height and weight."""
        return round(self.weight / ((self.height / 100) ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """Return BMI verdict."""
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.get("/")
def hello():
    return {"message": "Patient Management System"}


@app.get("/about")
def about():
    return {"message": "This is a FastAPI application for managing patient data."}


@app.get("/patients")
def get_patients():
    data = load_data()
    return {"patients": data}


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve")):
    data = load_data()
    patients = json.loads(data)
    if patient_id in patients:
        return {"patient": patients[patient_id]}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")



@app.get("/sort")
def sort_patients(sort_by:str = Query(..., description="The attribute to sort patients by height, weight, age, or bmi"),
    order: str = Query("asc", description="Sort order: asc or desc")):

    valid_fields = {"height", "weight", "age", "bmi"}

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort attribute: {sort_by}")
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail=f"Invalid sort order: {order}")

    data = load_data()
    patients = json.loads(data)
    sort_order = True if order == "desc" else False
    
    sorted_data = sorted(patients.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)

    return {"sorted_patients": sorted_data}


@app.post("/create_patient")
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    
    return JSONResponse(status_code=201,content={"message": "Patient created successfully", "patient": patient.model_dump()})