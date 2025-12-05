#!/usr/bin/env bash

set -e


uv sync --extra dev

python -m unittest discover tests/ -v