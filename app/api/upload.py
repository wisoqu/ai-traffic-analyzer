from fastapi import UploadFile, File, APIRouter, HTTPException
from app.parsers.ssh import SSHLogParser

router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024
CHUNK_SIZE = 1024 * 64 # 64 KB
ALLOWED_TYPES = {"text/plain", "application/octet-stream"}
ALLOWED_EXTENSIONS = {".log", ".txt"}


@router.post("/upload")
async def upload_logs(file: UploadFile = File(...)):
    """File (logs) uploading"""

    # Security type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type")
    # Security (extension)
    if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file extension")

    # Reading

    parser = SSHLogParser()
    buffer = ""
    total_size = 0

    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break

        total_size += len(chunk)
        if total_size > MAX_FILE_SIZE:
            raise HTTPException(413, "File too large")

        text = chunk.decode('utf-8', errors='ignore')
        buffer += text


        lines = buffer.split("\n")
        buffer = lines.pop()

        parser.feed(lines)

    # Tail
    if buffer:
        parser.feed([buffer])

    return {
        "filename" : file.filename,
        "analysis" : parser.result()
    }