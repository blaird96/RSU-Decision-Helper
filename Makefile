.PHONY: run install clean

install:
	pip install -r requirements.txt

run:
	python -m RSUHelper

gui:
	python -m RSUHelper --gui

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
