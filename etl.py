import psycopg2
import pandas as pd

class ETL:

    def __init__(self,**kwargs ):
        self.database = kwargs.get('database')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        
    def connect_to_db(self):
        conn = psycopg2.connect(database = self.database, 
                                user = self.user, 
                                password = self.password,
                                host = self.host,
                                port = self.port)
        print ("Opened database successfully")
        return conn
        
    
        
    def create_table(self):
        try:
            conn = self.connect_to_db()
            cur = conn.cursor()
        except Exception as e:
            print(e)
        
        cur.execute('''CREATE TABLE IF NOT EXISTS knab_info
          (AccNo VARCHAR(10000) PRIMARY KEY NOT NULL,
          PrAccHol VARCHAR(10000) NOT NULL,
          ScAccHol VARCHAR(10000) NULL,
          Nom VARCHAR(10000) NULL,
          DepAmt VARCHAR(10000) NOT NULL,
          MatAmt VARCHAR(10000) NULL,
          IntGain VARCHAR(10000) NULL,
          RoI VARCHAR(10000) NULL,
          DoD VARCHAR(10000) NOT NULL,
          DoM VARCHAR(10000) NULL,
          DtM VARCHAR(10000) NOT NULL,
          YtM VARCHAR(10000) NOT NULL,
          AccType VARCHAR(10000) NOT NULL,
          KnabName VARCHAR(10000) NOT NULL);''')
        print ("Table created successfully")
        conn.commit()
        conn.close()
        
    def insert_value(self,**kwargs):
        try:
            conn = self.connect_to_db()
            cur = conn.cursor()
        except Exception as e:
            print(e)
        finally:
            self.create_table()
        self.AccNo = kwargs.get("AccNo")
        self.PrAccHol = kwargs.get("PrAccHol")
        self.ScAccHol = kwargs.get("ScAccHol", None)
        self.Nom = kwargs.get("Nom",None)
        self.DepAmt = kwargs.get("DepAmt")
        self.MatAmt = kwargs.get("MatAmt", self.DepAmt)
        self.IntGain =  kwargs.get("IntGain")
        self.RoI = kwargs.get("RoI")
        self.DoD = kwargs.get("DoD")
        self.DoM = kwargs.get("DoM",self.DoD)
        self.DtM = kwargs.get("DtM")
        self.YtM = kwargs.get("YtM")
        self.AccType = kwargs.get("AccType","FD")
        self.KnabName = kwargs.get("KnabName",'PNB')
        print( self.AccNo,  self.PrAccHol,  self.ScAccHol,
                                     self.Nom,self.DepAmt,self.MatAmt,self.IntGain,self.RoI,self.DoD,self.DoM,self.AccType,self.KnabName,self.DtM,self.YtM)
        query = f""" INSERT INTO knab_info (AccNo,PrAccHol,ScAccHol,Nom,DepAmt,MatAmt,IntGain,RoI,DoD,DoM,DtM,YtM,AccType,KnabName)\
                    VALUES ('{self.AccNo}','{self.PrAccHol}','{self.ScAccHol}','{self.Nom}','{self.DepAmt}','{self.MatAmt}','{self.IntGain}','{self.RoI}','{self.DoD}','{self.DoM}','{self.DtM}','{self.YtM}','{self.AccType}','{self.KnabName}')"""
        # print(query)
        cur.execute(query)

        conn.commit()
        print ("Records created successfully");
        conn.close()
        
    def show_value(self):
        try:
            conn = self.connect_to_db()
            cur = conn.cursor()
        except Exception as e:
            print(e)
        cur.execute("SELECT * from knab_info;")
        rows = cur.fetchall()
        return rows
        
    def update_value(self, **kwargs):
        try:
            conn = self.connect_to_db()
            cur = conn.cursor()
        except Exception as e:
            print(e)
        pass
        
    def delete_value(self):
        try:
            conn = self.connect_to_db()
            cur = conn.cursor()
        except Exception as e:
            print(e)
        pass
                                

        
        