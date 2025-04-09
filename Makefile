.PHONY: run install clean

install:
	pip install -r requirements.txt

run:
	python -m RSUHelper.gui.main_gui

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
