## FastAPI -- Web framework used to build Python APIs. It is fast. Gives Swagger UI.
## JWT     -- manages user identity and access in applications.
from fastapi import FastAPI, HTTPException, Depends # Depends is used inside a function. Function written inside Depends is executed first and then the main function.
                                                    # HTTPException is used to raise HTTP errors.
from pydantic import BaseModel # used to define data models.
from fastapi.security import OAuth2PasswordRequestForm # OAuth2PasswordRequestForm automatically extracts form data
from datetime import timedelta # creates time durations.
from auth import(
    get_password_hash,verify_password,create_access_token,get_current_user,ACCESS_TOKEN_EXPIRE_MINUTES,HASHED_PASSWORD
)

app=FastAPI()

class Student(BaseModel): # a Student object includes
    name:str
    gender:str
    age:int

students={} # empty dictionary.

fake_user_db={
    "admin":{
        "username":"admin",
        "hashed_password":HASHED_PASSWORD
    }
}
print(get_password_hash("admin123"))

@app.post("/token")
def login(form_data:OAuth2PasswordRequestForm = Depends()): # OAuth2PasswordRequestForm automatically fetches form data
                                                            # form_data ={
                                                                # username:admin,
                                                                # password:admin123
                                                            #}
    user=fake_user_db.get(form_data.username) # user= {
                                                    #     "username": "admin",
                                                    #     "hashed_password": "$2b$12$...hashed_password..."
                                              # }
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(status_code=404,detail="Incorrect username or password")
    access_token=create_access_token(
        data={"sub":user["username"]}, #sub=admin
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }

#create
@app.post("/students/{student_id}")
#inside get_current_user (created in auth.py) from token, payload is fetched and then from payload username is fetched
def create_student(student_id:int, student:Student,username:str=Depends(get_current_user)):
    if student_id in students:
        raise HTTPException(status_code=404, detail="Student already exist")
    students[student_id]=student
    return{
        "message":"Student added successfully",
        "student":student
    }

#read
@app.get("/students/{student_id}")
def read_student(student_id:int,username:str=Depends(get_current_user)):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

#update
@app.put("/students/{student_id}")
def update_student(student_id:int, student:Student,username:str=Depends(get_current_user)):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="student not found")
    students[student_id]=student
    return{
        "message":"Student record updated",
        "student":student
    }

#delete
@app.delete("/students/{student_id}")
def delete_student(student_id:int,username:str=Depends(get_current_user)):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return{
        "message":"Student record deleted"
    }


