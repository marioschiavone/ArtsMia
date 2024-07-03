import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.creaGrafo()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi"))
        self._view.update_page()

    def handleCompConnessa(self, e):
        idAdded = self._view._txtIdOggetto.value
        try:
            intId = int(idAdded)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Il valore inserito non è un intero"))
            self._view.update_page()
            return

        if self._model.checkExistece(intId):
            self._view._txt_result.controls.append(
                ft.Text(f"L'oggetto {intId} è presente nel grafo."))
        else:
            self._view._txt_result.controls.append(
                ft.Text(f"L'oggetto {intId} NON è presente nel grafo."))

        sizeConnessa = self._model.getConnessa(intId)

        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa che contiene {intId} ha dimensione {sizeConnessa}.")
        )
        # Fill DD
        self._view._ddLun.disabled = False
        self._view._btnCercaPercorso.disabled = False
        myOptionsNum = list(range(2, sizeConnessa))
        myOptionsDD = list(map(lambda x: ft.dropdown.Option(x), myOptionsNum))
        self._view._ddLun.options = myOptionsDD

        # for i in range(2, sizeConnessa):
        #     self._view._ddLun.options.append(ft.dropdown.Option(i))

        self._view.update_page()

    def handleCercaPercorso(self, e):
        path, peso = self._model.getBestPath(int(self._view._ddLun.value),
                                self._model.getObjFromId(int(self._view._txtIdOggetto.value)))
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato "
                                                       f"con peso migliore uguale a {peso}"))
        self._view._txt_result.controls.append(ft.Text(f"Percorso:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()