# api-tools
api-tools


cd api-tools
gunicorn --bind 0.0.0.0:5008 wsgi:app

# Installation

```
git clone https:github.com/spelhate/api-tools
cd api-tools
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

`cp .env.dist .env`

Editer ensuite ce fichier

## dev mode

`flask run`

## production mode

`sudo cp api-tools.service /etc/systemd/system/api-tools.service`

Then edit this file and set the correct USER and PORT

```
sudo mkdir /var/log/api-tools
chown USER /var/log/api-tools
sudo systemctl daemon-reload
sudo systemctl enable api-tools
sudo systemctl start api-tools
sudo cp nginx.conf /etc/nginx/applications/api-tools.conf
sudo systemctl reload nginx
```
