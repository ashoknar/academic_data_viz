from collections import defaultdict
from query_MAG import query
from plot_graph import plot
import pickle


def dd():
    return None


# Original structure for each fos node in  fos_hierarchy.pkl
class Node:
    def __init__(self, level, idx):
        self.level = level
        self.id = idx
        self.parent = list()
        self.child = list()


# Structure for fos node inside each paper
class Paper_Node:
    def __init__(self, level, idx, name):
        self.level = level
        self.id = idx
        self.parent = dict()
        self.child = dict()
        self.score = 0
        self.done = 0
        self.fos_name = name


# Structure for each paper
class Paper:
    def __init__(self, tree, score, idx, year, author):
        self.idx = idx
        self.tree = tree
        self.score = score
        self.year = year
        self.author = author


def process_data(topic_1, topic_2, start_y, end_y):
    fos_file = open("fos.pkl", "rb")
    fos_tree = pickle.load(fos_file)
    fos_file.close()

    # JSON response from MAG API
    data = query(topic_1, topic_2)

    papers = defaultdict(lambda: list())
    year_papers = dict()
    author_papers = defaultdict(lambda: list())

    for paper in data['entities']:
        year_papers[paper['Id']] = paper['Y']
        for name in paper['AA']:
            author_papers[paper['Id']].append(name['AuN'])
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
            paper_new = Paper(tree=tree_paper, score=0, idx=paper_id, year=year_papers[paper_id],
                              author=author_papers[paper_id])
            papers_new[paper_id] = paper_new

    scores_author = defaultdict(lambda: defaultdict(lambda: 0))
    total_author = defaultdict(lambda: 0)

    scores_year = defaultdict(lambda: defaultdict(lambda: 0))
    scores = defaultdict(lambda: 0)

    # Recursive function to calculate fos score
    def calc_score(year, tree, node, author):
        if not node.done:
            if len(node.child) != 0:
                for each in node.child:
                    child_node = tree[each]
                    if child_node.score != 0:
                        node.score += child_node.score
                    else:
                        node.score += calc_score(year, tree, child_node, author)
            else:
                child_ctr = 0
                for fos_id, fos_node in tree.items():
                    if len(fos_node.child) == 0:
                        child_ctr += 1
                node.score = 1 / child_ctr
        node.done = 1

        scores_year[year][node.fos_name] += node.score
        for name in author:
            scores_author[name][year] += node.score
            total_author[name] += node.score

        scores[node.fos_name] += node.score

        return node.score

    for paper_id, paper_node in papers_new.items():
        for fos_id, fos_node in paper_node.tree.items():
            papers_new[paper_id].tree[fos_id].score = calc_score(paper_node.year, paper_node.tree, fos_node,
                                                                      paper_node.author)

    scores = sorted(scores, key=scores.get, reverse=True)
    # top10_fos = scores[:10]
    # Top 2 topics are omitted since they are always the two selected topics
    top10_fos = scores[2:11]

    score_yrs = defaultdict(lambda: list())

    # Calculate range of years in available papers
    # all_years = sorted(set(year_papers.values()))

    for fos_name in top10_fos:
        for y in range(start_y, end_y):
            score_yrs[fos_name].append(scores_year[y][fos_name])

    score_y = list()
    for each in score_yrs.values():
        score_y.append(each)

    # Stacked area chart for fos.
    plot(start_year=start_y, end_year=end_y, y=score_y, label=top10_fos, topic_1=topic_1, topic_2=topic_2)

    total_author_copy = total_author

    total_author = sorted(total_author_copy, key=total_author_copy.get, reverse=True)
    top10_authors = total_author[:9]

    author_yrs = defaultdict(lambda: list())

    for auth_name in top10_authors:
        for y in range(start_y, end_y):
            author_yrs[auth_name].append(scores_author[auth_name][y])

    author_y = list()
    for each in author_yrs.values():
        author_y.append(each)

    # Stacked area chart for authors.
    plot(start_year=start_y, end_year=end_y, y=author_y, label=top10_authors, topic_1=topic_1, topic_2=topic_2)