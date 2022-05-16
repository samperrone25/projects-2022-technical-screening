"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json
import re # regular expression
from test_handbook import *

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    
    # working:
    # example courses_list = ["COMP9417", "COMP9418", "COMP9447"]
    # example prepreq_str = "COMP1511    or DPST1091 or COMP1911 or COMP1917"
    # empty case
    # single case
    # AND, OR
    # ...

    prereq_str = CONDITIONS[target_course].upper() # make all upper case

    allowed = is_unlocked_2(courses_list, prereq_str) # can recur

    print("Returned " + str(allowed) + " for target course " + target_course, end="\n\n")
    return allowed


def is_unlocked_2(courses_list, prereqs):

    allowed = False

    # empty case ""
    if prereqs == "":
        return True

    # composite (or,and) case, prioritise smaller index

    i = prereqs.find("OR")
    j = prereqs.find("AND")
    op = ""
    print("Prereq String: " + prereqs)
    print("i (or-index), j (and-index)]: " + str(i) + ", " + str(j))

    if i != -1 and j != -1:
        if i < j:
            op = "OR"
            index = i
        elif j < i:
            op = "AND"
            index = j
            
    elif i != -1 and j == -1:
        op = "OR"
        index = i
    elif i == -1 and j != -1:
        op = "AND"
        index = j
    else: # both -1, no logical operations remaining
        # singular case, e.g. "COMP4337"
        immediate = re.search(r"....(\d+)", prereqs).group()
        return (immediate in courses_list)
    
    immediate, remainder = partition(prereqs, index , op)
        
    if op == "OR":
        if (immediate in courses_list):
            allowed = True
        else:
            allowed = is_unlocked_2(courses_list, remainder)
    else:
        if (immediate not in courses_list):
            allowed = False
        else:
            allowed = is_unlocked_2(courses_list, remainder)
        
    return allowed


def partition(string, i, op):

    print("Searching: " + string[:i])

    immediate = re.search(r"....(\d+)", string[:i]).group()
    remainder = string[i+3:]
    if op == 'OR':
        print("Concluded: " + immediate + " [OR] " + remainder + '\n')
    elif op == 'AND':
        print("Concluded: " + immediate + " [AND] " + remainder + '\n')
    return [immediate, remainder]

if __name__ == "__main__":
    test_empty()
    test_single()
    test_compound()





    