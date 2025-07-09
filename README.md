# JWT Authenticated FastAPI CRUD APP

    The Basic FastAPI CRUD APP which we created is now JWT Authenticated i.e only authorised users can perform
    create, read, update and delete operations for the student records.

## Project Structure

    Exercise_2_JWT_Authenticated_FastAPI_CRUD_APP/
    ├── pycache/
    ├── .env
    ├── main.py
    ├── auth.py
    ├── requirements.txt
    ├── README.md

## WorkFlow

    The FastAPI CRUD App needs to be authenticated with the JWT tokens. Before doing the operations, an authorised user logins and access token is generated.
    1. Login route is created where authorised user logins and authorises and generates access tokens.
    2. Authorised user then can perform all the CRUD operations within Access token expiry minutes.

## Setup instructions

    1. Clone the repository

        git clone https://github.com/saimanasreen001/Exercise_2_JWT_Authenticated_FastAPI_CRUD_APP.git
        cd Exercise_2_JWT_Authenticated_FastAPI_CRUD_APP

    2. Create and activate virtual environment

        python -m venv venv
        source venv/bin/activate

    3. Install all dependencies.

        pip install -r requirements.txt

    4. Run the application

        uvicorn main:app --reload

    5. Open http://127.0.0.1:8000/docs for the Swagger UI.



