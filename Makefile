curdir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: prepare

prepare: .venv

.venv:
	/usr/bin/python -m venv .venv
	$(curdir)/.venv/bin/pip install vrchatapi
build:
	$(curdir)/.venv/bin/python merge.py
