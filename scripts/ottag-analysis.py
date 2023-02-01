from itertools import permutations
import os
from xxlimited import new
import yaml
import sys
import unicodedata
import itertools
import json
from gflanguages import LoadLanguages, LoadScripts
from google.protobuf.json_format import MessageToDict

#gflangs = LoadLanguages()
#gfscripts = LoadScripts()


missingtag = open("missing_ot_tag.json", "w", encoding="utf8")
#coverage = open("glyph_coverage.json", "w", encoding='utf8')

#isoconv = {"aar": "aa", "afr": "af", "aka": "ak", "amh": "am", "bam": "bm", "ewe": "ee", "ful": "ff", "hau": "ha", "her": "hz", "ibo": "ig", "kik": "ki", "kin": "rw", "kon": "kg", "kua": "kj", "lin": "ln", "lub": "lu", "lug": "lg", "mlg": "mg", "nbl": "nr", "nde": "nd", "ndo": "ng", "nya": "ny", "orm": "om", "run": "rn", "sag": "sg", "sna": "sn", "som": "so", "sot": "st", "ssw": "ss", "swa": "sw", "tir": "ti", "tsn": "tn", "tso": "ts", "twi": "tw", "ven": "ve", "wol": "wo", "xho": "xh", "yor": "yo"}
with open('./language_tag_data/iso639-3-afr-all.txt', 'r') as f2:
    afr_tags = f2.read().splitlines() 
with open('.language_tag_data/ot-lang-tags.yaml', 'r') as f3:
	ot_tags = yaml.safe_load(f3)


def collect(lang):
    exemplar_chars = lang.get("exemplarChars", {})
    marks = exemplar_chars.get("marks", "").split() or []
    bases = exemplar_chars.get("base", "").split() or []
    auxiliary = exemplar_chars.get("auxiliary", "").split() or []
    return(bases, auxiliary, marks)

def main():

	missing_tags = []
	# operation search for ot lang tags in all afr tags. Dump report of missing tags
	for code in ot_tags(""):
		if ot_tags.get(tag) is None:
			missing_tags.append(tag)
		
	
	///
    all_bases = []
    all_marks = []
    all_pairs = []
    record = {}
    total_tags = 0
    avail_tags = []
    base_coverage = []
    mark_coverage = []
    pair_coverage = []


    for tag in afr_tags:
        item = ""
        if isoconv.get(tag) is not None:
            item =  isoconv.get(tag)+"_Latn"
        else:
            item = tag+"_Latn"
        if item in gflangs:
            total_tags = total_tags + 1
            avail_tags.append(item)
            record = MessageToDict(gflangs[item])
            bases, auxiliary, marks = collect(record)
            for base in bases:
                if base not in all_bases and len(base) == 1:
                    all_bases.append(base)
                elif base not in all_bases and len(base) > 1:
                    all_pairs.append(base)
            for aux in auxiliary:
                if aux not in all_bases and len(aux) == 1:
                    all_bases.append(aux)
                elif aux not in all_bases and len(aux) > 1:
                    all_pairs.append(aux)
            for mark in marks:
                if mark not in all_marks:
                    all_marks.append(mark)


    for glyph in all_bases:
        tags_for_base = []
        for tag in avail_tags:
            record = MessageToDict(gflangs[tag])
            bases, auxiliary, marks = collect(record)
            if glyph in bases or glyph in auxiliary:
                tags_for_base.append(tag)
        base_coverage.append(tags_for_base)

    for glyph in all_marks:
        tags_for_mark = []
        for tag in avail_tags:
            record = MessageToDict(gflangs[tag])
            bases, auxiliary, marks = collect(record)
            if glyph in marks:
                tags_for_mark.append(tag)
        mark_coverage.append(tags_for_mark)

    for glyph in all_pairs:
        tags_for_pair = []
        for tag in avail_tags:
            record = MessageToDict(gflangs[tag])
            bases, auxiliary, marks = collect(record)
            if glyph in bases or glyph in auxiliary:
                tags_for_pair.append(tag)
        pair_coverage.append(tags_for_pair)

    base_analysis = [dict(zip(all_bases, base_coverage))]
    mark_analysis = [dict(zip(all_marks, mark_coverage))]
    pair_analysis = [dict(zip(all_pairs, pair_coverage))]

    #print(total_tags)
    #print(all_bases)
    #print(all_marks)
    #print(avail_tags)
    #print(base_analysis)
    print(pair_analysis)
    ///

    json.dump([all_bases, all_marks], glyphset, indent=1)
    json.dump([total_tags, base_analysis, mark_analysis, pair_analysis], coverage, indent=1)

if __name__ == '__main__':
    main()