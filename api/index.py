from fastapi import FastAPI
from fastapi.responses import JSONResponse

# 以前のverel_blobのインポートなどは一旦コメントアウト（無効化）します
# from vercel_blob import put
# import os
# from typing import List
# from fastapi import File, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    """
    ルートURLにアクセスがあった場合にメッセージを返す、テスト用のエンドポイント
    """
    return {"Hello": "World"}

# 画像アップロードの機能も一旦コメントアウト（無効化）します
# @app.post("/upload-multiple-images/")
# async def upload_multiple_images(files: List[UploadFile] = File(...)):
#     uploaded_urls = []
#     try:
#         for file in files:
#             contents = await file.read()
#             blob_result = put(
#                 pathname=file.filename, 
#                 body=contents, 
#                 add_random_suffix=True,
#                 access='public'
#             )
#             uploaded_urls.append(blob_result['url'])
#         return JSONResponse(
#             status_code=200, 
#             content={
#                 "message": f"{len(uploaded_urls)} images uploaded successfully!", 
#                 "urls": uploaded_urls
#             }
#         )
#     except Exception as e:
#         return JSONResponse(
#             status_code=500, 
#             content={"message": f"An error occurred: {str(e)}"}
#         )