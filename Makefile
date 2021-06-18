TEST_MOD = pytest
TEST_OPT = --hypothesis-show-statistics

init:
	pip install -r requirements.txt

test:
	$(TEST_MOD) $(TEST_OPT)

.PHONY: init test
