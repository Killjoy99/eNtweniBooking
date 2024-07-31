# `eNtweniBooking`


## MY GIT Commands
```sh
git pull                    # request update from remote branch
git add .                   # stage files for commit
git commit -m "Message"     #commit the changes
git push                    # push changes upstream

# Create a new branch and work on it 
git branch <branch_name>
git checkout <branch_name>
git commit -m "Message"
git push -u origin <branch_name>

```


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
```sh
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
Run backend
```sh
python run.py
```
For now navigate to "127.0.0.1:8000" for a custom 404 error on the frontend, webapp, to configure api next

> The Folder Structure follows the netflix-dispatch fomular for fastapi apps. this is a robust structure that allows for exponential growth of the api without issues.

```sh
tree --dirsfirst -I __pycache__
ENTWENIBOOKING/backend
├── data
│   ├── requirements.txt
│   └── server-config.json
├── src
│   ├── admin
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── utils.py
│   ├── booking
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── decorators.py
│   │   ├── enums.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   └── schemas.py
│   ├── database
│   │   ├── __init__.py
│   │   └── core.py
│   ├── forms
│   │   └── __init__.py
│   ├── notification
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   └── service.py
│   ├── organisation
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── plugin
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   └── service.py
│   ├── plugins
│   │   └── __init__.py
│   ├── product
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── registration
│   │   ├── __init__.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── static
│   │   ├── css
│   │   │   ├── bootstrap.min.css
│   │   │   ├── sign-in.css
│   │   │   └── style.css
│   │   ├── images
│   │   │   ├── entweni-booking.png
│   │   │   └── question-mark-leaves.jpg
│   │   ├── js
│   │   │   └── bootstrap.min.js
│   │   ├── public
│   │   │   └── robots.txt
│   │   └── templates
│   │       ├── auth
│   │       │   ├── login.html
│   │       │   ├── me.html
│   │       │   └── signup.html
│   │       ├── booking
│   │       │   ├── create.html
│   │       │   ├── detail.html
│   │       │   ├── edit.html
│   │       │   └── list.html
│   │       ├── organisation
│   │       │   ├── create.html
│   │       │   ├── detail.html
│   │       │   ├── edit.html
│   │       │   └── list.html
│   │       ├── product
│   │       │   ├── create.html
│   │       │   ├── detail.html
│   │       │   ├── edit.html
│   │       │   └── list.html
│   │       ├── 404.html
│   │       ├── 500.html
│   │       ├── base.html
│   │       ├── home.html
│   │       └── index.html
│   ├── __init__.py
│   ├── api.py
│   └── main.py
├── tests
└── run.py
```

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

On production we will be using Nginx Unit

1. Json Configuaration

```json
{
    "listeners": {
        "*:80": {
            "pass": "applications/eNtweniBooking"
        }
    },
    "applications": {
        "eNtweniBooking": {
            "type": "python3",
            "path": "/app",
            "home": "/media/serpent99/Code/Python/APIs/eNtweniBooking/backend",
            "module": "api",
            "callable": "app"
        }
    }
    
}
```

2. start the server

```sh
sudo unitd
```

3. Give unit access to the folder

```sh
sudo chown unit:unit .
```

3. Push the config to the server

```sh
sudo curl -X PUT --data-binary @server-config.json --unix-socket /var/run/control.unit.sock http://localhost/config
```

4. If pushing fails, get the current config with

```sh
sudo curl -X GET --data-binary @server-config.json --unix-socket /var/run/control.unit.sock http://localhost/config
```

The backend server will be deployed using `Nginx Unit`, an Nginx server built to deploy multiple web apps on the same server with just different port access.

## `LOGIN WITH GOOGLE SETUP`
1. Login to google Cloud Console
2. Create project `entwenibooking
3. Enable APIs and Services
    i. Select the Google+ API
    ii. Enable it
4. Create OAuth2.0 Credentials
5. Retrieve Client ID and Secret

## `Contributing`

Contributions to the eNtweni Booking API are welcome and will be closely examined by lead devs before integration.
If you cannot contribute with writing code, kindly star the project and your efforts will not be taken for granted.
Thank you for supporting `eNtweni Team`

