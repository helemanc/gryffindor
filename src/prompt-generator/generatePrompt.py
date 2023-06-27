import json
from tqdm import tqdm
from verbalisation_module import VerbModule

def verbalise(tripleList, verbModule):
    ans = "translate Graph to English: "
    predicateSet = set([])
    for item in tripleList:
        if item['predicate'] not in predicateSet or item['predicate'] == "instance of":
            
            if "object" in item.keys():
                ans += f"<H> {item['subject']} <R> {item['predicate']} <T> {item['object']} "
            elif "prob" in item.keys():
                ans += f"<H> {item['subject']} <R> {item['predicate']} <T> {item['prob']} "   

            predicateSet.add(item['predicate'])
            
    return verbModule.verbalise(ans)

def plainPrompt(tripleList):
    ans = ""
    predicateSet = set([])
    for item in tripleList:
        if item['predicate'] not in predicateSet or item['predicate'] == "instance of":
            if "object" in item.keys():
                ans += f"{item['subject']} {item['predicate']} {item['object']}. "
            elif "prob" in item.keys():
                ans += f"{item['subject']} {item['predicate']} {item['prob']}. " 
            predicateSet.add(item['predicate'])
    return ans


def verbaliseFile(FILENAME, outputFile):
    results = []
    f = open(FILENAME, "r")
    data = json.loads(f.read())
    for item in tqdm(data):
        oneItem = {}
        oneItem['item_id'] = item['item_id']
        oneItem['label'] = item['label']
        oneItem['pic'] = item['pic']
        oneItem['basic_prompt'] = item['label']
        oneItem['plain_prompt'] = plainPrompt(item['triple_list'])
        oneItem['verbalised_prompt'] = verbalise(item['triple_list'], verb_module)
        results.append(oneItem)
        
    json_object = json.dumps(results, indent=4)
    with open(outputFile, "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    verb_module = VerbModule()
    FILENAME = "data/exp10.json"
    outputFile = "data/exp10_out.json"
    verbaliseFile(FILENAME, outputFile)