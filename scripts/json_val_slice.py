import sys
from pathlib import Path
import yaml
import json
import argparse


sliced1 = open("afr_lang_summary_1.json", "w", encoding='utf8')
sliced2 = open("afr_lang_summary_2.json", "w", encoding='utf8')
#sliced3 = open("afr_lang_summary_3.json", "w", encoding='utf8')


def validateJSON(data):
        try:
            results = json.load(data)
        except ValueError as err:
            return False
        return True


def main(results):
        #test = validateJSON(data)
    #print(test)
    
    print(len(results)) 
    keyList1 = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    keyList2 = ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    keyList3 = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']


    h1_fonts = [d for d in results if d['font'][0] in keyList1]
    json.dump(h1_fonts, sliced1, indent=1)

    h2_fonts = [d for d in results if d['font'][0] in keyList2]
    json.dump(h2_fonts, sliced2, indent=1)


    #h3_fonts = [d for d in results if d['font'][0] in keyList3]
    #json.dump(h3_fonts, sliced3, indent=1)

    #print(b_fonts)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='infile', help='shaperglot results.yaml input file', required='True')
    args = parser.parse_args()
    in_file = Path(args.infile)
    if not in_file.is_file():
        sys.exit("Input file [" + args.infile + "] does not exists")
    with open(args.infile, 'r') as file:
        #results = yaml.safe_load(file)
        results = json.load(file)
        main(results)
    file.close()


