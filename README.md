# Academic Data Visualization and Analysis

## Objectives:
1. Generate Field of Study(Fos) heirarchy from Microsoft Academic Graph(https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/).
2. Use heriarchy to replicate Fos Score, from original publication(https://dl.acm.org/doi/10.1145/3041021.3053064).
3. Query Microsoft Academic Knowledge API for data on _two_ selected fields of study.
4. Create visualizations from calculated Fos scores for related fields of study and most relavent authors.
5. Generate more insights from queried data (Planned).

## Using the repository:
1.**fos_hierarchy.py** to generate Field of study Hierarchy in **fos.pkl**
  * Files in _fos_list/_ may need to be updated to match latest format on MAG database.
  * Fos level lists in _fos_list/_ were created by directly querying Microsoft Academic Knowledge API.

2.**main.py** to generate visualizations.
  * First calls **query_MAG.py** to send a get request to MAK API.
  * Calls **fos_calc.py** to generate fos scores for each paper.
  * Calls **plot_graph.py** to draw visualizations.

3.**fos_print.py** to print generated **fos.pkl** heirarchy file to check integrity.

_You should generate your own API KEY for Microsoft Academic Knowlegde API before using the code at https://www.microsoft.com/en-us/research/project/academic-knowledge/_ 
