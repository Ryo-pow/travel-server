# 変更前にはなかった`put`をインポート
from vercel_blob import put
import os
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

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
            # access='public'にすることで、URLを知っていれば誰でも画像を見られるようになります
            blob_result = put(
                pathname=file.filename, 
                body=contents, 
                add_random_suffix=True,  # 同じファイル名でも上書きしないようにする設定
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