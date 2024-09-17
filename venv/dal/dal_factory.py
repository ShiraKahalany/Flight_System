from dal.interfaces.idal import IDAL
from dal.dal_impl import DALImpl

class DALFactory:
    _instance = None

    @staticmethod
    def get_instance() -> IDAL:
        if DALFactory._instance is None:
            DALFactory._instance = DALImpl()
        return DALFactory._instance
