# coding: utf-8
import pandas as pd
import requests
import yaml
class FinanceSheetCrawler:
    def __init__(self, symbols, sheet_typ=None, freq_typ=None):
        '''
        * symbol: 종목코드
        * fin_type: 재무제표 종류 (0: 손익계산서, 1: 재무상태표, 2: 현금흐름표)
        * freq_type: 기간 (y:년, q:분기)
        '''
        self.symbol = symbols
        
        if sheet_typ in ['ALL', -1]: self.sheet_typ = -1
        elif sheet_typ == 'IS': self.sheet_typ = 0
        elif sheet_typ == 'BS': self.sheet_typ = 1
        else: self.sheet_typ = 2
        
        if freq_typ in ['Y', 'y']: self.freq_typ = 0
        elif freq_typ in ['Q', 'q']: self.freq_typ = 1
        else: self.freq_typ = None
        
    def set_sheet_typ(self,value):
        self.sheet_typ=value
        
    def read(self):
        url='http://companyinfo.stock.naver.com/v1/company/cF3002.aspx'
        if self.sheet_typ == -1:
            df=pd.DataFrame()
            for i in range(3):
                self.set_sheet_typ(i)
                df=pd.concat([df,self.read()],axis=0)
            return df
        
        else:
            data = {    
                    'cmp_cd':self.symbol,
                    'rpt': self.sheet_typ,
                    'finGubun': 'IFRSL',
                    'frqTyp': self.freq_typ
            }
            try:
                f=requests.get(url, data).text   
                yamled_f=yaml.load(f)
            except:
                msg = "symbol:{} can not be crawled".format(self.symbol)
                raise NotImplementedError(msg)
    
            to_name=[x.split('<')[0] for x in yamled_f['YYMM'][:6]]
            from_name=[]
            meanable_list=['ACCODE','ACC_NM']
            for i in range(6):
                from_name.append('DATA{}'.format(i+1))
            meanable_list.extend(from_name)
    
            try:
                df=pd.DataFrame(yamled_f['DATA'],columns=meanable_list).set_index('ACCODE')
                df.rename(columns=dict(zip(from_name,to_name)),inplace=True)
            except:
                msg = "symbol:{} has no data".format(self.symbol)
                raise NotImplementedError(msg)  
    
            return df
        