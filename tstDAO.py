from database.DAO import DAO
from model.model import Model

res = DAO.getAllObjects()
model = Model()
#model.creaGrafo()

conn = DAO.getAllConnessioni(model._idMap)
print(len(res))
print(len(conn))
