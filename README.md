# How to run
## Run docker compose
```
docker-compose -f docker-compose.yml up --build
```
## Add new dependency
### Go to container 
```
sudo docker exec -it system-recommendation-system-recommendation-1 pip install python-dotenv
```
### Add dependency to requirements.txt
```
pip freeze > requirements.txt
```