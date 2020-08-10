from collections import defaultdict

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

    return scores, node.score
