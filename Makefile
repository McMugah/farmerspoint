install:
	pip install -r requirements.txt
format:
	black ./app
test:
	pytest ./app
lint:
	pylint  ./app
sort:
	isort ./app
run:
	python3 run.py
security:
	bandit ./app