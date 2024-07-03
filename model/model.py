import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._artObjectList = DAO.getAllObjects()
        self._grafo = nx.Graph()
        self._grafo.add_nodes_from(self._artObjectList)
        # associamo l'id dell'oggetto all'oggetto
        self._idMap = {}
        for v in self._artObjectList:
            self._idMap[v.object_id] = v
        self._solBest = []
        self._costBest = 0

    def getBestPath(self, lun, v0):
        self._solBest = []
        self._costBest = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            if v.classification == v0.classification:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()
        return self._solBest, self._costBest

    def ricorsione(self, parziale, lun):
        # controllo se parziale è una soluzione valida, ed in caso se è migliore del best
        if len(parziale) == lun:
            if self.peso(parziale) > self._costBest:
                self._costBest = self.peso(parziale)
                self._solBest = copy.deepcopy(parziale)
            return
        # se arrivo qui allora len(parziale) < lun
        for v in self._grafo.neighbors(parziale[-1]):
            # v lo aggiungo se non è già in parziale e se ha stessa classification di v0
            if v.classification == parziale[-1].classification and v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()


    def peso(self, listObject):
        p = 0  # sono sicuro che gli elementi hanno un arco
        for i in range(0, len(listObject) - 1):  # -1 perché devo contare gli archi
            p += self._grafo[listObject[i]][listObject[i + 1]]["weight"]
        return p

    def getConnessa(self, v0int):  # v0 nodo da cui partire
        v0 = self._idMap[v0int]
        # Modo 1: successori di v0 in DFS
        successors = nx.dfs_successors(self._grafo, v0)
        allSucc = []
        for v in successors.values():
            allSucc.extend(v)
        print(f"Metodo 1 (pred): {len(allSucc)}")
        # Modo 2: successori di v0 in DFS
        predecessors = nx.dfs_predecessors(self._grafo, v0)
        print(f"Metodo 2 (succ): {len(predecessors.values())}")
        # Modo 3: conto i nodi dell'albero di visita
        tree = nx.dfs_tree(self._grafo, v0)  # tree è un grafo, conta anche l'origine
        print(f"Metodo 3 (tree): {len(tree.nodes())}")

        # Modo4: node_connected_component
        connComp = nx.node_connected_component(self._grafo, v0)
        print(f"Metodo 4 (connected comp): {len(connComp)}")

        return len(connComp)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def checkExistece(self, idOggetto):
        return idOggetto in self._idMap

    def getObjFromId(self, idOggetto):
        return self._idMap[idOggetto]

    def creaGrafo(self):
        self.addEdges()

    def addEdges(self):
        # self._grafo.edges.clear()

        # Soluzione 1: Ciclare sui nodi (se vi sono pochi nodi
        """
        for u in self._artObjectList:
            for v in self._artObjectList:
                peso = DAO.getPeso(u, v)
                self._grafo.add_edge(u, v, weight=peso)
        """
        # Soluzione 2: Una sola query
        allEdges = DAO.getAllConnessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.o1, e.o2, weight=e.peso)
