import json
import re

def validate_string(input_string, char_list):
    pattern = f"[{''.join(re.escape(char) for char in char_list)}]"
    return bool(re.search(pattern, input_string))

def check_identical_lists(list1,list2):
    if len(list1) == len(list2) and len(list1) == sum(1 for i, j in zip(list1, list2) if i == j):
        return True
    return False

def delete_uselesss_variables(grammer,useless_variables):
    for u in useless_variables:
        del grammer["P"][u]

    for v in grammer["P"].keys():
        p_v = grammer["P"][v]
        for i in p_v:
            if validate_string(i,useless_variables):
                p_v.remove(i)

    grammer["V"] = grammer["P"].keys()

def useless_productions(grammer):
    ### First aspect 
    old_v = list()
    new_v = list()
    variables = grammer["V"]

    for v in grammer["P"].keys():
        p_v = grammer["P"][v]
        for i in p_v:
            if not validate_string(i,variables):
                new_v.append(v)
                break

    while not check_identical_lists(old_v,new_v):
        old_v = new_v
        not_in_old_v = [v for v in grammer["P"].keys() if v not in old_v]
        for v in grammer["P"].keys():
            if v in old_v:
                continue
            p_v = grammer["P"][v]
            for i in p_v:
                if not validate_string(i , not_in_old_v):
                    new_v.append(v)
                    break

    useless_variables = [v for v in grammer["P"].keys() if v not in old_v]
    
    delete_uselesss_variables(grammer,useless_variables)
    

    ### Second aspect

    old_v = list()
    new_v = grammer["S"]
    while not check_identical_lists(old_v,new_v):
        old_v = new_v
        for v in old_v:
            p_v = grammer["P"][v]
            for i in p_v:
                for s in i:
                    if s in grammer["P"].keys():
                        if s not in new_v:
                            new_v.append(s)
    useless_variables = [v for v in grammer["P"].keys() if v not in old_v]
    delete_uselesss_variables(grammer,useless_variables)


f = open("context_free_grammers.json")
grammer_list = json.load(f)

grammer = grammer_list["1"]
useless_productions(grammer)

print(grammer["P"])
# for i in range(1,len(grammer_list)+1,1):
#     grammer = grammer_list[str(i)]
    # print(grammer)
    