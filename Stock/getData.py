#About Network
import FinanceDataReader as fdr
import requests
from bs4 import BeautifulSoup as bs

import pandas as pd
import numpy as np
import re
import io

class MarketCodes():
    """
    코스피, 코스닥 종목코드 GET
    상장폐지, 우량주, 옵션 등 종목도 포함
    """
    def __init__(self,market):
        if(market!='KOSPI')&(market!='KOSDAQ'):
            print("Error : Please input KOSPI or KOSDAQ")
        self.market=market
        self.df = fdr.StockListing(self.market)
            
    def raw_code(self):
        """
        market = 'KOSPI' or 'KOSDAQ'
        """
        codes = self.df['Symbol'].tolist()
        return codes
    
    def stock_code(self):
        """
        콜, 풋옵션과 ETF, ETN 등 제외한 순수 주식
        """
        codes = self.df[~self.df['Sector'].isna()]['Symbol'].tolist()
        return codes
    
    def wo_code(self):
        """
        우량주 코드
        """
        codes = self.df[self.df['Sector'].isna()]['Symbol'].tolist()
        codes = [c for c in codes if not re.search('[a-zA-Z]', c) and len(c)==6 and c[-1] != '0'] + [c for c in codes if c.endswith == 'K']
        codes = [c for c in codes if int(c[0]) <= 1]
        return codes
    
    def etf_code(self):
        """
        ETF 코드
        """
        codes = self.df[self.df['Sector'].isna()]['Symbol'].tolist()
        codes = [c for c in codes if not re.search('[a-zA-Z]', c) and len(c)==6 and c[-1] == '0']
        return codes
    
    def etn_code(self):
        """
        ETN 코드
        """
        codes = self.df[self.df['Sector'].isna()]['Symbol'].tolist()
        codes = [c for c in codes if not re.search('[a-zA-Z]', c) and len(c)==6 and c[-1] != '0'] + [c for c in codes if c.endswith == 'K']
        codes = [c for c in codes if int(c[0]) >= 5]
        return codes
    
    def option_code(self):
        """
        콜, 풋옵션 등 코드
        """
        codes = self.df[self.df['Sector'].isna()]['Symbol'].tolist()
        codes = [c for c in codes if len(c) == 6 and c[2:4].isalpha()]
        return codes
    
    def closed_code(self):
        """
        code = [kospi : STK, kosdaq : KSQ]
        상장폐지 종목코드
        """
        if(self.market=='KOSPI'):
            code = 'STK'
        else:
            code = 'KSQ'
        url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?' \
                    'name=fileDown&filetype=xls&url=MKD/04/0406/04060600/mkd04060600&' \
                    'market_gubun='+code+'&isu_cdnm=%EC%A0%84%EC%B2%B4&isu_cd=&isu_nm=&' \
                    'isu_srt_cd=&fromdate=20000101&todate=22001231&del_cd=1&' \
                    'pagePath=%2Fcontents%2FMKD%2F04%2F0406%2F04060600%2FMKD04060600.jsp'

        header_data = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
        }
        r = requests.get(url, headers=header_data)

        # STEP 02: download
        url = 'http://file.krx.co.kr/download.jspx'
        form_data = {'code': r.text}
        header_data = {
            'Referer': 'http://marketdata.krx.co.kr/contents/MKD/04/0406/04060600/MKD04060600.jsp',
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
        }
        r = requests.post(url, data=form_data, headers=header_data)
        df = pd.read_excel(io.BytesIO(r.content))
        df['종목코드'] = df['종목코드'].str.replace('A', '')
        df['폐지일'] = pd.to_datetime(df['폐지일'])
        col_map = {'종목코드':'Symbol', '기업명':'Name', '폐지일':'DelistingDate', '폐지사유':'Reason'}
        df=df.rename(columns = col_map)
        codes = df['Symbol'].tolist()
        
        return(codes)

class FinState():
	def __init__(self, code):
		self.code = code

	def get_naver(self):
	    """
	    네이버 금융페이지에서 재무제표 데이터 수집
	    """
	    URL = "https://finance.naver.com/item/main.nhn?code="+self.code

	    samsung_electronic = requests.get(URL)
	    html = samsung_electronic.text

	    soup = bs(html, 'lxml')
	    finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]

	    th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
	    annual_date = th_data[3:7]
	    quarter_date = th_data[7:13]
	    
	    finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]
	    finance_data = [item.get_text().strip() for item in finance_html.select('td')]
	    finance_data = np.array(finance_data)
	    finance_data.resize(len(finance_index), 10)
	    finance_date = annual_date + quarter_date
	    finance = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)
	    
	    return finance 