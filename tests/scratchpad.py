import pyasx
import time


# wpl = pyasx.Ticker('WPL.AX')
# wpl.get_history()
# fin = wpl.get_financials(fin_type='financials')
# bal = wpl.get_financials(fin_type='balance-sheet')
# bal2 = wpl.get_financials(fin_type='balance-sheet')

# cash = wpl.get_financials(fin_type='cash-flow')
# stats = wpl.get_statistics()

# asd = pyasx.SaveLoad('WPL.AX')

if __name__ == '__main__':  # have to use this for MultiThreading to work
    start = time.perf_counter()

    test1 = pyasx.Create('WPL.AX')

    end = time.perf_counter()

    print(f'time to complete: {round(end - start, 2)} seconds(s)')

    test1.create_indicators()




