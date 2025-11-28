from fastapi import FastAPI, Path, HTTPException, Query

app = FastAPI()
import json
def load_data():
    with open("patients.json", "r") as file:
        data = file.read()
    return data

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