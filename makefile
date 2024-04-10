
TARGETS=initprod initfrontenddev inibackendev deploy run frontend backend test tests cleantest inittests refresh logs clean
BUILD_CMD=docker compose build --no-cache
UP_CMD=docker compose up --build -d
DOWN_CMD=docker compose down --remove-orphans
LOGS_CMD=docker compose logs -f
BACKUPDB_CMD=cp -R ../../prod/world-prod/app/dbbackups/ ../../backups/
BACKUPIMAGES_CMD=cp -R ../../prod/world-prod/static/images ../../backups/
APPCONTAINERS=$$(sudo docker ps --filter "name=${APP_NAME}" -q)

# **Use .ONESHELL**: By default, each line in a makefile is run in a separate shell. This can cause problems if you're trying to do something like change the current directory. You can use the `.ONESHELL:` directive to run all the commands in a target in the same shell.

.PHONY: $(TARGETS)

# # Check if the config file exists - XXX: don't know which .env file to use yet
# ifeq (,$(wildcard .env))
# $(error The file $(CONFIG_FILE) does not exist)
# endif

include .env
export
###### PROD #######

deploy: refresh run

run: initprod
	$(UP_CMD)
	docker compose stop db-express
	$(LOGS_CMD)

db:
	docker compose up -d db-express
	$(LOGS_CMD)

initprod:
	$(BACKUPDB_CMD)
	$(BACKUPIMAGES_CMD)
	cp -rf envs/prod/.env ./
	cp -rf envs/prod/docker-compose.yml ./
	cp -rf envs/prod/gunicorn.conf.py ./vendor
###### Front End DEV #######
	
frontend: initfrontenddev 
	$(UP_CMD)
	$(LOGS_CMD)

initfrontenddev:
	cp -rf envs/frontenddev/.env ./
	cp -rf envs/frontenddev/docker-compose.yml ./
	cp -rf envs/frontenddev/gunicorn.conf.py ./vendor

###### Back End DEV #######

backend: initbackenddev 
	$(UP_CMD)
	$(LOGS_CMD)

initbackenddev:
	cp -rf envs/backenddev/.env ./
	cp -rf envs/backenddev/docker-compose.yml ./
	cp -rf envs/backenddev/gunicorn.conf.py ./vendor

###### TESTING #######

cleantests: refresh tests 

tests: inittests
	$(UP_CMD)
	docker exec -it $(APP_NAME) python -m pytest #--pdb

RUNTEST?=TestAIIntegration
test: inittests
	$(UP_CMD)
	docker exec -it $(APP_NAME) python -m pytest -k $(RUNTEST) #--pdb

inittests:
	cp -rf envs/testing/.env ./
	cp -rf envs/testing/docker-compose.yml ./
	cp -rf envs/testing/gunicorn.conf.py ./vendor
	cd /root/dev/testdb && docker compose up -d

###### UTILITY #######

clean:
	sudo docker ps -a
	-$(DOWN_CMD)
	-sudo docker kill $(APPCONTAINERS)

refresh: clean
	$(BUILD_CMD)
	$(UP_CMD)

logs:
	$(LOGS_CMD)