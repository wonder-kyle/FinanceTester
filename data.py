from FinanceTester.investing.data import (InvestingDailyReader)
from FinanceTester.krx.listing import (KrxStockListing)
from FinanceTester.krx.PriceCrossSectionReader import (PriceCrossSection)
from FinanceTester.sheet.data import (FinanceSheetCrawler)

def PriceReader(symbol, start=None, end=None, country=None):
    return InvestingDailyReader(symbols=symbol, start=start, end=end, country=country).read()

def SheetReader(symbol, sheet_typ=None, freq_typ=None):
    return FinanceSheetCrawler(symbols=symbol,sheet_typ=sheet_typ, freq_typ=freq_typ).read()

def StockListing(market):
    market = market.upper()
    if market in [ 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX']:
        return KrxStockListing(market).read()
    else:
        msg = "market=%s is not implemented" % market
        raise NotImplementedError(msg)
        
def PriceCrossSectionReader(date=None):
    return PriceCrossSection(date=None).read()