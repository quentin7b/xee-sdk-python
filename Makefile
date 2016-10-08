.PHONY: init lint test coverage

install:
	pip install -r requirements.txt

lint:
	pylint xee --output-format=html > lint.html || true
	open lint.html

test:
	pip install -r test/requirements.txt
	python -m unittest test.test_sdk

coverage:
	pip install -r test/requirements.txt
	coverage run --source ./xee/  -m unittest test.test_sdk
	coverage report -m
	coverage html
	open htmlcov/index.html

coverage_ci:
	pip install -r test/requirements.txt
	coverage run --source ./xee/  -m unittest test.test_sdk
	coverage report -m

clean:
	coverage erase
	rm lint.html || true
	rm -rf htmlcov
	rm coverage.xml
	rm -rf **/**.pyc