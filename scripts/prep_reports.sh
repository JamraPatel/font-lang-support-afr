#!/bin/bash

# batch script to process results from shaperglot for web reporting

python summarize.py -i ./results.json
python coverage-analysis.py
python ottag-analysis.py
gzip ./../docs/data/afr_lang_summary_1.json
gzip ./../docs/data/afr_lang_summary_2.json