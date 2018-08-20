# coding: utf-8
from FinanceTester.data import (PriceReader, SheetReader, StockListing, PriceCrossSectionReader)
from FinanceTester.sheet.data import FinanceSheetCrawler
from FinanceTester._utils import NegativeDenominatorError
import pandas as pd
import numpy as np

class strategy:
    def __init__(self):
        self.date = None
        self.scoring_func = None #function
    
    def fit(self, scoring_func):
        self.scoring_func = scoring_func
        
    def screening(self, basket):
        price_df=PriceCrossSectionReader().set_index('Symbol').reindex(basket).dropna(how='all')
        if price_df.empty:
            print('You might input wrong basket. PriceCrossSection DataFrame is empty.')
            return np.nan
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
            try: symbol_score = self.scoring_func(symbol_df)
            except NegativeDenominatorError:
                print('{} has negative denominator'.format(symbol))
                symbol_score = np.nan
            except KeyError:
                print('{} doesn\'t have account which you ask'.format(symbol))
                symbol_score = np.nan
            except Error:
                print('{} has error during scoring'.format(symbol))
                symbol_score = np.nan
            else: score[symbol] = symbol_score
        
        df=pd.DataFrame.from_dict(score,orient='index',columns={'score'})
        df.score=df.score.astype('float')
        return df.sort_values('score')
    
    def backtesting(self, basket): #implementing...
        
        '''
        price_df=PriceCrossSectionReader().set_index('Symbol').reindex(basket).dropna(how='all')
        if price_df.empty:
            print('You might input wrong basket. PriceCrossSection DataFrame is empty.')
            return np.nan
        
        date=pd.to_datetime(temp_sheet.columns)
        
        score=dict()
        for symbol in basket:
            temp_sheet = SheetReader(symbols=symbol,sheet_typ= -1,freq_typ='Y').iloc[:,1:-1].dropna(how='all')
            temp_price = price_df.loc[symbol]
            symbol_df = pd.concat([temp_sheet,temp_price],axis=0)
            # Step 2 : Scoring
            try: symbol_score = self.scoring_func(symbol_df)
            except NegativeDenominatorError:
                print('{} has negative denominator'.format(symbol))
                symbol_score = np.nan
            except KeyError:
                print('{} doesn\'t have account which you ask'.format(symbol))
                symbol_score = np.nan
            except Error:
                print('{} has error during scoring'.format(symbol))
                symbol_score = np.nan
            else: score[symbol] = symbol_score
        
        df=pd.DataFrame.from_dict(score,orient='index',columns={'score'})
        df.score=df.score.astype('float')
        return df.sort_values('score')
        '''