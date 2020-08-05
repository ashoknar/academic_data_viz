import pickle

def dd():
    return None


class Node:
    def __init__(self, level, idx):
        self.level = level
        self.id = idx
        self.parent = list()
        self.child = list()

out_file = open("fos.pkl", "rb")
fos = pickle.load(out_file)
out_file.close()

print(fos)