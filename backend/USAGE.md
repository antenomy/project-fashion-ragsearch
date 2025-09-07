# USAGE

### Backend
source venv/bin/activate

To start backend, navigate to root directory and run:
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
or
uvicorn backend.main:app --reload
or 
uvicorn backend.main:app

close: CTRL + C


alternatively outside uvicorn: python -m backend.main

### Database (on HM Mac)
run postgres in daemon:
pg_ctl -D /opt/homebrew/var/postgres start

stop daemon:
pg_ctl -D /opt/homebrew/var/postgres stop

start verbose:
postgres -D /opt/homebrew/var/postgres
close: CTRL + C

to get local ip:
ipconfig getifaddr en0



### setting up sql database

install pgvector on computer and pip install in venv


create database
CREATE DATABASE project_db;

enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

## Running files in backend

python -m backend.FILENAME


### Testing

Testing phrases:
I am going to the pool later and looking for swimming trunks and for sunglasses to wear while going. Also a top, preferablyfor going to the beach.

Tomorrow there is a party, I want to find a pair of nice socks, and a casual blazer, and my brother is looking for a pair of grey dresspants.

I am looking for one red and one black shirt to wear under my grey blazer.

I am looking for a t shirt that goes well with some blue jeans and green sneaks.

      {
        "role": "system",
        "content": "You are a helpful clothing store AI assistant that extracts and formats structured product data for a clothing e-commerce catalog."
      },

curl -X POST http://172.16.8.224:8000/recommend_products \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Tomorrow there is a party, I want to find a pair of nice socks, and a casual blazer, and my brother is looking for a pair of grey dresspants."
      }
    ]
  }'



### Nix Host Commands

Start Playwright Shell

ssh ssh.lucasgrant.com

sudo systemctl stop greetd

cd /home/antenomy/git/work-hm-project/

nix shell github:pietdevries94/playwright-web-flake#playwright-test

Test: echo $PATH

nix-shell

source backend/.env/bin/activate

pip install -r backend/requirements.txt
