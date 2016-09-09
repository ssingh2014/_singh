import json
import sys
import getopt
import os
import argparse


def func_add_query_obj(ip_query, ip_vertical, ip_score, ip_max_rank):
    pN_obj = {"query": ip_query, "vertical": ip_vertical, "score": int(ip_score), "max_rank": int(ip_max_rank)}
    print "ADD - Input Query Object --> \"" + input_ps_neg + "\" : " + str(pN_obj)
    return pN_obj


def func_update_query_obj(ip_query, ip_vertical, ip_score, ip_max_rank):
    pN_obj = {"query": ip_query, "vertical": ip_vertical, "score": int(ip_score), "max_rank": int(ip_max_rank)}
    print "UPDATE - Query Object --> \"" + input_ps_neg + "\" : " + str(pN_obj)
    return pN_obj


def func_update_sources_UNIQUE(obj, ip_sources):
    input_srcAry = map(str.strip, ip_sources.split(','))
    for aryVal in input_srcAry:
        obj["sources"].append(aryVal)

    unique_srcAry = []
    [unique_srcAry.append(item) for item in obj["sources"] if item not in unique_srcAry]

    print "New UNIQUE Sources list --> " + str(unique_srcAry)
    return unique_srcAry


def func_addFunction_obj(input_func_name, input_ps_neg, input_query, input_vertical, input_score, input_max_rank, input_sources):
    func_obj = {"function": input_func_name, "positive": [], "negative": [], "sources": []}

    # create positive/negative object
    pn_object = func_add_query_obj(input_query, input_vertical, input_score, input_max_rank)

    inpute_srcAry = map(str.strip, input_sources.split(','))

    if input_ps_neg == "positive":
        func_obj["positive"].append(pn_object)
        for aryVal in inpute_srcAry:
            func_obj["sources"].append(aryVal)

    elif input_ps_neg == "negative":
        func_obj["negative"].append(pn_object)
        for aryVal in inpute_srcAry:
            func_obj["sources"].append(aryVal)

    print "ADD - New function Object --> " + str(func_obj)
    return func_obj


def function_exist(ip_function_name, the_data):
    for checkFunc in the_data["functions"]:
        func = checkFunc["function"]

        if func.find(ip_function_name) > -1:
            print "Update existing function --> \"" + input_func_name + "\""
            return checkFunc
    return None


def query_exist(obj, qry, sign_pN, ip_vertical, ip_score, ip_max_rank):
    print "Raw Input Object is a --> " "\"" + sign_pN + "\" object"

    existingFuncObj = obj

    pn_Obj = existingFuncObj[sign_pN]
    print "Existing \"" + sign_pN + "\" : " + str(pn_Obj)

    for q_obj in pn_Obj:
        # check if query exist in positive/negative object
        # print "Existing query \"" + q_obj["query"] + "\""

        q = q_obj["query"]

        if q.find(qry) > -1:
            print "Input query \"" + qry + "\" exist"
            return q_obj
        else:
            print "Input query \"" + qry + "\" DOESN'T exist"
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a generic file map")
    parser.add_argument("-a", "--app_key", help="provide app name", required=True)
    parser.add_argument("-f", "--func_name", help="provide function name", required=True)
    parser.add_argument("-q", "--query", help="provide query", required=True)
    parser.add_argument("-v", "--vertical", help="provide vertical name", required=True)
    parser.add_argument("-s", "--score", help="provide score", required=True)
    parser.add_argument("-m", "--max_rank", help="provide max rank", required=True)
    parser.add_argument("-pn", "--ps_neg", help="provide positive negative value", required=True)
    parser.add_argument("-src", "--sources", help="provide sources info", required=True)
    args = parser.parse_args()

    input_func_name = "func://" + args.app_key + "/" + args.func_name
    input_query = args.query
    input_vertical = args.vertical
    input_score = args.score
    input_max_rank = args.max_rank
    input_ps_neg = args.ps_neg
    input_sources = args.sources

    icon = u'\u25b2'

    print("\n" + icon.encode('utf-8') * 140)
    print "Input Func Name:--> \"" + input_func_name + "\" <------ Input object --> \"" + input_ps_neg + "\" <------ Input query:--> \"" + input_query + "\""
    print(icon.encode('utf-8') * 140 + "\n")

    #  check and remove content-processing directory
    os.system("rm -rf /mnt/tmp/search-config")

    # clone content-processing repo
    os.system("cd /mnt/tmp && git clone git@github.com:quixey/search-config.git")
    # print "cd /mnt/tmp && git clone git@github.com:quixey/search-config.git"
    print "Remove existing directory & Cloned \"search-config\" --> "

    os.system("cd /mnt/tmp/search-config && git fetch")
    os.system("cd /mnt/tmp/search-config && git checkout master")
    os.system("cd /mnt/tmp/search-config && git pull")

    # path = "data_file"

    path = "/mnt/tmp/search-config/prod_config/v4/queries.json"

    print "queries.json file path --> " + str(path) + "\n"

    with open(path, 'r') as data_file:
        data = json.load(data_file)

    # CHECK if function exist or not
    chkFunc = function_exist(input_func_name, data)

    # ADD new function - if it doesn't exist
    if chkFunc == None:
        add_func_obj = func_addFunction_obj(input_func_name, input_ps_neg, input_query, input_vertical, input_score,
                                            input_max_rank, input_sources)
        print "ADDED - New Function Object ---->  " + str(add_func_obj) + "\n"

        with open(path, mode="w") as data_file_1:
            data["functions"].append(add_func_obj)
            json.dump(data, data_file_1)

        print "\n FINAL OUTPUT data file ---->  " + str(data) + "\n\n"


    # UPDATE function - if it exist
    elif chkFunc != None:
        print "Existing function object --> " + str(chkFunc) + "\n"
        qry = query_exist(chkFunc, input_query, input_ps_neg, input_vertical, input_score, input_max_rank)


        # UPDATE SOURCES list --> "UNIQUE" source list
        new_add_unq_src = func_update_sources_UNIQUE(chkFunc, input_sources)
        chkFunc["sources"] = list(new_add_unq_src)


        # UPDATE query object after checking if "query" exist or not
        if qry == None:
            add_obj = func_add_query_obj(input_query, input_vertical, input_score, input_max_rank)
            add_dd = chkFunc[input_ps_neg]

            print "Existing object --> \"" + input_ps_neg + "\" : " + str(add_dd)

            add_dd = chkFunc[input_ps_neg].append(add_obj)

            with open(path, mode="w") as data_file_2:
                print "\nADDED Function object -----> " + str(chkFunc)
                json.dump(data, data_file_2)

        if qry != None:
            update_obj = func_update_query_obj(input_query, input_vertical, input_score, input_max_rank)

            # list of dictionaries
            object_list = chkFunc[input_ps_neg]

            print "\nCurrent object list --> \"" + input_ps_neg + "\" : " + str(object_list)

            # get dictionaries out of list -- Run O(N cube) loop over here
            for object_dict in object_list:
                if input_query == object_dict["query"]:
                    for key, value in object_dict.items():
                        for keyUpdate, valueUpdate in update_obj.items():
                            if keyUpdate == key:
                                object_dict[keyUpdate] = valueUpdate

            update_dd = object_dict

            print "Update existing query object -----> " + str(update_dd)

            with open(path, mode="w") as data_file_2:
                print "\nUPDATED Function object -----> " + str(chkFunc)
                json.dump(data, data_file_2)

            print ("\n\033[34m {}\033[00m".format("FINAL OUTPUT data file ----> \t" + str(data)) + "\n")

    os.system("cd /mnt/tmp/search-config && git add '/mnt/tmp/search-config/prod_config/v4/queries.json'")
    os.system("cd /mnt/tmp/search-config && git commit -m 'committing merge' ")
    os.system("cd /mnt/tmp/search-config && git push git@github.com:quixey/search-config.git")

    print "\n"


