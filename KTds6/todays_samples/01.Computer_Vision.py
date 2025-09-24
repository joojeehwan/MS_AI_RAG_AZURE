import os, sys, subprocess
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from PIL import Image, ImageDraw

load_dotenv()

COMPUTER_VISION_KEY = os.getenv("COMPUTER_VISION_KEY")
COMPUTER_VISION_ENDPOINT =  os.getenv("COMPUTER_VISION_ENDPOINT")

credential = AzureKeyCredential(COMPUTER_VISION_KEY)
client = ImageAnalysisClient(endpoint=COMPUTER_VISION_ENDPOINT, credential=credential)


def get_image_info():
    file_path = input("분석할 이미지 파일 경로를 입력하세요: ")
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()

    results = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.TAGS,
                         VisualFeatures.CAPTION,
                         VisualFeatures.OBJECTS,
                         VisualFeatures.READ,
                         VisualFeatures.SMART_CROPS,
                         VisualFeatures.PEOPLE
                        ],
        model_version="latest",
       smart_crops_aspect_ratios=[1.0, 1.7778] 

    )

    print("-------------------------------")
    if results.caption is not None:
        print(f"Caption: '{results.caption.text}' with confidence {results.caption.confidence:.2f}")

    print("-------------------------------")
    if results.tags is not None:
        print("Tags:")
        for tag in results.tags.list:
            print(f" - {tag.name} (confidence: {tag.confidence:.2f})")

    print("-------------------------------")
    bounding_boxes =[]
    if results.objects is not None:

        for obj in results.objects.list:
            tag = obj.tags[0]
            print(tag)
            print("Objects:")
            print(f" - {tag.name} (confidence: {tag.confidence:.2f}) at location {obj.bounding_box}")
            bounding_boxes.append(obj.bounding_box)

    draw_bounding_boxes(file_path, bounding_boxes)

def draw_bounding_boxes(image_path, bounding_boxes):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    print("draw_bounding_boxes")

    for box in bounding_boxes:
        x = box['x']
        y = box['y']
        w = box['w']
        h = box['h']

        draw.rectangle(((x,y),(x+w,y+h)),outline="red", width=4)
        draw.text((x,y),"Object",fill="red")
   #image.show()
    out_path = os.path.join(os.path.dirname(image_path), "objects_overlay.png")
    image.save(out_path)
    print("✅ 저장:", out_path)

    # OS별로 파일 열기
    open_image(out_path)

def open_image(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            # WSL이면 wslview, 일반 Linux면 xdg-open
            if "WSL" in os.popen("uname -a").read():
                subprocess.run(["wslview", path])
            else:
                subprocess.run(["xdg-open", path])
    except Exception as e:
        print("자동으로 열기 실패:", e)
        print("파일 경로를 수동으로 열어주세요:", path)

    # print("-------------------------------")
    # if results.read:
    #     for bi, block in enumerate(results.read.blocks):
    #         for li, line in enumerate(block.lines):
    #             print(f"[{bi}-{li}] {line.text}")

    # print("-------------------------------")
    # if results.smart_crops and results.smart_crops.list:
    #     crop = results.smart_crops.list[0]  # 첫 번째 추천 영역
    #     bb = crop.bounding_box             # bounding_box 객체 꺼내기
    #     box = (bb.x, bb.y, bb.x + bb.width, bb.y + bb.height)
    #     print("Bounding Box:", box)

    # print("-------------------------------")
    # if results.people:
    #     for p in results.people.list:
    #         bb = p.bounding_box
    #         print(f"Person box=({bb.x},{bb.y},{bb.width},{bb.height}) conf={p.confidence:.2f}")


if __name__ == "__main__":
    get_image_info()