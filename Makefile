TEST_MOD = pytest

init:
	pip install -r requirements.txt

test:
	$(TEST_MOD)

.PHONY: init test
