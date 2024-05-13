# `eNtweniBooking`

A booking API with ride hailing and food delivery microservices.

## `Tech Stack`

    Python
    FastAPI
    Kivy/Kivymd

### `Requirements`

Requirements are found in the respective folders i.e `backend/requirements.txt` and `frontend/requirements.txt`

## `Development`

These are the development steps for both the frontend and the backend

### `Frontend`

`Linux`
```bash
cd frontend/
python -m venv venv
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt
python main.py          # run the frontend app
```

`Windows`

    cd frontend/
    python -m venv venv
    .\venv\Scripts\activate.bat # activate the virtual environment
    pip install -r requirements.txt
    python main.py          # run the frontend app

### `Backend`

`Linux`
```bash
cd backend/
python -m venv backend
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt
python -m uvicorn main:app --reload          # run the backend app
```

`Windows`

    cd backend/
    python -m venv backend
    source venv/bin/activate # activate the virtual environment
    pip install -r requirements.txt
    python -m uvicorn main:app --reload          # run the backend app

`Bootstrap`

    Download bootstrap 5 and extact it to the static folder.
    Rename the folder bootstrap

## `Deployment`

The backend server will be deployed using `Nginx Unit`, an Nginx server built to deploy multiple web apps on the same server with just different port access.

## `Contributing`

Contributions to the eNtweni Booking API are welcome and will be closely examined by lead devs before integration.
If you cannot contribute with writing code, kindly star the project and your efforts will not be taken for granted.
Thank you for supporting `eNtweni Team`
