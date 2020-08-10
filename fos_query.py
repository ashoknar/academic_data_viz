from collections import defaultdict
import requests
import pickle


def dd():
    return None


class Node:
    def __init__(self, level, idx):
        self.level = level
        self.id = idx
        self.parent = list()
        self.child = list()


class Paper_Node:
    def __init__(self, level, idx, name):
        self.level = level
        self.id = idx
        self.parent = dict()
        self.child = dict()
        self.score = 0
        self.done = 0
        self.fos_name = name


class Paper:
    def __init__(self, tree, score, idx, year):
        self.idx = idx
        self.tree = tree
        self.score = score
        self.year = year


def query(topic_1, topic_2):

    out_file = open("fos.pkl", "rb")
    fos_tree = pickle.load(out_file)
    out_file.close()

    # topic_1 = "computer science"
    # topic_2 = "quantum physics"
    URL = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr=And(Composite(F.FN='{}'),Composite(F.FN='{}'))&count=50000&attributes=F.FId,F.FN,Id,Y".format(
        topic_1, topic_2)

    HEADERS = {"Ocp-Apim-Subscription-Key": "c6c5efdaac704c90b6c3f151d1e7dd8a"}

    PAYLOAD = {}

    response = requests.request("GET", url=URL, headers=HEADERS, data=PAYLOAD)

    data = response.json()

    papers = defaultdict(lambda: list())
    year_papers = dict()

    for paper in data['entities']:
        year_papers[paper['Id']] = paper['Y']
        fos_ids = paper['F']
        for idx in fos_ids:
            papers[paper['Id']].append((fos_tree[idx['FId']], idx['FN']))

    papers_new = defaultdict(lambda: None)

    for paper_id, paper in papers.items():
        tree_paper = defaultdict(lambda: None)
        for fos, fos_name in paper:
            if fos is not None:
                if tree_paper[fos.id] is None:
                    new_node = Paper_Node(idx=fos.id, level=fos.level, name=fos_name)
                else:
                    new_node = tree_paper[fos.id]

                for fos_inner, _ in paper:

                    for fos_node_id in fos.child:
                        if fos_inner is not None and fos_inner.id == fos_node_id:
                            new_node.child[fos_node_id] = fos_inner

                    for fos_node_id in fos.parent:
                        if fos_inner is not None and fos_inner.id == fos_node_id:
                            new_node.parent[fos_node_id] = fos_inner

                new_node.id = fos.id

                tree_paper[fos.id] = new_node

        if fos is not None:
            paper_new = Paper(tree=tree_paper, score=0, idx=paper_id, year=year_papers[paper_id])
            papers_new[paper_id] = paper_new

    scores = defaultdict(lambda: 0)

    def calc_score(tree: object, node: object) -> object:
        if not node.done:
            if len(node.child) != 0:
                for each in node.child:
                    child_node = tree[each]
                    if child_node.score != 0:
                        node.score += child_node.score
                    else:
                        node.score += calc_score(tree, child_node)
            else:
                child_ctr = 0
                for fos_id, fos_node in tree.items():
                    if len(fos_node.child) == 0:
                        child_ctr += 1
                node.score = 1 / child_ctr
        node.done = 1

        scores[node.fos_name] += node.score

        return node.score

    for paper_id, paper_node in papers_new.items():
        for fos_id, fos_node in paper_node.tree.items():
            papers_new[paper_id].tree[fos_id].score = calc_score(paper_node.tree, fos_node)

    scores = sorted(scores, key=scores.get, reverse=True)
    print(scores[:10])
    return 'done'

query(topic_1 = "computer science", topic_2 = "quantum physics")

print('a')
