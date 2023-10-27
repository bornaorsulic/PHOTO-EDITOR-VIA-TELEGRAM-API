import requests
import json
import pilgram
import os
from PIL import Image
import time
import telegram
from telegram import InputFile
import asyncio


def download_image(token, file_path, br):
    url = f'https://api.telegram.org/file/bot{token}/{file_path}'

    response = requests.get(url)

    if response.status_code == 200:
        with open(f'images//photo{br}.jpg', 'wb') as f:
            f.write(response.content)


def get_telegram_updates_text(api_url):
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def extract_last_bot_command(text):
    try:
        data = json.loads(text)
        updates = data.get("result", [])
        
        for update in reversed(updates):
            if "message" in update and "text" in update["message"]:
                message = update["message"]
                if "/" in message["text"]:
                    if "entities" in message:
                        entities = message["entities"]
                        for entity in entities:
                            if entity.get("type") == "bot_command":
                                return message["text"]
        
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None


def get_pictures_ids(telegram_updates_text):
    data = json.loads(telegram_updates_text)
    photo_file_ids = []
    for update in data['result']:
        if 'message' in update and 'photo' in update['message']:
            photos = update['message']['photo']

            for photo in photos:
                print(photo['file_id'])
                photo_file_ids.append(photo['file_id'])

    return photo_file_ids


def get_picture_path(pic_ids, bot_token):
    file_paths = []

    for pic_id in pic_ids:
        url = f'https://api.telegram.org/bot{bot_token}/getFile?file_id={pic_id}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                file_path = data['result']['file_path']
                file_paths.append(file_path)

    return file_paths


def get_photos(api_url, token):
    # Call the function to get the text content from the URL
    telegram_updates_text = get_telegram_updates_text(api_url)

    if telegram_updates_text is None:
        print("Failed to retrieve data from the URL.")

    # Call the function to extract the last bot command
    last_bot_command = int(extract_last_bot_command(telegram_updates_text)[1::])

    if last_bot_command is not None:
        print(f"Last Bot Command: {last_bot_command}")
    else:
        print("No matching command found in the JSON text.")

    # get all pic_ids
    pic_ids = list(reversed(get_pictures_ids(telegram_updates_text)))

    pic_ids2 = []
    for k in range(0, 4*last_bot_command, 4):
        pic_ids2.append(pic_ids[k])

    # get all pic_file_paths
    pic_paths = get_picture_path(pic_ids2, token)

    # download images 
    for k in range(len(pic_paths)):
        download_image(token, pic_paths[k], k + 1)


def editing():
    for image_url in os.listdir('images'):
        img = Image.open(f'images/{image_url}')
        os.mkdir(image_url[:-4])
        img.save(f'{image_url[:-4]}/{image_url[:-4]}-1.jpg')
        pilgram.lofi(img).save(f'{image_url[:-4]}/{image_url[:-4]}-2.jpg')
        pilgram.brannan(img).save(f'{image_url[:-4]}/{image_url[:-4]}-3.jpg')
        pilgram.brooklyn(img).save(f'{image_url[:-4]}/{image_url[:-4]}-4.jpg')
        pilgram.clarendon(img).save(f'{image_url[:-4]}/{image_url[:-4]}-5.jpg')
        pilgram.hudson(img).save(f'{image_url[:-4]}/{image_url[:-4]}-6.jpg')
        pilgram.lofi(img).save(f'{image_url[:-4]}/{image_url[:-4]}-7.jpg')
        pilgram.mayfair(img).save(f'{image_url[:-4]}/{image_url[:-4]}-8.jpg')
        pilgram.nashville(img).save(f'{image_url[:-4]}/{image_url[:-4]}-9.jpg')
        pilgram.perpetua(img).save(f'{image_url[:-4]}/{image_url[:-4]}-10.jpg')
        pilgram.rise(img).save(f'{image_url[:-4]}/{image_url[:-4]}-11.jpg')
        pilgram.slumber(img).save(f'{image_url[:-4]}/{image_url[:-4]}-12.jpg')
        pilgram.valencia(img).save(f'{image_url[:-4]}/{image_url[:-4]}-13.jpg')
        pilgram.walden(img).save(f'{image_url[:-4]}/{image_url[:-4]}-14.jpg')
        pilgram.xpro2(img).save(f'{image_url[:-4]}/{image_url[:-4]}-15.jpg')

    print("All images processed and EDITED.")
    

def combining():
    # Parent folder containing all the folders with photos
    parent_folder = './'

    # Get a list of all subfolders (e.g., photo1, photo2, photo3, ...)
    subfolders = [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]
    subfolders.remove('images')

    # Process each subfolder
    for subfolder in subfolders:
        folder_path = os.path.join(parent_folder, subfolder)

        # Create a list of image file paths in the folder
        image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(('jpg', 'jpeg', 'png', 'gif'))]

        # Sort the image files alphabetically
        image_files.sort()

        # Number of photos per combined image
        photos_per_combined_image = 3

        # Initialize a counter to keep track of the processed images
        image_counter = 0

        # Create a new folder for the combined images
        combined_folder = os.path.join(parent_folder, f'{subfolder}-combined')
        os.makedirs(combined_folder, exist_ok=True)

        while image_counter < len(image_files):
            # Create a new blank image for each batch of 3 photos
            total_width = 0
            total_height = 0
            combined_images = []

            # Process up to 3 images
            for i in range(photos_per_combined_image):
                if image_counter < len(image_files):
                    image_file = image_files[image_counter]
                    image = Image.open(image_file)
                    combined_images.append(image)
                    total_width += image.width
                    total_height = max(total_height, image.height)
                    image_counter += 1

            # Create a new combined image with the calculated size
            new_image = Image.new('RGB', (total_width, total_height))

            # Paste each image onto the new image
            x_offset = 0
            for image in combined_images:
                new_image.paste(image, (x_offset, 0))
                x_offset += image.width

            # Save the combined image in the corresponding combined folder
            combined_image_path = os.path.join(combined_folder, f'combined_image_{image_counter // 3}.jpg')
            new_image.save(combined_image_path)

            # Close the original images
            for image in combined_images:
                image.close()
            new_image.close()

    print("All images processed and COMBINED.")


def lastMessage(date, api_url):

    def extract_last_message_text(text, date):
        try:
            # Parse the JSON text
            data = json.loads(text)
            # Get the "result" field, which contains an array of updates
            updates = data.get("result", [])

            # Iterate through the updates in reverse order to find the last message
            for update in reversed(updates):
                if "message" in update and "text" in update["message"] and date != update['message']['date']:
                    date = update['message']['date']
                    message = update["message"]
                    return message["text"], date

                else:
                    date = update['message']['date']
                    # If no messages are found, return None
                    return None, date
        
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None

    telegram_updates_text = get_telegram_updates_text(api_url)
    last_bot_command, date = extract_last_message_text(telegram_updates_text, date)
    if last_bot_command is not None:
        return f"{last_bot_command[1:]}", date
    else:
        return None, date


async def send_image(bot, chat_ID, image_path):
    with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id=chat_ID, photo=InputFile(photo))


def uploudImage(path, api_token, chat_id):
    bot = telegram.Bot(token=api_token)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_image(bot, chat_id, path))


def selecting_photos(api_url, api_token, chat_id):
    while True:

        datum = 0
        x, datum = lastMessage(datum, api_url)
        if [x] == ['Start']:
            selectedPhotosPaths = []

            dir_path = 'images'
            photosNum = (len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))

            for i in range(1, photosNum + 1):
                dir_path = f'photo{i}-combined'
                photosNumCombined = (len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))

                for j in range(1, photosNumCombined + 1):
                    photoShow = f'photo{i}-combined/combined_image_{j}.jpg'
                    uploudImage(photoShow, api_token, chat_id)

                    time.sleep(5)
                    while True:
                        
                        x, datum = lastMessage(datum, api_url)
                        if [x] == ['1']:
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(1 + (j-1)*3)}.jpg')
                            break
                        elif [x] == ['2']:
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(2 + (j-1)*3)}.jpg')
                            break
                        elif [x] == ['3']:
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(3 + (j-1)*3)}.jpg')
                            break
                        elif [x] == ['12']:
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(1 + (j-1)*3)}.jpg')
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(2 + (j-1)*3)}.jpg')
                            break
                        elif [x] == ['13']:
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(1 + (j-1)*3)}.jpg')
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(3 + (j-1)*3)}.jpg')
                            break
                        elif [x] == ['23']:
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(2 + (j-1)*3)}.jpg')
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(3 + (j-1)*3)}.jpg')
                            break
                        elif [x] == ['123']:
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(1 + (j-1)*3)}.jpg')
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(2 + (j-1)*3)}.jpg')
                            selectedPhotosPaths.append(f'photo{i}/photo1-{(3 + (j-1)*3)}.jpg')
                            break
                        elif [x] == ['!']:
                            break
                        time.sleep(5)

            print('Program Done')
            return selectedPhotosPaths
        time.sleep(3)
     

def main():
    api_token = "YOUR API TOKEN"
    api_url = f"https://api.telegram.org/bot{api_token}/getUpdates"
    chat_id = 'YOUR CHAT ID'

    get_photos(api_url, api_token)

    editing()
    combining()

    finalImages = selecting_photos(api_url, api_token, chat_id)
    for i in finalImages:
        uploudImage(i, api_token, chat_id)


if __name__=='__main__':
    main()
