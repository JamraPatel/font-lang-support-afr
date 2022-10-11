# font-lang-support-afr
 Toolkit to assist in evaluating African language support in fonts. Makes use of Hyperglot and Shaperglot.

Scripts are still being developed.

## extract-hg-chardata.py
This script to extract character data from Hyperglot language profiles.
```
python extract-hg-chardata.py -h
usage: extract-hg-chardata.py [-h] [-r] [script]

positional arguments:
  script      No argument for all scripts. Options: Arabic, Ge\'ez/Fidel, Latin

optional arguments:
  -h, --help  show this help message and exit
  -r          Change output format to reporting structure
```
 
## subset-hyperglot.py
This script to generate a subsetted Hyperglot YAML file with a susbset of languages
 
 Planned updates:
 - Import language tags from file
 - Add arguments to filter script
 
 This script may be unnecessary in the long run.
 
## generate-sg-profile.py
This script simplifies generating shaperglot language profiles. Test data is input via a data file with simple strings containing the test parameters for any given type of test. generate-sg-profile.py automatically constructs a compatible shaperglot profile for the provided languages.

Example test strings:
```
acz|features|mark|involves|hyperglot
acz|features|smcp|present|
acz|languagesystems|arab|
ajg|features|mark|involves|hyperglot
ajg|languagesystems|latn|dflt
ajg|languagesystems|latn|YOR 
ajg|mark2base|Á|
ajg|mark2base|Á|smcp
```


 ```
 usage: generate-sg-profile.py [-h] -i INFILE

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --input INFILE
                        .csv input file
```
 
Language Tag Sets will contain different groups of Language Tags. Currently it only includes iso639-3-afr-all.txt which contains all language tags for African Languages irrespective of script.



# Requirements
* Python 3.8+
* pyyaml
