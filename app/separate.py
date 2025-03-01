import demucs.separate

def separate_mp3(file_name: str):
    try:
        demucs.separate.main(['--mp3', '--mp3-preset=2', '-n', 'htdemucs_6s', f'downloads/{file_name}.mp3'])
    except Exception as e:
        raise Exception(f"Failed to separate mp3 {file_name}: {str(e)}")