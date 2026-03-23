from fastapi import FastAPI, Request
from fastapi.responses import Response
import joblib
import requests

app = FastAPI()

JUICE_URL = "http://127.0.0.1:3000"

model = joblib.load("waf_model.pkl")

def extract_features(req:str):
     req = req.lower()
     return[
     [
        len(req),
        req.count("'"),

        1 if "or 1=1" in req else 0,
        1 if "<script>" in req else 0,
    ]
   ]
    
@app.api_route("/{path:path}",methods=["GET","POST"])
async def waf(request: Request , path:str):
    try:
       url = f"{JUICE_URL.rstrip('/')}/{path}"
       req_text = ""
       
       if request.method == "POST":
           body = await request.body()
           req_text = body.decode(errors = "ignore")
           response = requests.post(url , data=req_text)
       else:
           req_text = request.query_params.get("q","")
           
           response = requests.get(url,params=request.query_params)
            
       if "or 1=1" in req_text.lower() or "<script>" in req_text.lower():
            return{
                 "status": "BLOCKED",
                 "message":"Malicious request detected by WAF"
                }
       
       features = extract_features(req_text)
       prediction = model.predict(features)[0]
       
       if prediction == 1:
           return{
               "status": "BLOCKED",
                "message":"Malicious request detected by WAF"
            }
       response.headers.pop("content-encoding",None)
       response.headers.pop("transfer-encoding",None)
       
       return Response(
             content=response.content,
             status_code = response.status_code,
             headers=dict(response.headers)
            )
    except Exception as e:
         return {"error":str(e)}
          
        


