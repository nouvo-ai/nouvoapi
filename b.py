from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import subprocess
import uuid

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to nouvo.ai API", "version": "1.0.0", "author": "Hyeonjun Park", "Usable commands": {"/generate_image": "Image Synthesis. Need 3 image files: face, target, eyewear"}}

def overlay_images(background, overlay):
    # 배경 이미지 열기
    background_img = Image.open(background)
    # 안경 이미지 열기
    overlay_img = Image.open(overlay)
    # 배경 이미지에 안경 이미지 합성
    background_img.paste(overlay_img, (0, 0), overlay_img)
    # 합성된 이미지 저장
    output_path = f"output_{str(uuid.uuid4())}.png"
    background_img.save(output_path)

    return output_path

@app.post("/generate_image/")
async def merge_images(face: UploadFile = File(...), target: UploadFile = File(...), eyewear: UploadFile = File(...)):
    # 각 이미지를 파일로 저장
    face_path = "face.png"
    target_path = "target.png"
    eyewear_path = "eyewear.png"
    with open(face_path, "wb") as f:
        f.write(face.file.read())
    with open(target_path, "wb") as f:
        f.write(target.file.read())
    with open(eyewear_path, "wb") as f:
        f.write(eyewear.file.read())

    # roop로 faceswap한 이미지
    faceswap_path = "faceswap.png"

    # 터미널 명령 실행
    command = f"python run.py -s {face_path} -t {target_path} -o {faceswap_path}"
    subprocess.run(command, shell=True)

    merged_image_path = overlay_images(faceswap_path, eyewear_path)

    # 임시로 생성된 이미지 파일들 삭제
    subprocess.run(f"rm {face_path} {target_path} {eyewear_path} {faceswap_path}", shell=True)

    return FileResponse(merged_image_path, media_type="image/png")

if __name__ == "__main__":
    import uvicorn

    # FastAPI 앱을 실행합니다.
    uvicorn.run(app, host="0.0.0.0", port=8000)
