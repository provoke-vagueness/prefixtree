SHELL := /bin/bash

deps:
	pip install --upgrade --use-mirrors \
	            -r requirements/development.txt \
	            -r requirements/testing.txt \
	            -r requirements/production.txt

build:
	python setup.py build

sdist: build
	python setup.py sdist

register:
	python setup.py register

site:
	cd docs; make html

test: build
	coverage run setup.py test

unittest: build
	coverage run -m unittest discover

lint:
	flake8 --exit-zero prefixtree tests

coverage:
	coverage report --show-missing --include="prefixtree*"

performance:
	PYTHONPATH=. python tests/test_performance.py

clean:
	python setup.py clean --all
	find . -type f -name "*.pyc" -exec rm '{}' +
	find . -type d -name "__pycache__" -exec rmdir '{}' +
	rm -rf *.egg-info .coverage
	cd docs; make clean

docs: site

.PHONY: deps build sdist register site test unittest lint coverage clean docs
