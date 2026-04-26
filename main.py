#PATIENT MANAGEMENT SYSTEM PROJECT

from fastapi import FastAPI #import fastapi
from fastapi import Path
from fastapi import HTTPException
from fastapi import Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse
import json

app=FastAPI() #create a fastapi instance

class Patient(BaseModel):
    id: Annotated[str,Field(...,description='id of the patient')]
    name: Annotated[str,Field(...,description='name of the patient')]
    city: Annotated[str,Field(...,description='city of the patient')]
    age: Annotated[int,Field(...,gt=0,lt=100,description='age of the patient')]
    gender: Annotated[Literal['male','female','other'],Field(...,description='gender of the patient')]
    height: Annotated[float,Field(...,gt=0,description='height of the patient in meteres')]
    weight: Annotated[float,Field(...,gt=0,description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi= round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'underweight'
        elif 25<self.bmi<30:
            return 'normal'
        else: 
            return 'obese'


class Patient_update(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None,gt=0)]
    gender: Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height: Annotated[Optional[float],Field(default=None,gt=0)]
    weight: Annotated[Optional[float],Field(default=None,gt=0)]


#to load the data from the json file
def load_data():
    with open('patients.json', 'r', encoding='utf-8') as f:
        data=json.load(f)
    return data

#to save the data into the json file
def save_data(data):
    with open('patients.json', 'w', encoding='utf-8') as f:
        json.dump(data,f)

@app.get("/") #define a (endpoint)route listens to GET requests-> / is the (home url)root route
def hello(): #define a function 
    return{'message':'Patient management system API'} #return a message (response)

@app.get("/about")
def about():
    return{'message':'A Fully functional API for managing patients records'}

@app.get("/view")
def view():
    data= load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(..., description='The ID of the patient to view', examples=['P001'])):
    #load all the patients data from the json file
    data= load_data()

    if patient_id in data:
        return data[patient_id]
    # else:
    #     return{'message':'Patient not found'}
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height, weight, BMI'),order:str=Query('asc',description='Sort in ascending or descending order')):

    valid_fields=['height', 'weight', 'BMI']
    valid_orders=['asc', 'desc']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field for sorting:{valid_fields}')
    if order not in valid_orders:
        raise HTTPException(status_code=400, detail=f'Invalid order:{valid_orders}')

    data= load_data()

    sort_order=True if order=='asc' else False
    sorted_data= sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):
#patient is a input of class Patient so that Patient class can put all the data validation checks on input patient
    #load existing data
    data=load_data()
    #check if the patient already exists in our database
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    #if the patient does not exist -> new patient add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])
    #save into the json file
    save_data(data)
    #return a response
    return JSONResponse(status_code=201,content={'message':'Patient created succesfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update:Patient_update):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not found')
    
    existing_patient_info=data[patient_id] #value(existing data) of the patient_id 

    updated_patient_info=patient_update.model_dump(exclude_unset=True) #gives only the fields that the client has sent to update in dictionary format

    for key, value in updated_patient_info.items():
        existing_patient_info[key]=value

    #existing_patient_info-> pydantic object-> (computed classes) updated bmi + verdict automatically if only weight or heaight or both are updated by the client then the pydantic object will be converted into a dictionary->save data
    existing_patient_info['id']=patient_id
    patient_pydantic_object=Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_object.model_dump(exclude={'id'})
    data[patient_id]=existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted'})


# uvicorn main:app --reload -> run the server and automatically keeps on reloading the server when you make changes to the code
# http://127.0.0.1:8000/ -> home url
# http://127.0.0.1:8000/about -> about url
# http://127.0.0.1:8000/view -> view all patients data
# http://127.0.0.1:8000/patient/P001 -> view patient data by ID
# http://127.0.0.1:8000/sort?sort_by=height&order=asc -> sort patients by height in ascending order
# http://127.0.0.1:8000/sort?sort_by=weight&order=desc -> sort patients by weight in descending order
# http://127.0.0.1:8000/sort?sort_by=BMI&order=asc -> sort patients by BMI in ascending order
# http://127.0.0.1:8000/sort?sort_by=BMI&order=desc -> sort patients by BMI in descending order
# http://127.0.0.1:8000/sort?sort_by=height&order=desc -> sort patients by height in descending order
# http://127.0.0.1:8000/sort?sort_by=weight&order=asc -> sort patients by weight in ascending order
# http://127.0.0.1:8000/sort?sort_by=BMI&order=asc -> sort patients by BMI in ascending order
# http://127.0.0.1:8000/sort?sort_by=BMI&order=desc -> sort patients by BMI in descending order