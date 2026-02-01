from fastapi import UploadFile, File, APIRouter
from app.parsers.ssh import make_logs

router = APIRouter()


@router.post("/upload")
async def upload_logs(file: UploadFile = File(...)):
    """File (logs) uploading"""
    content: bytes = await file.read()  # reading bytes stream
    text = content.decode('utf-8', errors='ignore')  # decoding bytes to text
    lines =  text.splitlines()
    parsed = make_logs(lines)
    #explanation = ai_response(parsed)





    return {
        "filename" : file.filename,
        "lines_cout" : len(lines)
    }