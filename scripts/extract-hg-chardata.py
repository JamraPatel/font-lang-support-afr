import base64
from pprint import pprint
import yaml, argparse


def load_hg_data():

    #Import static instance of Hyperglot database
    with open('Hyperglot_DEV_09152022.yaml', 'r') as f:
        dataMap = yaml.safe_load(f)
        #pprint(dataMap)

    return dataMap

'''Check Hyperglot for missing language profiles and return list of language tags that have profiles. Tag with missing profiles are dumped into a text file missing_profiles.txt'''
def sortProfiles(lang_tags, dataMap):
    #Create output data files
    missing_profiles = open("missing_profiles.txt", "w")

    profiles_true = []
    count_in = 0
    count_out = 0
    missing_profiles.write("The following language tags don't have a Hyperglot profile:\n")
    for tag in lang_tags:
        count_in += 1
        if not tag in dataMap:
                missing_profiles.write(tag + '\n')
                count_out += 1
        else:
            profiles_true.append(tag)
    missing_profiles.write(str(count_out) + ' of ' + str(count_in) + 'profiles missing')
    missing_profiles.close()
    count_true = count_in - count_out
    return profiles_true, count_true


def extract_data(script, report, lang_tags, dataMap):
    #Create output data files
    out = open("extracted_hyperglot_char_data.tsv", "w")

    '''Loop through hyperglot Keys and find desired language tags. Extracts Language Name, ISO 639 Language Tag, Base, Marks into extracted_hyperglot_char_data.tsv for import into Google Sheets'''
    extract_tags, count_true = sortProfiles(lang_tags, dataMap)

    script_map = {'arab': 'Arabic', 'ethi': 'Ge\'ez/Fidel', 'latn': 'Latin', 'all': 'Arabic, Ge\'ez/Fidel, Latin'}
    hg_script = script_map.get(script)
    
    if report:
        for tag in extract_tags:

            for item in dataMap[tag]['orthographies']:
                if item['script'] in (script):
                    out.write(dataMap[tag]['name'] + '\t')
                    out.write(tag + '\t')
                    if 'base' in item:
                        base_string = item['base']
                        base_tabs = base_string.replace(' ', '\t')
                        out.write(base_tabs + '\t')
                    else:
                        out.write(item['inherit'] +"\t")
                    if 'auxilary' in item:
                        aux_string = item['auxiliary']
                        aux_tabs = aux_string.replace(' ', '\t')
                        out.write(aux_tabs + '\t')
                    else:
                        out.write("\t")
                    if 'marks' in item:
                        marks_string = item['marks']
                        marks_tabs = marks_string.replace(' ', '\t')
                        out.write(marks_tabs + '\n')
                    else:
                        out.write("\n")
                    
        out.close()
    else:
        for tag in extract_tags:

            for item in dataMap[tag]['orthographies']:
                if item['script'] in (script):
                    out.write(dataMap[tag]['name'] + '\n')
                    out.write("Language Tag:\t" + tag + '\n')
                    if 'base' in item:
                        out.write("Base:\t" + item['base'] + '\n')
                    else:
                        out.write("Inherited Base:\t" + item['inherit'] +"\n")
                    if 'auxilary' in item:
                        out.write("Auxiliary:\t" + item['auxiliary'] + '\n')
                    else:
                        out.write("Auxiliary:\t None\n")
                    if 'marks' in item:
                        out.write("Marks:\t" + item['marks'] + '\n\n')
                    else:
                        out.write("Marks:\t None\n\n")
                    
        out.close()
        print('%s data sets extracted for the following Script(s) %s' % (str(count_true), script))



def main(infile, script, report):
    lines = infile
    lang_tags = []
    for l in lines:
        lang_tags.append(l.replace("\n", ""))
    dataMap = load_hg_data()
    extract_data(script, report, lang_tags, dataMap)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Argument to filter retuned items based on writing system
    parser.add_argument('script', help='No argument for all scripts. Options: arab, ethi, latn', nargs='?', default='all')
    # Argument to provide character data in a format for reporting
    parser.add_argument('-r', dest='report', action='store_true', help='Change output format to reporting structure')
    parser.add_argument('-i', '--input', dest='infile', help='Plain text file with line-separated ISO639-3 lang tags', type=argparse.FileType('r'), required='True')
    args = parser.parse_args()
    #print(args.infile.readlines())
    main(args.infile.readlines(), args.script, args.report)
    args.infile.close()
