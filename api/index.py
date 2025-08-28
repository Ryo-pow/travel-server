from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware # CORSを許可するために追加
from typing import List
from vercel_blob import put
import os

app = FastAPI()

# CORSミドルウェアの設定を追加
# これにより、どの場所からのアクセスも許可されるようになります
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

@app.get("/")
def read_root():
    """
    ルートURLにアクセスがあった場合にメッセージを返す、テスト用のエンドポイント
    """
    return {"Hello": "World"}

@app.post("/upload-multiple-images/")
async def upload_multiple_images(files: List[UploadFile] = File(...)):
    """
    クライアントから複数の画像ファイルを受け取り、Vercel Blobにアップロードするエンドポイント
    """
    uploaded_urls = []
    try:
        for file in files:
            contents = await file.read()
            
            # Vercel Blobにファイルをアップロード
            blob_result = put(
                pathname=file.filename, 
                body=contents, 
                add_random_suffix=True,
                access='public'
            )
            
            # アップロードされたファイルのURLをリストに追加
            uploaded_urls.append(blob_result['url'])

        # 成功したことをクライアントに伝える
        return JSONResponse(
            status_code=200, 
            content={
                "message": f"{len(uploaded_urls)} images uploaded successfully!", 
                "urls": uploaded_urls
            }
        )

    except Exception as e:
        # エラーが発生した場合
        return JSONResponse(
            status_code=500, 
            content={"message": f"An error occurred: {str(e)}"}
        )