import json
import re

def validate_string(input_string, char_list):
    if len(char_list) == 0 :
        return False
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


def landa_productions(grammer):
    old_null = list()
    new_null = list()
    variables = grammer["V"]

    for v in grammer["P"].keys():
        p_v = grammer["P"][v]
        for i in p_v:
            if i == "": 
                new_null.append(v)
    while not check_identical_lists(old_null,new_null):
        old_null = new_null
        for v in grammer["P"].keys():
            p_v = grammer["P"][v]
            for s in p_v:
                if all(ch in old_null for ch in s):
                    if not v in new_null:
                        new_null.append(v)

    null_variables = new_null
    
    new_p = dict()
    for v in grammer["P"].keys():
        new_p[v]= list()
        p_v = grammer["P"][v]

        for i in p_v:
            if not validate_string(i,null_variables):
                new_p[v].append(i)
            else:
                null_variable_indexes=list()
                for index,s in enumerate(i):
                    if s in null_variables: 
                        null_variable_indexes.append(index)

                strings = list()
                for j in null_variable_indexes:
                    if len(strings) == 0 :
                        strg = i 
                        strings.append(strg)
                    
                    strings= strings + strings

                    for k in range(int(len(strings)/2),len(strings),1):
                        strings[k]=str(strings[k]).replace(strings[k][j]," ")


                for j in range(len(strings)):
                    strings[j]= strings[j].replace(" ","")

                new_p[v] = new_p[v] + strings

        new_p[v] = list(filter(("").__ne__, new_p[v])) 
    grammer["P"] = new_p
    grammer["V"] = grammer["P"].keys()
    
def find_unit_productions(items,variable_list):
    res= [i for i in items if i in variable_list]
    
    return set(res)



def unit_productions(grammer):
    new_p = dict()
    for v in grammer["P"].keys():
        expanded_unit_list = set()
        new_p[v] = list()
        for i in grammer["P"][v]:
            new_p[v].append(i)
            if i in grammer["V"]:
                new_p[v] = new_p[v] + grammer["P"][i]
                expanded_unit_list.add(i)
                unit_list = find_unit_productions(new_p[v],grammer["V"])
                while not check_identical_lists(expanded_unit_list,unit_list):
                    for u in unit_list:
                        if not u in expanded_unit_list:
                            new_p[v] = new_p[v] + grammer["P"][u]
                            expanded_unit_list.add(u)
                    unit_list = find_unit_productions(new_p[v],grammer["V"])    
        
        new_p[v] = [j for j in set(new_p[v]) if not j in grammer["V"]]

    grammer["P"] = new_p
    grammer["V"] = grammer["P"].keys()
            




    
if __name__ == "__main__":
    f = open("context_free_grammers.json")
    grammer_list = json.load(f)
    
    grammer = grammer_list["3"]

    landa_productions(grammer)
    unit_productions(grammer)
    useless_productions(grammer)

    print(grammer["P"])
    # for i in range(1,len(grammer_list)+1,1):
    #     grammer = grammer_list[str(i)]
        # print(grammer)