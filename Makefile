APP_ROOT=./src

lint:
	black --skip-string-normalization $(APP_ROOT)
	isort $(APP_ROOT)
	flake8 $(APP_ROOT)

build_image:
	docker build -t zara-fetcher:0.1 -f ./deploy/images/app/Dockerfile .

install: build_image
	helm install zara-fetcher ./deploy/zara-fetcher

local_db_access:
	kubectl port-forward --namespace default svc/zara-fetcher-postgresql 25432:5432

uninstall:
	helm uninstall zara-fetcher

upgrade: build_image
	helm upgrade zara-fetcher ./deploy/zara-fetcher

make_migrations:
	export APP_DB_HOST=0.0.0.0 && \
	export APP_DB_PORT=25432 && \
	export APP_DB_NAME=zara && \
	export APP_DB_USER=zara && \
	export APP_DB_PASSWORD=secret2 && \
	cd ./src && alembic revision --autogenerate && cd ..

migrate:
	export APP_DB_HOST=0.0.0.0 && \
	export APP_DB_PORT=25432 && \
	export APP_DB_NAME=zara && \
	export APP_DB_USER=zara && \
	export APP_DB_PASSWORD=secret2 && \
	cd ./src && alembic upgrade head && cd ..