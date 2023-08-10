import re

import requests
from bs4 import BeautifulSoup
from plugins.aipaint.config.config import default_config

session = requests.session()

main_page_url = 'https://holara.ai/holara/'
random_prompt = 'https://holara.ai/holara/api/1.0/random_prompt'
generator_url = 'https://holara.ai/holara/api/1.0/generate_image'


def get_csrf_value():
    main_page = session.get(main_page_url)

    bs = BeautifulSoup(main_page.content, 'lxml')

    pattern = r"var csrf = '([A-Za-z0-9]+)';"
    match = re.search(pattern, bs.select('script')[5].get_text().strip())
    csrf_value = ''
    if match:
        csrf_value = match.group(1)
    else:
        print("CSRF value not found.")
    return csrf_value


'''
{
    "status": "success",
    "prompt": "",
    "seed": ""
}
'''


def get_random_prompt():
    return session.get(random_prompt).json()


def get_generator_img(prompt, negative_prompt, model, width, height, steps, cfg_scale, strength, seed, history, random_autogen, variations_autogen, quality_tags, num_images, random_prompt_seed, init_image, skip, continuous_mode, csrfmiddlewaretoken):
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://holara.ai',
        'Referer': 'https://holara.ai/holara/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': f'csrftoken={csrfmiddlewaretoken};sessionid={default_config["sessionid"]}; holara_r={default_config["holara_r"]}'
    }
    data = {
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'model': model,
        'width': width,
        'height': height,
        'steps': steps,
        'cfg_scale': cfg_scale,
        'strength': strength,
        'seed': seed,
        'history': history,
        'random_autogen': random_autogen,
        'variations_autogen': variations_autogen,
        'quality_tags': quality_tags,
        'num_images': num_images,
        'random_prompt_seed': random_prompt_seed,
        'init_image': init_image,  # data:image/png;base64,
        'skip': skip,
        'continuous_mode': continuous_mode,
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
    }
    return session.post(generator_url, data=data, headers=headers).json()


def gen_img(random_img, prompt, negative_prompt, model, width, height, steps, cfg_scale, strength, seed, history, random_autogen, variations_autogen, quality_tags, num_images, init_image, skip, continuous_mode):
    csrf = get_csrf_value()
    random_img_seed = '0'
    if random_img:
        prompts = get_random_prompt()
        prompt, random_img_seed = prompts['prompt'], prompts['seed']
    img = get_generator_img(prompt, negative_prompt, model, width, height, steps, cfg_scale, strength, str(seed), history, random_autogen, variations_autogen, quality_tags, num_images, str(random_img_seed), init_image, skip, continuous_mode, csrf)
    images = img['images']
    remain = img['hologems_remaining']
    generation_cost = img['generation_cost']
    return images, remain, generation_cost
