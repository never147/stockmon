VERSION = $(shell cat .version)

all: venv lint

clean:
	rm -rf venv

venv:
	python3.6 -m venv venv
	venv/bin/pip install -r requirements.txt

lint: venv
	venv/bin/pip install -r requirements_test.txt
	. venv/bin/activate && prospector -DFM

build:
	docker build -t stockmon:$(VERSION) .