Documentation is a work in progress  


# font-lang-support-afr
This repository is a toolkit to visualize how well a font library supports African languages. font-lang-support-afr consists of a set of scripts to process the raw results from [shaperglot](https://github.com/googlefonts/shaperglot) and [gflanguages](https://github.com/googlefonts/lang) in order to create a web-based report that makes it easier to analyze the results and set priorities for improving African language support. The charts in the web report are created using [chart.js](https://www.chartjs.org/). This toolkit was primarily developed to evaluate the Google Fonts library, but can be adapted to report on any font library. The repository 

The assessment of the Google Fonts library is accessible via https://JamraPatel.github.io/font-lang-support-afr, which is hosted on the `report` branch of this repository. Documentation on how to use the web report is on the website.

# Usage
Assessing how well a font supports a given language requires not only looking to see if the necessary glyphs are included in the font but also making sure that everything is shaped properly. To assess this, we use shaperglot. While shaperglot can be run on a single font what we are interested in her is running the analysis on an entire font library against all known African language tags. This is accomplished by using the 'bulk-sg-run.py' script located in the script folder of the shaperglot repository. The following instructions are for those who are updating the Google Fonts web report. To assess a different font library, follow the same instructions without making any commits to this repo.

1. Run 'bulk-sg-run.py' on a font library directory.
```
$ bulk-sg-run.py ./path-to-font-library
```
Output
```
results.json
afr_tag_overview.json
```
2. Clone the font-lang-support-afr repository. Fork the repository if you are trying to assess a font library other than Google Fonts.

3. Create a new branch based on `report`. 

4. Copy `afr_tag_overview.json` to the `./docs/data/` directory where you have installed font-lang-support-afr 

5. Copy `results.json` to the `./scripts/` directory font-lang-support-afr 

6. Run the `prep_reports.sh` shell script
```
$ ./prep_reports.sh
processing . . .
Summary files have been generated
```
Output:
```
./docs/data/afr_family_overview.json
./docs/data/afr_font_overview.json
./docs/data/afr_lang_summary_1.json.gz
./docs/data/afr_lang_summary_2.json.jz
./docs/data/glyph_coverage.json
./docs/data/glyph_set.json
./docs/data/required_ot_lang_tags.txt
```

7. Test the results with a local webserver.
```
$ cd ./docs
$ python -m http.server 8000
```
Open a browser tab go to [http://localhost:8000/index.html](http://localhost:8000/index.html)

8. If all of the reports look like they are working properly, delete the `results.json` file and submit PR to update the report.


## Overview of Scripts and Data 
# Scripts
`summarize.py` is a script that process raw shaperglot results into a handful of reports. These include a family level summary, a font level summary, and splits the language tag results into two files.

`prep_reports.sh` is a shell script that runs `summarize.py`, `coverage-analysis.py`, `ottag-analysis.py` and zips the language tag result files and places everything in the appropriate directory.

# Data Sets
iso639-3-afr-all.txt which contains all language tags for African Languages irrespective of script. 

ot-lang-tags.yaml is a database of available OpenType language tags for African languages. The data is sourced from [Microsoft Typography](https://learn.microsoft.com/en-us/typography/opentype/spec/languagetags)


# Setup
## Requirements
* Python 3.9+
* [gflanguages](https://github.com/googlefonts/lang) <- If you installed shaperglot gflanguages will have been installed already.
