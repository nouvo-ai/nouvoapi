import requests

def merge_images_api(face_path, target_path, eyewear_path):
    # url = "http://localhost:8000/merge_images/"  # API의 URL을 여기에 입력하세요
    url = "https://nouvoapi.c2lv.repl.co/generate_image/"  # API의 URL을 여기에 입력하세요

    files = {
        "face": open(face_path, "rb"),
        "target": open(target_path, "rb"),
        "eyewear": open(eyewear_path, "rb"),
    }

    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("이미지 합성이 완료되어 저장되었습니다.")
    else:
        print("이미지 합성에 실패하였습니다.")

if __name__ == "__main__":
    face_path = "a.png"  # 백그라운드 이미지 파일 경로
    target_path = "b.png"       # 안경 이미지 파일 경로
    eyewear_path = "c.png"       # 안경 이미지 파일 경로

    merge_images_api(face_path, target_path, eyewear_path)