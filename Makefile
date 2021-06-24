TEST_MOD = pytest
TEST_OPT = -s

init:
	pip install -r requirements.txt

test:
	$(TEST_MOD) $(TEST_OPT)

.PHONY: init test
