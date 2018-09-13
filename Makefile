.DEFAULT_GOAL := docs

init:
	pip install -r requirements.txt

tox:
	# just to document that it is here
	tox

test:
	# This runs all of the tests with coverage
	python setup.py test

clean:
	python setup.py clean

wheel: clean
	python setup.py bdist_wheel --universal

test-publish:
	python setup.py register -r pypitest
	python setup.py bdist_wheel --universal upload -r pypitest

publish:
	python setup.py register
	python setup.py bdist_wheel --universal upload

.PHONY: docs
docs:
	@cd docs && $(MAKE) --no-print-directory html
	@echo "\033[96m\nBuild successful! Docs URL: file://$(PWD)/docs/_build/html/index.html\033[0m"
