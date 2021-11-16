from dotenv import load_dotenv
load_dotenv()
import os
import http.client
import json

class Service:
    
    def __init__(self):
        self.conn = http.client.HTTPSConnection(os.environ.get("MAGIC_ALIEXPRESS_URL"))
        self.headers = {
            'x-rapidapi-host': os.environ.get("MAGIC_ALIEXPRESS_URL"),
            'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY")
        }
  #GET Product Historical Volumen sales
    def getProductVolumenHistory(self,productId, minDate, maxDate):
        try:
            self.conn.request("GET", f"/api/bestSales/product/{productId}/salesHistory?maxDate={maxDate}&minDate={minDate}", 
            headers=self.headers)
            res= self.conn.getresponse()
            data = json.loads(res.read())
            return {'data':data,'status':res.status,'reason':res.reason}
        except Exception as x:
            return {'error':x};
    #GET Product Historical Price
    def getProductPriceHistory(self,productId,minDate, maxDate):
        try:
            self.conn.request("GET", f"/api/bestSales/product/{productId}/pricesHistory?maxDate={maxDate}&minDate={minDate}", 
            headers=self.headers)
            res= self.conn.getresponse()
            data = json.loads(res.read())
            return {'data':data,'status':res.status,'reason':res.reason}
        except Exception as x:
            return {'error':x};
    #Product Best Sales
    def getProductsbyBestSales(self,searchByName,sorting='EVALUATE_RATE_ASC'):
        try:
            self.conn.request("GET", f"/api/bestSales/products?page=1&sort={sorting}&searchName={searchByName}", 
            headers=self.headers)
            res= self.conn.getresponse()
            data = json.loads(res.read())
            return {'data':data,'status':res.status,'reason':res.reason}
        except Exception as x:
            return {'error':x};
    #GET Product feedbacks
    def getFeedbacksbyProduct(self,productId):
        try:
            self.conn.request("GET", f"/api/product/{productId}/feedbacks?page=1", 
            headers=self.headers)
            res= self.conn.getresponse()
            data = json.loads(res.read())
            return {'data':data,'status':res.status,'reason':res.reason}
        except Exception as x:
            return {'error':x};

    #GET Products Searching
    def getProductsbySearch(self,searchWord, minPrice,maxPrice):
        try:
            self.conn.request("GET", f"/api/products/search?name={searchWord}&minSalePrice={minPrice}&sort=NEWEST_DESC&page=1&maxSalePrice={maxPrice}", 
            headers=self.headers)
            res= self.conn.getresponse()
            data = json.loads(res.read())
            return {'data':data,'status':res.status,'reason':res.reason}
        except Exception as x:
            return {'error':x};