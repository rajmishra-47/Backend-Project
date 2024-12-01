from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional,List
from pymongo import MongoClient
from bson import ObjectId

app=FastAPI()

client = MongoClient("mongodb+srv://rajnandanmishra422:SzvkgHXupuEptzjQ@cluster0-0.5x4ew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0-0")

db = client["Sample-Data"]  
collection = db["Project0.0"] 



class Address(BaseModel):
    city:str
    country:str

class Student(BaseModel):
    name:str
    age:int
    address:Address


class Data(BaseModel):
    name:str
    age:int

class StudentData(BaseModel):
    data:List[Data]

class StudentID(BaseModel):
    id:str


def student_helper(student) -> dict:
    return {
        "name": student["name"],
        "age": student["age"],
        "address": student["address"]
    }


@app.post('/students',response_model=StudentID,status_code=201)
async def Create_Students(student:Student):
    result = collection.insert_one(student.model_dump())
    student_body = student.model_dump()  
    student_body['id'] = str(result.inserted_id)
    return StudentID(id=student_body['id'])


@app.get('/students',status_code=200)
async def List_students():
    students = list(collection.find())
    student_data = [Data(name=student['name'], age=student['age']) for student in students]
    return StudentData(data=student_data)


@app.get("/students/{id}",status_code=200)
async def Fetch_student(id: str):
    student = collection.find_one({"_id": ObjectId(id)})
    return student_helper(student)


@app.patch("/students/{id}",status_code=204)
async def Update_student(id: str, student: Student):
    student_id = ObjectId(id)
    update_fields = {}
    if not student.name:
        update_fields["name"] = student.name
    if not student.age:
        update_fields["age"] = student.age
    if not student.address:
        update_fields["address"] = student.address.model_dump(exclude_unset=True)

    collection.update_one({"_id": student_id}, {"$set": update_fields})
    return {}



@app.delete("/students/{id}",status_code=200)
async def Delete_student(id:str):
    student_id = ObjectId(id)

    ids= collection.find_one({"_id":student_id})

    if not ids:
        return "Field Does Not Exist"    

    collection.delete_one({"_id": student_id})
    return {}

# if __name__=="__main__":
#     import uvicorn
#     uvicorn.run(app,host="0.0.0.0",port=8000)




# rajnandanmishra422
# SzvkgHXupuEptzjQ