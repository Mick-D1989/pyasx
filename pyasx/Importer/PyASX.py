from pyasx.Importer.Importer import Ticker
from pyasx.Indicators.Common import Common
from pyasx.utils.utils import *
import concurrent.futures as p


class Create:
    """
    Co-Ordinates the lot:
    """

    def __init__(self, tick, **kwargs):
        tmp1 = Ticker(tick)
        tmp1.get_history(**kwargs)
        self.data = tmp1
        # ThreadPoolExecutor() was about 2s quicker than ProcessPoolExecutor() in testing.
        with p.ThreadPoolExecutor() as executor:
            fin_type = ['financials', 'balance-sheet', 'cash-flow']
            results = executor.map(tmp1.get_financials, fin_type)
            type_tmp = {}
            # map() returns the results in the order they started so its OK to use for loop here
            for result, typ in zip(results, fin_type):
                type_tmp[typ] = result
        self.data.income_statement = type_tmp['financials']
        self.data.balance_sheet = type_tmp['balance-sheet']
        self.data.cash_flow = type_tmp['cash-flow']
        self.indicators = {}

    def create_indicators(self, indicators_to_create=None, **kwargs):
        df = self.data.history
        com = Common(df)
        public_method_names = [method for method in dir(Common) if
                               callable(getattr(Common, method)) if not method.startswith('_')]
        with p.ThreadPoolExecutor() as executor:
            for method in public_method_names:
                tmp = executor.submit(getattr(com, method))
                self.indicators[method] = tmp.result()
        self.indicators = pd.DataFrame(self.indicators)
        return
