import os
import subprocess
import glob
from unittest import result
import yaml
from gflanguages import LoadLanguages, LoadScripts
from google.protobuf.json_format import MessageToDict

gflangs = LoadLanguages()
gfscripts = LoadScripts()
#import yaml_to_table


with open('./language_tag_data/iso639-3-afr-all.txt', 'r') as f2:
    afr_tags = f2.read().splitlines()

output = open("results.txt", "w", encoding='utf8')
results = open("results.yaml", "w", encoding='utf8')
summary = open("summary.csv", "w", encoding='utf8')

isoconv = {"aar": "aa", "afr": "af", "aka": "ak", "amh": "am", "bam": "bm", "ewe": "ee", "ful": "ff", "hau": "ha", "her": "hz", "ibo": "ig", "kik": "ki", "kin": "rw", "kon": "kg", "kua": "kj", "lin": "ln", "lub": "lu", "lug": "lg", "mlg": "mg", "nbl": "nr", "nde": "nd", "ndo": "ng", "nya": "ny", "orm": "om", "run": "rn", "sag": "sg", "sna": "sn", "som": "so", "sot": "st", "ssw": "ss", "swa": "sw", "tir": "ti", "tsn": "tn", "tso": "ts", "twi": "tw", "ven": "ve", "wol": "wo", "xho": "xh": "yor": "yo"}


#afr_tags = ["dje", "agq", "ro", "bjp", "bas"]


def collect(fontname, out):
    collected = {}
    outstring = str(out)
    if("Font supports language" in outstring):
        collected = {fontname: {"status": "pass"}}
    else:
        collected = {fontname: {"status": "fail"}}
        failures = outstring.split("\n")
        for failure in failures:
            if "Some base glyphs were missing" in failure:
                details = failure.split(":")
                collected[fontname]["missing bases"] = details[1].replace(',', '').strip(' ')
            if "Some mark glyphs were missing" in failure:
                details = failure.split(":")
                detailsclean = details[1].replace(',', '').strip(' ')
                collected[fontname]["missing marks"] = detailsclean
            if "Shaper produced a .notdef" in failure:
                collected[fontname]["orphaned marks"] = "See Missing Bases/Marks"
            if "not known" in failure:
                collected[fontname]["gflang"] = "No GFLang profile"

    return(collected)

    
def summarize(tag, fontname, out):
    outstring = str(out)
    failures = outstring.split("\n")
    for failure in failures:
        if "Some base glyphs were missing" in failure:
            details = failure.split(":")
            glyphs = details[1].split(',')
            errcount = str(len(glyphs))
            summary.write(fontname+","+tag+",missing base,"+errcount+"\n")
        if "Some mark glyphs were missing" in failure:
            details = failure.split(":")
            glyphs = details[1].split(',')
            errcount = str(len(glyphs))
            summary.write(fontname+","+tag+",missing mark,"+errcount+"\n")
        if "Shaper produced a .notdef" in failure: # Needs implementation for when shaping succeeds
            summary.write(fontname+","+tag+",orphaned marks,1\n")
        if "not known" in failure:
            summary.write(fontname+","+tag+",profile missing,1\n")

        



def main():
    fonts = (glob.glob("./fonts/*.ttf"))

    tag_results = {}
    new_collection = []
    num_tags = len(afr_tags)
    missing_tags = []



    for tag in afr_tags:
        tag_index = afr_tags.index(tag)
        percent = (tag_index + 1)/num_tags * 100
        formatpercent = "{:.2f}".format(percent)
        item = ""
        if isoconv.get(tag) is not None:
            item =  isoconv.get(tag)+"_Latn"
        else:
            item = tag+"_Latn"
        output.write(item+"\n")
        new_collection = []
        print("analyzing: " + item + " - " + str(formatpercent) + "\u0025 complete")

        if item in gflangs:
            record = MessageToDict(gflangs[item])
            for font in fonts:
                fontname = font.split("/").pop()
                output.write(fontname+"\n")
                arg1 = "check"
                arg2 = "-v"
                arg3 = font
                arg4 = item
                try:
                    proc = subprocess.Popen(["shaperglot", arg1, arg2, arg3, arg4], stdout=subprocess.PIPE)
                except:
                    continue
                out = proc.stdout.read().decode('utf8').strip('\n')
                output.write(str(out)+"\n")

                new_collection.append(collect(fontname, out))
                summarize(item, fontname, out)

            tag_results[item] = new_collection
        else:
            missing_tags.append(item)

    tag_results["Missing GFLang Data"] =  missing_tags
    output.close
    yaml.safe_dump(tag_results, results, allow_unicode=True, sort_keys=False)
    results.close
    summary.close
    f2.close
if __name__ == '__main__':
    main()
