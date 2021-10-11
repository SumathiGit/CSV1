from fastapi import FastAPI
from typing import Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
from io import StringIO
from fastapi import FastAPI, File, UploadFile
import pandas as pd

app = FastAPI(title="MyCSV") 

@app.get('/')
async def root():
    return {'message': 'This API is converting a CSV file into Json'} 

@app.post("/myrequest")
async def root(request: Request):
    return {"received_request_body": await request.body()}


@app.post('/uploadfile/')
async def create_data_file(
        data_file: UploadFile = File(...),
        ):
    df = pd.read_csv(StringIO(str(data_file.file.read(), 'utf-8')), encoding='utf-8')
    headers = {"header_count": "3", "content_type": "text/csv","col_header":['id','name','price']}

    col_header=[]
    for items in headers["col_header"]: 
        print(items)
        col_header.append(items)
    print(type(col_header)) #list
    print(col_header)


    mycol = list(df.columns)          #list
    print(mycol)
    print(type(mycol))                #list
    rowcount = len(df.columns)        #3
    

    
    myjson = json.loads(df.to_json(orient = "records"))
    print(myjson)
    print(type(myjson))



    col_header.sort()
    print(col_header)
    mycol.sort()
    print(mycol)


    
    for i in col_header:
        if i not in mycol:
            raise HTTPException(status_code=404,detail="Item not Found !")
        if int(headers["header_count"]) == len(df.columns):
            pass
    else:
        return {'filetype': data_file.content_type,"filename":data_file.filename,"myjsondata":myjson}

