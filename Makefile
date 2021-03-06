.DEFAULT_GOAL := docs

venv:
	if [[ ! -d "venv" ]]; then python -m virtualenv venv; fi

init: venv
	pip install -r requirements.txt
	pip install -e .

tox:
	@# just to document that it is here
	@tox

test:
	# This runs all of the tests with coverage
	python setup.py test

coverage: test
	python -m http.server -d tests/coverage

clean:
	python setup.py clean

wheel: clean
	python setup.py dist

test-publish:
	# https://packaging.python.org/tutorials/packaging-projects/
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish:
	twine upload dist/*

.PHONY: docs
docs:
	@cd docs && $(MAKE) --no-print-directory html
	@echo -e "\033[96m\nBuild successful! Docs URL: file://$(PWD)/docs/_build/html/index.html\033[0m"
