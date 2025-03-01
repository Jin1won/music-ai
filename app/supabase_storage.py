from supabase import create_client, Client
from pathlib import Path
import mimetypes

import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 Supabase 설정 가져오기
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME", "Score")  # 기본값 제공


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_file(file_path: Path, storage_path: str):
    try:
        # 파일 읽기
        with open(file_path, 'rb') as f:
            contents = f.read()
        
        # 파일 타입 확인
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = 'application/octet-stream'
        
        # Supabase Storage에 업로드
        response = supabase.storage \
            .from_(BUCKET_NAME) \
            .upload(
                path=storage_path,
                file=contents,
                file_options={"content-type": content_type}
            )
        
        # 업로드된 파일의 공개 URL 가져오기
        file_url = supabase.storage \
            .from_(BUCKET_NAME) \
            .get_public_url(storage_path)
        
        return {
            "storage_path": storage_path,
            "file_url": file_url
        }
    except Exception as e:
        raise Exception(f"Failed to upload file {file_path}: {str(e)}")