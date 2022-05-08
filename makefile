install:
	pip install -r requirements.txt

run:
	python src/main.py

exe:
	pyinstaller --onefile --windowed --clean src/main.py

lint:
	black .
	isort .

hooks:
	pre-commit install

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./main.spec
