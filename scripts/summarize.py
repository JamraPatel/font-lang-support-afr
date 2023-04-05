import sys
from pathlib import Path
import yaml
import json
import argparse
import copy


#summary = open("afr_lang_summary.json", "w", encoding='utf8')
sliced1 = open("./../data/afr_lang_summary_1.json", "w", encoding='utf8')
sliced2 = open("./../data/afr_lang_summary_2.json", "w", encoding='utf8')

overview = open("./../data/afr_font_overview.json", "w", encoding='utf8')
family_overview = open("./../data/afr_family_overview.json", "w", encoding='utf8')


font_details = []
tag_analysis = []
family_details = []



'''def listToString(inList):
    """ Convert list to String """
    ret = ''
    for line in inList:
        if line:
            ret = ret + line + ' '
    return ret'''


# Compile errors for all languages by font
def load_font_details(font, type, errors):
    if not font_details:
            newrecord = {'font': font, 'mbase': {'count': 0, 'enum': []}, 'mmark': {'count': 0, 'enum': []}, 'omark': {'count': 0, 'enum': []}, 'nvariant': {'count': 0, 'enum': []}, 'mfea': {'count': 0, 'enum': []}, 'msmcap': {'count': 0, 'enum': []}}
            newrecord[type]['enum'] = errors
            font_details.append(newrecord)
    elif font_details:
        fontrecord = [x for x in range(len(font_details)) if font_details[x]['font'] == font]
        if fontrecord:
            category = font_details[fontrecord[0]][type]['enum']
            for error in errors:
                if error not in category:
                    font_details[fontrecord[0]][type]['enum'].append(error)
        else:
            newrecord = {'font': font, 'mbase': {'count': 0, 'enum': []}, 'mmark': {'count': 0, 'enum': []}, 'omark': {'count': 0, 'enum': []}, 'nvariant': {'count': 0, 'enum': []}, 'mfea': {'count': 0, 'enum': []}, 'msmcap': {'count': 0, 'enum': []}}
            newrecord[type]['enum'] = errors
            font_details.append(newrecord)


# Compile errors for all languages by font family
def family_summary(data):
    last_family = ""
    for idf, item in enumerate(data):
        curr_font = item.get('font')
        curr_font_split = str(curr_font).split('-')
        curr_family = curr_font_split[0]
        if last_family == curr_family:
            get_family = {k: v for d in family_details for k, v in d.items()}
            if get_family['mbase'] != item['mbase']:
                list_orig = list(get_family['mbase']['enum'].split(' '))
                list_add = list(item['mbase']['enum'].split(' '))
                for glyph in list_add:
                    if glyph not in list_orig:
                        list_orig.append(glyph)
                get_family['mbase']['enum'] = ' '.join(list_orig)
                get_family['mbase']['count'] = len(list_orig)
            if get_family['mmark'] != item['mmark']:
                list_orig = list(get_family['mmark']['enum'].split(' '))
                list_add = list(item['mmark']['enum'].split(' '))
                for glyph in list_add:
                    if glyph not in list_orig:
                        list_orig.append(glyph)
                get_family['mmark']['enum'] = ' '.join(list_orig)
                get_family['mmark']['count'] = len(list_orig)
            if get_family['omark'] != item['omark']:
                list_orig = list(get_family['omark']['enum'].split(' '))
                list_add = list(item['omark']['enum'].split(' '))
                for glyph in list_add:
                    if glyph not in list_orig:
                        list_orig.append(glyph)
                get_family['omark']['enum'] = ' '.join(list_orig)
                get_family['omark']['count'] = len(list_orig)
            if get_family['nvariant'] != item['nvariant']:
                list_orig = list(get_family['nvariant']['enum'].split(' '))
                list_add = list(item['nvariant']['enum'].split(' '))
                for glyph in list_add:
                    if glyph not in list_orig:
                        list_orig.append(glyph)
                get_family['nvariant']['enum'] = ' '.join(list_orig)
                get_family['nvariant']['count'] = len(list_orig)
            if get_family['mfea'] != item['mfea']:
                list_orig = list(get_family['mfea']['enum'].split(' '))
                list_add = list(item['mfea']['enum'].split(' '))
                for glyph in list_add:
                    if glyph not in list_orig:
                        list_orig.append(glyph)
                get_family['mfea']['enum'] = ' '.join(list_orig)
                get_family['mfea']['count'] = len(list_orig)
            if get_family['msmcap'] != item['msmcap']:
                list_orig = list(get_family['msmcap']['enum'].split(' '))
                list_add = list(item['msmcap']['enum'].split(' '))
                for glyph in list_add:
                    if glyph not in list_orig:
                        list_orig.append(glyph)
                get_family['msmcap']['enum'] = ' '.join(list_orig)
                get_family['msmcap']['count'] = len(list_orig)
        else:
            family = item
            family['font'] = curr_family
            family_details.append(item)
        last_family = curr_family


# Update error counts for the aggregated font errors. Includes experimental scoring system to set priorities. This is not currently implemented in the report.
def tally_details(data):
    score = 0
    for idf, font in enumerate(data):
        count = len(font['mbase']['enum'])
        score = count * 4
        font_details[idf]['mbase']['count'] = count
        font_details[idf]['mbase']['enum'] = ' '.join(font['mbase']['enum'])
        count = len(font['mmark']['enum'])
        score = score + count * 4
        font_details[idf]['mmark']['count'] = count
        font_details[idf]['mmark']['enum'] = ' '.join(font['mmark']['enum'])
        count = len(font['omark']['enum'])
        score = score + count * 1
        font_details[idf]['omark']['count'] = count
        font_details[idf]['omark']['enum'] = ' '.join(font['omark']['enum'])
        count = len(font['nvariant']['enum'])
        score = score + count * 3
        font_details[idf]['nvariant']['count'] = count
        font_details[idf]['nvariant']['enum'] = ' '.join(font['nvariant']['enum'])
        count = len(font['mfea']['enum'])
        score = score + count * 1
        font_details[idf]['mfea']['count'] = count
        font_details[idf]['mfea']['enum'] = ' '.join(font['mfea']['enum'])
        count = len(font['msmcap']['enum'])
        score = score + count * 5
        font_details[idf]['msmcap']['count'] = count
        font_details[idf]['msmcap']['enum'] = ' '.join(font['msmcap']['enum'])
    
        font_details[idf]['weight'] = score


'''def tag_coverage():
    all_mbase = set([x['mbase']['enum'] for x in font_details])
    unique_mbase = set([j for i in all_mbase for j in i])'''


# Convert long form shaperglot errors into reporting categories  
def format_errors(lang, font, failures):
    collected = {"tag": lang, "font": font, "mbase": {"count": 0, "enum": ""},  "mmark": {"count": 0, "enum": ""}, "omark": {"count": 0, "enum": ""}, "nvariant": {"count": 0, "enum": ""}, "mfea": {"count": 0, "enum": ""}, "msmcap": {"count": 0, "enum": ""}}
    omarks = {"count": 0, "enum": ''}
    nvariants = {"count": 0, "enum": ''}
    mfeas = {"count": 0, "enum": ''}
    msmcaps = {"count": 0, "enum": ''}
   

    for failure in failures:

        if "Some base glyphs were missing" in failure:
            details = failure.split(":")
            details_string = details[1].replace(',', '').strip(' ')
            collected["mbase"] = {"count": (len(details_string) - details_string.count(' ')), "enum": details_string}
            errors = details_string.split(' ')
            load_font_details(font, 'mbase', errors)
        elif "Some mark glyphs were missing" in failure:
            details = failure.split(":")
            details_clean = details[1].replace(',', '').strip(' ')
            collected["mmark"] = {"count": (len(details_clean) - details_clean.count(' ') - details_clean.count('◌')), "enum": details_clean}
            errors = details_clean.split(' ')
            load_font_details(font, 'mmark', errors)
        elif "Shaper produced a .notdef" in failure:
            collected["omark"] = {"count": 1, "enum": "*see missing bases/marks*"} 
            load_font_details(font, 'omark', ["*see missing bases/marks*"])
        elif "Shaper didn't attach" in failure:
            details = failure.split("Shaper didn't attach ")
            formatted_detail = f"({details[1]})"
            count = omarks["count"] + 1
            enum = omarks["enum"]
            enum += formatted_detail
            omarks.update({"count": count, "enum": enum})
            load_font_details(font, 'omark', [formatted_detail])
        elif "No variant glyphs were found" in failure:
            details = failure.split("No variant glyphs were found for ")
            if details[1] == ".notdef":
                nvariants.update({"count": 1, "enum": "*see notes on glyph variants*"})
                load_font_details(font, 'nvariant', ["*see notes on glyph variants*"])
            else:
                formatted_detail = f"({details[1]})"
                count = nvariants["count"] + 1
                enum = nvariants["enum"]
                enum += formatted_detail
                nvariants.update({"count": 1, "enum": enum})
                load_font_details(font, 'nvariant', [formatted_detail])
        elif "Requires Small-cap" in failure:
            details = failure.split(";")
            formatted_detail = f"({details[0][-1]})"
            count = msmcaps["count"] + 1
            enum = msmcaps["enum"]
            enum += formatted_detail
            msmcaps.update({"count": 1, "enum": enum})
            load_font_details(font, 'msmcap', [formatted_detail])
        elif "The locl feature did not affect" in failure:
            details = failure.split("The locl feature did not affect ")
            formatted_detail = f"({details[1]})"
            count = mfeas["count"] + 1
            enum = mfeas["enum"]
            enum += formatted_detail
            mfeas.update({"count": 1, "enum": enum})
            load_font_details(font, 'mfea', [formatted_detail])
        elif "No exemplar glyphs were defined" in failure:
            continue


    if omarks["count"] != 0:
        collected["omark"] = omarks
    if nvariants["count"] != 0:
        collected["nvariant"] = nvariants
    if msmcaps["count"] != 0:
        collected["msmcap"] = msmcaps
    if mfeas["count"] != 0:
        collected["mfea"] = mfeas

    #collected["weight"] = collected['mbase']['count'] * 4 + collected['mmark']['count'] * 4 + collected['omark']['count'] * 1  + collected['nvariant']['count'] * 3  + collected['mfea']['count'] * 1  + collected['msmcap']['count'] * 5

    return(collected)


# generate summary files for reporting tool
def lang_summary(results):
    tag_data = []
    for lang in results:
        if lang != 'Missing GFLang Data':
            fonts = results.get(lang)
            for font in fonts.items():
                errors = font[1]
                formatted_err = format_errors(lang, font[0], errors)
                tag_data.append(formatted_err)
   
    keyList1 = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    keyList2 = ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


    h1_fonts = [d for d in tag_data if d['font'][0] in keyList1]
    json.dump(h1_fonts, sliced1, indent=1)

    h2_fonts = [d for d in tag_data if d['font'][0] in keyList2]
    json.dump(h2_fonts, sliced2, indent=1)


    #json.dump(tag_data, summary, indent = 1)
    tally_details(font_details)
    data_temp = copy.deepcopy(font_details)
    family_summary(data_temp)

    json.dump(font_details, overview, indent = 1)
    json.dump(family_details, family_overview, indent=1)

    

def main(results):
    print("processing . . .")
    lang_summary(results)

    sliced1.close()
    sliced2.close()

    #summary.close()
    overview.close()
    family_overview.close()
    print("Summary files have been generated")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='infile', help='shaperglot results.yaml input file', required='True')
    args = parser.parse_args()
    in_file = Path(args.infile)
    if not in_file.is_file():
        sys.exit("Input file [" + args.infile + "] does not exists")
    with open(args.infile, 'r') as file:
        results = json.load(file)
        main(results)
    file.close()
