import pyasx

wpl = pyasx.Ticker('WPL.AX')
wpl.get_history()
# fin = wpl.get_financials(fin_type='financials')
# bal = wpl.get_financials(fin_type='balance-sheet')
# cash = wpl.get_financials(fin_type='cash-flow')
# stats = wpl.get_statistics()

asd = pyasx.SaveLoad('WPL.AX')



