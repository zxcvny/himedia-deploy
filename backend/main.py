from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import get_db, create_tables
from models import Post
from schema import PostResponse, PostCreate, PostUpdate

import uvicorn
import os 
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 설정
ENV_PATH = Path(__file__).parent / '.env'
load_dotenv(ENV_PATH)

# 환경변수 가져오기 
# react 서버 주소를 origin에 등록을 해야함
# 같은 도메인이 아니므로 react 서버에서 들어오는 요청을 허용할 수 있게 CORS 설정 필요
REACT_HOST = os.getenv('REACT_HOST', "react-server")

if REACT_HOST.startswith('http'):
    # http://localhost:3000 or 5173
    ORIGIN = REACT_HOST
else:
    # https://react-server-xxxx.onrender.com
    ORIGIN = f"https://{REACT_HOST}.onrender.com"

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ORIGIN], # REACT_HOST 에서 ORIGIN으로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 테이블 생성
create_tables()

@app.get('/')
def home():
    return {'message': 'Post API Server'}

@app.post('/posts', response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get('/posts', response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@app.get('/posts/{post_id}', response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put('/posts/{post_id}', response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

@app.delete('/posts/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {'message': 'Post deleted successfully'}

if __name__ == '__main__':
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=8000,
                reload=True)