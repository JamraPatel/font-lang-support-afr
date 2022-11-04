import os
import subprocess
import glob
import yaml
from pathlib import Path

from shaperglot.languages import Languages
from shaperglot.checker import Checker
from shaperglot.reporter import Result

gflangs = Languages()


with open("./language_tag_data/iso639-3-afr-all.txt", "r") as f2:
    afr_tags = f2.read().splitlines()

output = open("results.txt", "w", encoding="utf8")
results = open("results.yaml", "w", encoding="utf8")
summary = open("summary.csv", "w", encoding="utf8")

isoconv = {
    "aar": "aa",
    "afr": "af",
    "aka": "ak",
    "amh": "am",
    "bam": "bm",
    "ewe": "ee",
    "ful": "ff",
    "hau": "ha",
    "her": "hz",
    "ibo": "ig",
    "kik": "ki",
    "kin": "rw",
    "kon": "kg",
    "kua": "kj",
    "lin": "ln",
    "lub": "lu",
    "lug": "lg",
    "mlg": "mg",
    "nbl": "nr",
    "nde": "nd",
    "ndo": "ng",
    "nya": "ny",
    "orm": "om",
    "run": "rn",
    "sag": "sg",
    "sna": "sn",
    "som": "so",
    "sot": "st",
    "ssw": "ss",
    "swa": "sw",
    "tir": "ti",
    "tsn": "tn",
    "tso": "ts",
    "twi": "tw",
    "ven": "ve",
    "wol": "wo",
    "xho": "xh",
    "yor": "yo",
}


# afr_tags = ["dje", "agq", "ro", "bjp", "bas"]


def summarize(tag, fontname, results):
    for code, failure in results:
        if code == Result.PASS:
            continue
        if "Some base glyphs were missing" in failure:
            details = failure.split(":")
            glyphs = details[1].split(",")
            errcount = str(len(glyphs))
            summary.write(fontname + "," + tag + ",missing base," + errcount + "\n")
        if "Some mark glyphs were missing" in failure:
            details = failure.split(":")
            glyphs = details[1].split(",")
            errcount = str(len(glyphs))
            summary.write(fontname + "," + tag + ",missing mark," + errcount + "\n")
        if (
            "Shaper produced a .notdef" in failure
        ):  # Needs implementation for when shaping succeeds
            summary.write(fontname + "," + tag + ",orphaned marks,1\n")
        if "not known" in failure:
            summary.write(fontname + "," + tag + ",profile missing,1\n")


def main():
    fonts = glob.glob("./fonts/*.ttf")

    tag_results = {}
    new_collection = []
    num_tags = len(afr_tags)
    missing_tags = []

    for font in fonts:
        checker = Checker(font)
        fontname = Path(font).stem
        print(f"analyzing {font}")
        for tag in afr_tags:
            if isoconv.get(tag) is not None:
                item = isoconv.get(tag) + "_Latn"
            else:
                item = tag + "_Latn"
            if item not in gflangs:
                missing_tags.append(item)
                continue

            this_results = checker.check(gflangs[item])
            summarize(item, fontname, this_results)
            tag_results.setdefault(item, {})[fontname] = [
                message for code, message in this_results if code != Result.PASS
            ]

    tag_results["Missing GFLang Data"] = missing_tags
    yaml.safe_dump(tag_results, results, allow_unicode=True, sort_keys=False)


if __name__ == "__main__":
    main()
