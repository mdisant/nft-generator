# Program to create PNGs for NFT purposes

import png
from PIL import Image
from IPython.display import display 
import random
import json


# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%
background = ["green", "red"] 
background_weights = [30, 70]

hair = ['ginger', 'blonde']
hair_weights = [20, 80]

base = ['base']
base_weights = [100]

skin = ['white']
skin_weights = [100]

eyes = ['big', 'small', 'stoner']
eyes_weights = [60, 30, 10]

mouth = ['gold', 'smile']
mouth_weights = [10, 90]

frame = ['box']
frame_weights = [100]

shade = ['grey_tint']
shade_weights = [100]

outfit = ['space', 'collar']
outfit_weights = [20, 80]

background_files = {'green':'green', 'red':'red'}
hair_files = {'ginger':'ginger', 'blonde':'blonde'}
base_files = {'base':'base'}
skin_files = {'white':'white'}
eyes_files = {'big':'big', 'small':'small', 'stoner':'stoner'}
mouth_files = {'gold':'gold','smile':'smile'}
frame_files = {'box':'box'}
shade_files = {'grey_tint':'grey_tint'}
outfit_files=  {'space':'space', 'collar':'collar'}

TOTAL_IMAGES = 30 # Number of random unique images we want to generate ( 2 x 2 x 1 x 1 x 3 x 2 x 1 x 2 x 2 = 96)
all_images = [] 

def create_new_image():

    new_image = {}

    # For each trait category, select a random trait based on the weightings 
    new_image["Background"] = random.choices(background, background_weights)[0]
    new_image["Hair"] = random.choices(hair, hair_weights)[0]
    new_image["Base"] = random.choices(base, base_weights)[0]
    
    new_image["Skin"] = random.choices(skin, skin_weights)[0]
    new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image["Mouth"] = random.choices(mouth, mouth_weights)[0]
    
    new_image["Frame"] = random.choices(frame, frame_weights)[0]
    new_image["Shade"] = random.choices(shade, shade_weights)[0]

    new_image["Outfit"] = random.choices(outfit, outfit_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image

# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)

def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))

i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1

print(all_images)


background_count = {}
for item in background:
    background_count[item] = 0

hair_count = {}
for item in hair:
    hair_count[item] = 0

base_count = {}
for item in base:
    base_count[item] = 0

skin_count = {}
for item in skin:
    skin_count[item] = 0

eyes_count = {}
for item in eyes:
    eyes_count[item] = 0

mouth_count = {}
for item in mouth:
    mouth_count[item] = 0

frame_count = {}
for item in frame:
    frame_count[item] = 0

shade_count = {}
for item in shade:
    shade_count[item] = 0

outfit_count = {}
for item in outfit:
    outfit_count[item] = 0

# for image in all_images:
#     background_count[image["Background"]] += 1
#     hair_count[image["Hair"]] += 1
#     base_count[image["Base"]] += 1
#     skin_count[image["Skin"]] += 1
#     skin_count[image["Eyes"]] += 1
#     skin_count[image["Mouth"]] += 1
#     skin_count[image["Frame"]] += 1
#     skin_count[image["Shade"]] += 1
#     outfit_count[image["Outfit"]] += 1

# print(background_count)
# print(hair_count)
# print(base_count)
# print(skin_count)
# print(eyes_count)
# print(mouth_count)
# print(frame_count)
# print(shade_count)
# print(outfit_count)

METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)

for item in all_images:

    im1 = Image.open(f'./layers/background/{background_files[item["Background"]]}.png').convert('RGBA')
    im2 = Image.open(f'./layers/hair/{hair_files[item["Hair"]]}.png').convert('RGBA')
    im3 = Image.open(f'./layers/base/{base_files[item["Base"]]}.png').convert('RGBA')
    im4 = Image.open(f'./layers/skin/{skin_files[item["Skin"]]}.png').convert('RGBA')
    im5 = Image.open(f'./layers/eyes/{eyes_files[item["Eyes"]]}.png').convert('RGBA')
    im6 = Image.open(f'./layers/mouth/{mouth_files[item["Mouth"]]}.png').convert('RGBA')
    im7 = Image.open(f'./layers/glasses_frame/{frame_files[item["Frame"]]}.png').convert('RGBA')
    im8 = Image.open(f'./layers/glasses_shade/{shade_files[item["Shade"]]}.png').convert('RGBA')
    im9 = Image.open(f'./layers/outfit/{outfit_files[item["Outfit"]]}.png').convert('RGBA')

    #Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)
    com6 = Image.alpha_composite(com5, im7)
    com7 = Image.alpha_composite(com6, im8)
    com8 = Image.alpha_composite(com7, im9)

    #Convert to RGB
    rgb_im = com8.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./Images/" + file_name)

f = open('./metadata/all-traits.json',) 
data = json.load(f)

IMAGES_BASE_URI = "ADD_IMAGES_BASE_URI_HERE"
PROJECT_NAME = "ADD_PROJECT_NAME_HERE"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))
    token["attributes"].append(getAttribute("Base", i["Base"]))
    token["attributes"].append(getAttribute("Skin", i["Skin"]))
    token["attributes"].append(getAttribute("Eyes", i["Eyes"]))
    token["attributes"].append(getAttribute("Mouth", i["Mouth"]))
    token["attributes"].append(getAttribute("Frame", i["Frame"]))
    token["attributes"].append(getAttribute("Shade", i["Shade"]))
    token["attributes"].append(getAttribute("Outfit", i["Outfit"]))

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()