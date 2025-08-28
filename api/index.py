from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from vercel_blob import put
import os

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload-single-image/")
async def upload_single_image(file: UploadFile = File(...)):
    """
    クライアントから単一の画像ファイルを受け取り、Vercel Blobにアップロードするエンドポイント
    """
    try:
        contents = await file.read()
        
        # Vercel Blobにファイルをアップロード
        blob_result = put(
            file.filename, 
            body=contents, 
            add_random_suffix=True,
            access='public'
        )
        
        # アップロードされたファイルのURLを返す
        return JSONResponse(
            status_code=200, 
            content={
                "message": "Image uploaded successfully!", 
                "url": blob_result['url']
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"message": f"An error occurred: {str(e)}"}
        )
