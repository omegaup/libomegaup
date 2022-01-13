.PHONY: test lint pytest mypy validatortest build upload

test: pytest lint mypy validatortest

lint:
	python3 -m flake8 --exclude=.env,.tox,dist,docs,build,*.egg --ignore=E501,W503 .

mypy:
	python3 -m mypy --strict .

pytest:
	python3 -m pytest -xvv

validatortest:
	cd tests && \
	RESULT="$$(PYTHONPATH="${PWD}" python3 validatortest_test.py validatortest)" && \
	if [ "$${RESULT}" -ne 1 ]; then \
		echo "Expected result to be 1, got '$${RESULT}'"; \
		exit 1; \
	fi

.PHONY: docs
docs: $(shell find omegaup -name '*.py')
	python3.9 -m pdoc -o docs/ omegaup/

build: docs
	rm -rf dist/*
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*
