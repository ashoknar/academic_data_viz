import os
from flask import Flask
from fos_query import query, dd, Node
from fos_hierarchy import create_hierarchy

app = Flask(__name__)


@app.route('/')
def run_query():
    topic_1 = "computer science"
    topic_2 = "quantum physics"

    if not os.path.exists("fos.pkl"):
        create_hierarchy()

    output = query(topic_1=topic_1, topic_2=topic_2)
    return output
    return 'bwoh'