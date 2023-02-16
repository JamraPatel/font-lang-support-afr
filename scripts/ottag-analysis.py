import yaml
from gflanguages import LoadLanguages, LoadScripts
from google.protobuf.json_format import MessageToDict

gflangs = LoadLanguages()


isoconv = {"aar": "aa", "afr": "af", "aka": "ak", "amh": "am", "bam": "bm", "ewe": "ee", "ful": "ff", "hau": "ha", "her": "hz", "ibo": "ig", "kik": "ki", "kin": "rw", "kon": "kg", "kua": "kj", "lin": "ln", "lub": "lu", "lug": "lg", "mlg": "mg", "nbl": "nr", "nde": "nd", "ndo": "ng", "nya": "ny", "orm": "om", "run": "rn", "sag": "sg", "sna": "sn", "som": "so", "sot": "st", "ssw": "ss", "swa": "sw", "tir": "ti", "tsn": "tn", "tso": "ts", "twi": "tw", "ven": "ve", "wol": "wo", "xho": "xh", "yor": "yo"}
with open('./../language_tag_data/iso639-3-afr-all.txt', 'r') as f2:
    afr_tags = f2.read().splitlines() 
with open('./../language_tag_data/ot-lang-tags.yaml', 'r') as f3:
	ot_tags = yaml.safe_load(f3)


# collect exemplar data from gflang profiles 
def collect(lang):
    exemplar_chars = lang.get("exemplarChars", {})
    name = lang.get("name")
    marks = exemplar_chars.get("marks", "").split() or []
    bases = exemplar_chars.get("base", "").split() or []
    auxiliary = exemplar_chars.get("auxiliary", "").split() or []
    return(bases, name)

def main():
    all_ot = []
    required_tags = []

	# Filter OT lang tag list to only African Languages
    for lang in ot_tags:
        for code in lang.get("codes"):
            all_ot.append(code)

	# Look for languages that require an "Eng". Check to see if those languages have a corresponding OT Lang Tag. If not add those languages to the required OT tag list.
    for tag in afr_tags:
        item = ""
        if isoconv.get(tag) is not None:
            item =  isoconv.get(tag)+"_Latn"
        else:
            item = tag+"_Latn"
        if item in gflangs:
            record = MessageToDict(gflangs[item])
            bases, name = collect(record)
            if "Ŋ" in bases:
                if tag not in all_ot:
                    required_tags.append(name + " (" + tag + ")")

    with open("./../docs/data/required_ot_lang_tags.txt", "w") as output:
        for rtag in required_tags:
            output.write('%s\n' % rtag)

if __name__ == '__main__':
    main()