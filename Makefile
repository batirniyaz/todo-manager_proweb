.PHONY: build down run start

build:
	docker-compose build

run:
	docker-compose up -d

down:
	docker-compose down

start: build run