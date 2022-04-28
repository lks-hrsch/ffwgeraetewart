install:
	pip install -r requirements.txt

run:
	python src/main.py

exe:
	pyinstaller --onefile --windowed --clean src/main.py
	
lint:
	black .
	isort .
