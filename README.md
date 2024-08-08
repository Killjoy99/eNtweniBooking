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

```ps
    cd frontend/
    python -m venv venv
    .\venv\Scripts\activate.bat # activate the virtual environment
    pip install -r requirements.txt
    python main.py          # run the frontend app
```

## `IMAGES MOBILE`

Welcome: ![text][welcome]

[welcome]: showcase/welcome.png

Welcome: ![text][login]

[login]: showcase/login.png

Welcome: ![text][register]

[register]: showcase/register.png

Home: ![text][home]

[home]: showcase/home.png

## `IMAGES WEB`

Home: ![text][login-web]

[login-web]: showcase/login-web.png

Home: ![text][register-web]

[register-web]: showcase/register-web.png

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

```ps
    cd backend/
    python -m venv backend
    source venv/bin/activate # activate the virtual environment
    pip install -r requirements.txt
    python -m uvicorn main:app --reload          # run the backend app
```

`Bootstrap`

Download bootstrap 5 and extact it to the static folder.
Rename the folder bootstrap

## `Deployment`

## `DEVELOPMENT`

```sh
python run.py
```

## `PRODUCTION`

On production we will be using Nginx Unit

## `Configure Nginx Unit`

1. Create a new service for Nginx Unit

```sh
sudo nano /etc/systemd/system/unit.service
# find running instances of unit
ps aux |grep unitd
# kill the instance that causes problems
sudo kill <pid>
# run a new instance of unit
sudo unitd --control 127.0.0.1:9000 --user unit
```

2. Add the following content to the service file

```ini
[Unit]
Description=Nginx Unit
After=network.target

[Service]
ExecStart=/usr/sbin/unitd --no-daemon
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -QUIT $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Make sure that the ExecStart path matches the location of the unitd executable on your system. If it's different, adjust accordingly.

```sh
which unitd
```

3. Reload systemd to apply the new service file

```sh
sudo systemctl enable unit.service
```

4. Start the Nginx Unit service immediately

```sh
sudo systemctl start unit.service
```

4. Check the status of the service to ensure it's running

```sh
sudo systemctl status unit.service
```

5. Reload and restart the service if failed

```sh
sudo systemctl daemon-reload
sudo systemctl restart unit.service
```

6. Check for Required Directories and Permissions

Ensure that the directories and files required by Nginx Unit have the correct permissions. You might need to adjust the permissions of your application directory to be accessible by the unit user:

```sh
sudo chown -R unit:unit /path/to/your/app
```

7. Check the Configuration

Ensure that your Nginx Unit configuration is correct. Invalid configurations can cause the service to fail. You can test your configuration file before applying it:

```sh
sudo unitd --check
```

`Additional Notes`
If you need to make any changes to the service file, always reload the systemd configuration using sudo systemctl daemon-reload after making changes.
Use sudo systemctl restart unit.service to restart the service if needed.

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
curl -X PUT --data-binary @server-config.json --unix-socket /var/run/control.unit.sock http://localhost/config
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

## `CREATING KEYS`

```sh
# Generate a 2048-bit RSA private key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Extract the public key
openssl rsa -pubout -in private_key.pem -out public_key.pem

```


## `EntweniSDK`

In the frontend a folder for generating methods to call the backend has the code to generate the frontend api, We named the folder entweni_openapi_sdk for covenience.
This code generates methods based o the openapi json schema when the dev server is running.
TODO: updated the entweni_openapi_sdk to also get the models when generating the frontend code for convenience so that we do not send raw json but rather Model data.

## `Contributing`

Contributions to the eNtweni Booking API are welcome and will be closely examined by lead devs before integration.
If you cannot contribute with writing code, kindly star the project and your efforts will not be taken for granted.
Thank you for supporting `eNtweni Team`
