.PHONY: verify falsify ci

PYTHON ?= python3

verify:
	$(PYTHON) verifier/ledger_core_verifier.py verify-all

falsify:
	$(PYTHON) scripts/falsify_ledger.py

ci: verify falsify

