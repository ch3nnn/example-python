# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2022/4/13 00:39


import base64
import os
from pathlib import Path

import requests

"""
百度云调用图片翻译api示例代码
批量翻译文件夹下图片内容
"""

ak = "官网获取的AK"
sk = "官网获取的SK"

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
response = requests.get(host)
if response:
    print(response.json())


def getImgFilePathByDir(dir_path):
    """按目录获取 Img 文件路径"""
    img_file_list = []
    for cur_dir, sub_dir, included_file in os.walk(dir_path):
        if included_file:
            for img_file in included_file:
                if img_file.endswith(".jpg"):
                    img_file_list.append(img_file)
    return img_file_list


def getImgBase64ByTranslate(fileName):
    """通过翻译获取图像 Base64"""

    access_token = "获取Access Token"

    url = f'https://aip.baidubce.com/file/2.0/mt/pictrans/v1?access_token={access_token}'

    from_lang = 'kor'
    to_lang = 'zh'

    # Build request
    payload = {'from': from_lang, 'to': to_lang, 'v': '3', 'paste': '1'}
    image = {'image': (os.path.basename(fileName), open(fileName, 'rb'), "multipart/form-data")}

    # Send request
    response = requests.post(url, params=payload, files=image)
    result = response.json()

    # Show response
    print(result["data"]["content"])
    return result["data"]["pasteImg"]


def base64ToImg(ImgBase64, fileName):
    imgdata = base64.b64decode(ImgBase64)
    fileName.write_bytes(imgdata)


if __name__ == '__main__':
    try:
        dirPath = '图片文件夹'
        for imgFile in getImgFilePathByDir(dirPath):
            imgAbsolutePath = os.path.join(dirPath, imgFile)
            imgBase64 = getImgBase64ByTranslate(imgAbsolutePath)
            base64ToImg(imgBase64, Path(dirPath).joinpath("download", imgFile))
    except Exception as e:
        print(e)
