# api-tools
api-tools


cd api-tools
gunicorn --bind 0.0.0.0:5008 wsgi:app

# Installation

```
git clone https:github.com/spelhate/api-tools
cd api-tools
python3 -m venv .venv
pip install
```

## Configuration

`cp .env.dist .env`

Editer ensuite ce fichier

## dev mode

`flask run`

## production mode

`sudo cp tools-api.service /etc/systemd/system/tools-api.service`

Then edit this file and set the correct USER and PORT

```
sudo mkdir /var/log/api-tools
chown USER /var/log/api-tools
sudo systemctl daemon-reload
sudo systemctl enable api-tools
sudo systemctl start api-tools
```
