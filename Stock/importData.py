import pymysql
import pandas as pd

class FromMysql:
    
    def __init__(self, db_name, password):
        '''
        Connect to mysql by password, db name
        '''
        
        self.con = pymysql.connect(
        user='root', 
        passwd=password, 
        host='127.0.0.1', 
        db=db_name, 
        charset='utf8'
        )
        
    def all_codes(self):
        '''
        Return all code names from db
        '''
        
        cur = self.con.cursor()
        cur.execute('show tables')
        codes = [c[0] for c in cur]
        return codes
    
    def extract_df(self, code):
        '''
        Extract data frame from the code
        '''
        cur = self.con.cursor()
        sql = f"select * from {code}"
        cur.execute(sql)
        result = cur.fetchall();

        df = pd.DataFrame(result)
        columnNames = [x[0] for x in cur.description]
        df.columns = columnNames
        return df
    
    def __del__(self):
        '''
        Disconnect
        '''
        self.con.close()