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
	python setup.py register -r pypitest
	python setup.py bdist_wheel upload -r pypitest

publish:
	python setup.py register
	python setup.py bdist_wheel upload

.PHONY: docs
docs:
	@cd docs && $(MAKE) --no-print-directory html
	@echo -e "\033[96m\nBuild successful! Docs URL: file://$(PWD)/docs/_build/html/index.html\033[0m"
