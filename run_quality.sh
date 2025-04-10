#!/bin/bash
black --required-version 23 --check src examples benchmarks utils
ruff check src examples benchmarks utils
doc-builder style src/accelerate docs/source --max_len 119 --check_only