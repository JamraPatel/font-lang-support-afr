import yaml, argparse, unicodedata, os, os.path
from pprint import pprint
from pyexpat import features
from yaml import Loader, Dumper



class Features:
    def __init__(self, feature, test, value):
        self.feature = feature
        self.test = test
        self.value = value
    def construct_involves(self):
        return {self.feature: [{self.test:self.value}]}
    def construct_present(self):
        return {self.feature: [self.test]}

class Languagesystems:
    def __init__(self, script, lang):
        self.script = script
        self.lang = lang
    def construct(self):
        return [self.script, self.lang]

class Inputs1:
    def __init__(self, lang, text, feature, value):
        self.lang = lang
        self.text = text
        self.feature = feature
        self.value = value
    def construct(self):
        if(self.feature and self.value):
            return [{"text":self.text, "language":self.lang,  "features":{self.feature: self.value}}]
        else:
             return [{"text":self.text, "language":self.lang}]
class Inputs2:
    def __init__(self, lang, text1, text2, feature, value):
        self.lang = lang
        self.text1 = text1
        self.text2 = text2
        self.feature = feature
        self.value = value
    def construct(self):
        if(self.feature and self.value):
            return [{"text":self.text2, "language":self.lang, "features":{self.feature: self.value}}, {"text":self.text1 + self.text2, "language":self.lang, "features":{self.feature: self.value}}]
        else:
            return [{"text": self.text2, "language":self.lang}, {"text":self.text1 + self.text2, "language":self.lang}]

class FilterFeature:
    def __init__(self, feature):
        self.feature = feature
    def construct(self):
        return {"feature":self.feature}

class Mark2Base:
    def __init__(self, lang, base, mark):
        self.lang = lang
        self.base = base
        self.mark = mark
    def construct(self):
        return [[0,0],[1,0]]

class Rationale:
    def __init__(self, lang, base, mark, feature, test):
        self.lang = lang
        self.base = base
        self.mark = mark
        self.feature = feature
        self.test = test
    def construct(self):
        feature_desc = {"smcp":"Small caps ", "c2sc":"Small caps ", "init":"Initial ", "medi":"Medial ", "fina":"Final "}
        b = ord(self.base)
        m = ord(self.mark)
        if(self.test == 'mark2base'):
            if(self.feature):
                return str(feature_desc.get(self.feature)) + str(unicodedata.name(self.base)) + " (" + str(format(b, '04x')) + ")" + " needs anchor for combining mark: " + str(unicodedata.name(self.mark)) + " (" + str(format(m, '04x')) + ")"
            else:
                return str(unicodedata.name(self.base)) + " (" + str(format(b, '04x')) + ")" + " needs anchor for: " + (unicodedata.name(self.mark)) + " (" + str(format(m, '04x')) + ")"
        else:
            if(self.feature):
                return str(feature_desc.get(self.feature)) + str(unicodedata.name(self.base)) + " (" + str(format(b, '04x')) + ")" + " needs to be sorted out: " + str(unicodedata.name(self.mark)) + " (" + str(format(m, '04x')) + ")"
            else:
                return str(unicodedata.name(self.base)) + " (" + str(format(b, '04x')) + ")" + " needs to be sorted out: " + (unicodedata.name(self.mark)) + " (" + str(format(m, '04x')) + ")"

def safe_open_w():
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    path = "./generated_profiles"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

def base_mark_splitter(pair):
    base = ''
    mark = ''
    if(len(pair) < 2):
        decomp = unicodedata.normalize('NFD', pair)
        base = decomp[0]
        mark = decomp[1]
    elif(len(pair) == 2):
        base = pair[0]
        mark = pair[1]
    else:
        print("pair definition incorrect")
    return base, mark

def create_file(profile_name):
    path = "./generated_profiles/"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    profile = open(path + profile_name, "w")
    return profile

     
''' construction patterns for profile
shaping_tests = [{"inputs": test3.construct(), "mark2base": test4.construct()[0], "rationale": test4.construct()[1]}]
new_profile["features"] = test.construct()
new_profile["languagesystems"] = test2.construct()
new_profile["shaping"] = shaping_tests
'''
def main(infile):
    data_raw = infile
    data = []
    for line in data_raw:
        x = line.replace('\n', '').split("|")
        data.append(x)

    current_script = ''
    profile = ''
    new_profile = {}
    features_tests = []
    langsystems_tests = []
    shaping_tests = []


    for sg_test in data:
        script = sg_test[0]


        #pprint(new_profile)

        if(profile == ''):
            current_script = script
            profile_name = '%s.yaml' % script
            profile = create_file(profile_name)
            profile.write("#auto-generated using generate-sg-profile.py\n")
        elif(script != current_script):
            yaml.safe_dump(new_profile, profile, allow_unicode=True, sort_keys=False)
            profile.close
            current_script = script
            profile_name = '%s.yaml' % script
            profile = create_file(profile_name)
            profile.write("#auto-generated using generate-sg-profile.py\n")

        #close_file(profile)


        #feature = "mark"
        #test = "involves"
        #value = "hyperglot"
        if(sg_test[1] == "features" and sg_test[3] == 'involves'):
            features_test = Features(sg_test[2], sg_test[3], sg_test[4])
            features_test = features_test.construct_involves()
            features_tests.append(features_test)
        elif(sg_test[1] == "features" and sg_test[3] == 'present'):
            features_test = Features(sg_test[2], sg_test[3], sg_test[4])
            features_test = features_test.construct_present()
            features_tests.append(features_test)

        #script = "latn"
        #language = "dflt"
        elif(sg_test[1] == 'languagesystems'):
            langsystems_tests = Languagesystems(sg_test[2], sg_test[3])
            new_profile["languagesystems"] = langsystems_tests.construct()


        elif(sg_test[1] == 'mark2base'):
            #pairs = ["e\u0300", "o\u0303", "n\u0303", "m\u0303"]
            pairs = []
            pairs = sg_test[2].replace('\n', '').split(" ")
            fea_setting = ''
            if(len(sg_test[3]) != 0):
                fea_setting = bool(1)
            else:
                fea_setting = bool(0)

            #test_feature = "smcp"
            #conditional_feature = "smcp"
            for pair in pairs:
                base, mark = base_mark_splitter(pair)
                inputs = Inputs2(script, base, mark, sg_test[3], fea_setting)
                mark2base = Mark2Base(script, base, mark)
                rationale = Rationale(script, base, mark, sg_test[3], sg_test[1])
                if(len(sg_test[3]) == 0):
                    shaping_test = {"inputs": inputs.construct(), "mark2base": mark2base.construct(), "rationale": rationale.construct()}
                else:
                    filter_feature = FilterFeature(sg_test[3])
                    shaping_test = {"inputs": inputs.construct(), "mark2base": mark2base.construct(), "rationale": rationale.construct(), "if": filter_feature.construct()}
                #print(shaping_tests)
                shaping_tests.append(shaping_test)

        if (len(features_tests) > 0):
            new_profile["features"] = features_tests
        if(len(shaping_tests) > 0):
            new_profile["shaping"] = shaping_tests

        
    yaml.safe_dump(new_profile, profile, allow_unicode=True, sort_keys=False)
    profile.close

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='infile', help='.csv input file', type=argparse.FileType('r'), required='True')
    args = parser.parse_args()
    #print(args.infile.readlines())
    main(args.infile)
    args.infile.close()
    print("Success: Profiles are in ./generated_profiles")