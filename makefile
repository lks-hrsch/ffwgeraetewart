install:
	uv sync

run:
	PYTHONPATH=./ uv run ./src/main.py

exe:
	uv run pyinstaller --onefile --windowed --clean src/main.py

lint:
	black .
	isort .
	ruff check .

hooks:
	pre-commit install

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./main.spec
