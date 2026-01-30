from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI()

@app.post('/users/upload')
async def file_upload(file: UploadFile = File(...)):

    # Strings reading block
    content: bytes = await file.read() # reading bytes stream
    text = content.decode('utf-8', errors='ignore') # decoding bytes to text
    lines = text.splitlines() # how a list now (with lines)

    #Analyzing block
    rejected = [el for el in lines if 'Failed password' in el]
    successful = [el for el in lines if 'Accepted password' in el]

    # IP analyzing
    import re
    ip_pattern = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
    rejectes_ips = []
    for line in rejected:
        found = re.findall(ip_pattern, line)
        rejectes_ips.extend(found)

    unique_apis = list(set(rejectes_ips))



    return {
        "filename" : file.filename,
        "content_type" : file.content_type,
        "bytes_size" : len(content),
        "lines_count" : len(lines),
        "failed" : len(rejected),
        "successful" : len(successful),
    }







if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)