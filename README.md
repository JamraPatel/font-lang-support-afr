# font-lang-support-afr
 Toolkit to assist in evaluating African language support in fonts. Makes use of Hyperglot and Shaperglot.

Scripts are still being developed.

extract-hg-chardata.py is a script to extract character data from Hyperglot language profiles.
```
python extract-hg-chardata.py -h
usage: extract-hg-chardata.py [-h] [-r] [script]

positional arguments:
  script      No argument for all scripts. Options: Arabic, Ge\'ez/Fidel, Latin

optional arguments:
  -h, --help  show this help message and exit
  -r          Change output format to reporting structure
```

Planned updates:
 - Import language tags from file
 - Change script selector to OpenType language tag format
 
 
 subset-hyperglot.py is a script to generate a subsetted Hyperglot YAML file with a susbset of languages
 
 Planned updates:
 - Import language tags from file
 - Add arguments to filter script
 
 
 Under development:
  - Create script to create a template shaperglot profile using available data from Hyperglot. e.g. Create all mark attachment tests and language tag tests from known info in Hyperglot.
