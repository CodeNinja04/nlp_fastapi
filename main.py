from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
#from gensim.summarization.summarizer import summarize
from pydantic import BaseModel
from gensim.similarities import Similarity
from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim.parsing.preprocessing import remove_stopwords
from fastapi.encoders import jsonable_encoder
from typing import Optional,List,Dict


app = FastAPI()

import spacy
nlp = spacy.load('en_core_web_sm')

class Item(BaseModel):
    text1: str
    text2:str
    
    
class Itemlist(BaseModel):
    text2:str

@app.get('/hello')
def index():
  return {'message': 'Hello world!'}


@app.post('/postagging',response_model=Itemlist)
def pos_tagging(item: Item,x: Optional[str] = None):
    
    
    
    x=nlp(item.text1)
    y=[]
    z={}
    for i in x:
        y.append(i.pos_)
        z[i.text]=i.pos_
   
    item.text2=z
    
    
    json_compatible_item_data = jsonable_encoder(item.text2)
    return JSONResponse(content=json_compatible_item_data)
    #return item

@app.post("/removestopwords",response_model=Itemlist)

def remove_stopword(items : Item,x: Optional[str] = None):
    
    filtered_sentence = remove_stopwords(items.text1)
    items.text2=filtered_sentence 
    json_compatible_item_data = jsonable_encoder(items.text2)
    return JSONResponse(content=json_compatible_item_data) 

origins=['http://localhost:3000/']

app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

