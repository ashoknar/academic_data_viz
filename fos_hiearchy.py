import json
import pickle
import numpy as np
from tqdm import tqdm
from collections import defaultdict


def dd():
    return None

class Node:
    def __init__(self, level, idx):
        self.level = level
        self.id = idx
        self.parent = list()
        self.child = list()


text_file = open("FieldOfStudyChildren.txt", 'r')
full_list = text_file.read().split('\n')

l0_file = open("l0.json", 'r')
l0_json_full = json.load(l0_file)
l0_json = l0_json_full['entities']

l0_list = list()
for item in l0_json:
    l0_list.append(int(item['Id']))

l1_file = open("l1.json", 'r')
l1_json_full = json.load(l1_file)
l1_json = l1_json_full['entities']

l1_list = list()
for item in l1_json:
    l1_list.append(int(item['Id']))

l2_file = open("l2.json", 'r')
l2_json_full = json.load(l2_file)
l2_json = l2_json_full['entities']

l2_list = list()
for item in l2_json:
    l2_list.append(int(item['Id']))

l3_file = open("l3_new.json", 'r')
l3_json_full = json.load(l3_file)
l3_json = l3_json_full['entities']

l3_list = list()
for item in l3_json:
    l3_list.append(int(item['Id']))

print(len(l0_list))
print(len(l1_list))
print(len(l2_list))
print(len(l3_list))

l_list = list()
r_list = list()
for each in full_list:
    left = each.split('\t')[0]
    right = each.split('\t')[1]

    l_list.append(int(left))
    r_list.append(int(right))

fos = defaultdict(dd)
done = list()
ctr = 0

for idx1 in tqdm(l_list, leave=False):

    if idx1 in done:
        continue
    else:
        done.append(idx1)

    indices = [i for i, x in enumerate(l_list) if x == idx1]

    for each in indices:

        idx2 = r_list[each]

        if idx2 in l1_list:
            lvl = 1
        elif idx2 in l2_list:
            lvl = 2
        elif idx2 in l3_list:
            lvl = 3
        else:
            lvl = 4

        if idx1 in l0_list:

            if fos[idx1] is None:
                n0 = Node(level=0, idx=idx1)
            else:
                n0 = fos[idx1]

            if fos[idx2] is None:
                n1 = Node(level=lvl, idx=idx2)
            else:
                n1 = fos[idx2]

            n0.child.append(idx2)
            n1.parent.append(idx1)

            fos[idx1] = n0
            fos[idx2] = n1

        elif idx1 in l1_list:
            if fos[idx1] is None:
                n1 = Node(level=1, idx=idx1)
            else:
                n1 = fos[idx1]

            if fos[idx2] is None:
                n2 = Node(level=lvl, idx=idx2)
            else:
                n2 = fos[idx2]

            n1.child.append(idx2)
            n2.parent.append(idx1)

            fos[idx1] = n1
            fos[idx2] = n2

        elif idx1 in l2_list:
            if fos[idx1] is None:
                n2 = Node(level=2, idx=idx1)
            else:
                n2 = fos[idx1]

            if fos[idx2] is None:
                n3 = Node(level=lvl, idx=idx2)
            else:
                n3 = fos[idx2]

            n2.child.append(idx2)
            n3.parent.append(idx1)

            fos[idx1] = n2
            fos[idx2] = n3

        elif idx1 in l3_list:
            if fos[idx1] is None:
                n3 = Node(level=3, idx=idx1)
            else:
                n3 = fos[idx1]

            if fos[idx2] is None:
                n4 = Node(level=lvl, idx=idx2)
            else:
                n4 = fos[idx2]

            n3.child.append(idx2)
            n4.parent.append(idx1)

            fos[idx1] = n3
            fos[idx2] = n4

        else:
            if fos[idx1] is None:
                n5 = Node(level=5, idx=idx1)
            else:
                n5 = fos[idx1]

            if fos[idx2] is None:
                n6 = Node(level=6, idx=idx2)
            else:
                n6 = fos[idx2]

            n5.child.append(idx2)
            n6.parent.append(idx1)

            fos[idx1] = n5
            fos[idx2] = n6
            ctr+=1

print(fos)

out_file = open("fos.pkl", "wb")
pickle.dump(fos, out_file)
out_file.close()