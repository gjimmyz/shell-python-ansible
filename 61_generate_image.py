cat generate_image.py
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:generate_image.py
#Function:
#Version:1.0
#Created:2023-06-09
#--------------------------------------------------
import json
import base64
import requests
import sys
import os
import math
import threading
import time
from datetime import datetime
from zipfile import ZipFile

def post_re(url, data):
    return requests.post(url, data=json.dumps(data))

def save_encoded_image(b64_image, output_path):
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))

def process_image(txt2img_url, prompt, model_name, output_path_prefix, num_images):    data = {'prompt': prompt, 'model': model_name}

    for i in range(1, num_images + 1):
        response = post_re(txt2img_url, data)
        output_file = f"{output_path_prefix}{i}.png"
        save_encoded_image(response.json()['images'][0], output_file)

def read_input_file(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    models = [line.strip().split('=')[1] for line in lines if line.startswith('model') and not line.startswith('#')]
    prompt = [line.strip().split('=')[1] for line in lines if line.startswith('prompt') and not line.startswith('#')][0]
    pic_all_num = int([line.strip().split('=')[1] for line in lines if line.startswith('pic_all_num')][0])
    txt2img_url = [line.strip().split('=')[1] for line in lines if line.startswith('txt2img_url')][0]
    images_dir = [line.strip().split('=')[1] for line in lines if line.startswith('images_dir')][0]
    compression = int([line.strip().split('=')[1] for line in lines if line.startswith('compression')][0])

    return txt2img_url, models, prompt, pic_all_num, images_dir, compression

def timer(message_interval=60):
    while not timer_event.is_set():
        print("正在处理图片，请稍等...")
        time.sleep(message_interval)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 generate_image.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    txt2img_url, models, prompt, pic_all_num, images_dir, compression = read_input_file(input_file)

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    start_time = datetime.now()
    print(f"开始时间: {start_time}")

    timer_event = threading.Event()
    t = threading.Thread(target=timer)
    t.start()

    # Calculate the number of images for each model
    num_models = len(models)
    num_images_per_model = [pic_all_num // num_models + (1 if x < pic_all_num % num_models else 0)  for x in range(num_models)]
    total_images_generated = 0
    for model, num_images in zip(models, num_images_per_model):
        process_image(txt2img_url, prompt, model, f"{images_dir}/{model}-", num_images)
        total_images_generated += num_images

    timer_event.set()
    t.join()

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(f"结束时间: {end_time}")
    print(f"共产生了{total_images_generated}张图片，耗时{elapsed_time.days}天{elapsed_time.seconds//3600}小时{(elapsed_time.seconds//60)%60}分钟{elapsed_time.seconds%60}秒")

    if compression:
        with ZipFile(f"{images_dir}.zip","w") as zipf:
            for root, dirs, files in os.walk(images_dir):
                for file in files:
                    zipf.write(os.path.join(root, file))

cat generate_image_var.txt
#var
model1=dreamlike-anime-1.0.safetensors
model2=v1-5-pruned-emaonly.safetensors
#model3=xxx
pic_all_num=2
txt2img_url=http://127.0.0.1:7860/sdapi/v1/txt2img
prompt1=Cartoon/Anime Rabbit。
#prompt2=xxx
images_dir=/root/scripts/images
compression=1