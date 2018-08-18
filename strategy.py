# coding: utf-8
from FinanceDataReader.data import (PriceReader, SheetReader, StockListing, PriceCrossSectionReader)
from FinanceDataReader.sheet.data import (FinanceSheetCrawler)
import pandas as pd

class strategy:
    def __init__(self):
        self.time = None
        self.scoring_func = None #function
    
    def fit(self, scoring_func):
        self.scoring_func = scoring_func
        
    def screening(self, basket):
        price_df=PriceCrossSectionReader().set_index('Symbol').reindex(basket)
        score=dict()
        for symbol in basket:
            # Step 1 : Generate DataFrame of each symbol
            temp_object = FinanceSheetCrawler(symbols=symbol,sheet_typ= -1,freq_typ='Q')
            temp_sheet = pd.DataFrame()
            for i in range(3):
                temp_object.set_sheet_typ(i)
                temp_subsheet = temp_object.read()
                if i==1:
                    averaged = temp_subsheet.iloc[:,2:-1].dropna(how='all').fillna(0)
                    averaged = averaged.mean(axis=1,skipna=False)
                else:
                    averaged = temp_subsheet.iloc[:,2:-1].sum(axis=1,skipna=True, min_count=1)
                temp_sheet = pd.concat([temp_sheet,averaged],axis=0)
            temp_price = price_df.loc[symbol]
            symbol_df = pd.concat([temp_sheet,temp_price],axis=0)
            # Step 2 : Scoring
            symbol_score = self.scoring_func(symbol_df)
            score[symbol] = symbol_score
         
        return pd.DataFrame.from_dict(score,orient='index',columns={'score'}).sort_values('score')
    
    def backtesting(self, basket, date): #구현 예정
        msg = "which basket would be tested for?"
        raise NotImplementedError(msg)