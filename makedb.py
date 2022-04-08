import csv
import requests
from io import BytesIO

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pop_final_project.settings")
import django
django.setup()

from django.core.files import File
from card.models import Gift

def makedb(name, tag_list, img_url, desc):
    new_gift = Gift()
    new_gift.gift_name = name
    temp_file = download(img_url)
    new_gift.gift_img.save(img_url.split("/")[-1], File(temp_file))
    new_gift.gift_desc = desc
    new_gift.save()
    for tag in tag_list:
        new_gift.tags.add(tag)
    new_gift.save()

# url로부터 파일을 임시 다운로드
def download(url):
    response = requests.get(url)
    binary_data = response.content
    temp_file = BytesIO()
    temp_file.write(binary_data)
    temp_file.seek(0)
    return temp_file

# ['세부테그', '다이어트식품', '다이어트음식', '다이어트식단', '맛있는단백질쉐이크', '마이프로틴5kg', '매일유업셀렉스', '셀렉스초코', '대장사랑', '맥스컷', '장청소', '다이어트단백질쉐이크', '지방분해', '히알루론산', '셀렉스웨이프로틴', '단백질파우더', '황금구렁이', '신타6아이솔레이트', '차전자피', '임팩트웨이프로틴', '초코프로틴', '돌외잎', '딥트3일', '다이어트보조제추천', '그라비올라', '돌외잎다이어트', '하이뮨 

if __name__=='__main__':
    info = open("./media/total_list (1).csv", "r", encoding="utf-8-sig")
    reader = csv.reader(info)
    de_tag_list1 = []
    line_list1 = []
    de_tag_list2 = []
    line_list2 = []
    de_tag_list3 = []
    line_list3 = []
    for line in reader:
        if not line[1] in de_tag_list1:
            de_tag_list1.append(line[1])
            line_list1.append(line)
        elif not line[1] in de_tag_list2:
            de_tag_list2.append(line[1])
            line_list2.append(line)
        elif not line[1] in de_tag_list3:
            de_tag_list3.append(line[1])
            line_list3.append(line)
    for l in line_list1:
        name = l[2]
        tag_list = l[:2] 
        desc = l[0] + " " + l[1] + " " + l[2]
        img_url = "https:" + l[4]
        if l[4] != "상품이미지":
            makedb(name=name, tag_list=tag_list, img_url=img_url, desc=desc)
            print(name)
    for l in line_list2:
        name = l[2]
        tag_list = l[:2] 
        desc = l[0] + " " + l[1] + " " + l[2]
        img_url = "https:" + l[4]
        if l[4] != "상품이미지":
            makedb(name=name, tag_list=tag_list, img_url=img_url, desc=desc)
            print(name)
    for l in line_list3:
        name = l[2]
        tag_list = l[:2] 
        desc = l[0] + " " + l[1] + " " + l[2]
        img_url = "https:" + l[4]
        if l[4] != "상품이미지":
            makedb(name=name, tag_list=tag_list, img_url=img_url, desc=desc)
            print(name)
    print("done")