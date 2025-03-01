from fastapi import FastAPI, HTTPException
import os
import shutil

from supabase_storage import upload_file
from youtube import export_mp3_from_url
from separate import separate_mp3

app = FastAPI()

@app.get('/extract_audio')
async def extract_audio(youtube_url: str, file_name: str, user_id: str):
    try:
        # youtube url로 mp3파일 추출
        export_mp3_from_url(youtube_url, file_name)
        # 음원분리 AI
        separate_mp3(file_name)

        # supabase 파일 업로드
        upload_results = []
        
        original_result = await upload_file('downloads/test.mp3', f'/audio/{user_id}/original.mp3')
        upload_results.append(original_result)

        parts = ['bass', 'drums', 'guitar', 'other', 'piano', 'vocals']
        for part in parts:
            result = await upload_file(
                f'separated/htdemucs_6s/test/{part}.mp3', 
                f'/audio/{user_id}/{part}.mp3'
            )
            upload_results.append(result)

        # clean up
        clear_dir()

        return upload_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def clear_dir():
    try:
        downloads_dir = 'downloads'
        separated_dir = 'separated'
        delete_dir(downloads_dir)
        delete_dir(separated_dir)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_dir(dir_name):
    folder_path = os.path.join(os.getcwd(), dir_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)