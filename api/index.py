from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
from vercel_blob import put
import os

app = FastAPI()

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