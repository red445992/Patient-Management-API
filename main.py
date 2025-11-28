from fastapi import FastAPI

app = FastAPI()

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