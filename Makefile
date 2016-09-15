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
	coverage run -m test.test_sdk discover
	coverage report -m
	coverage html
	open htmlcov/index.html

clean:
	coverage erase
	rm lint.html || true
	rm -rf **/**.pyc
