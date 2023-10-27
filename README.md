# PHOTO EDITOR VIA TELEGRAM API

Welcome to the official documentation for the `Photo Editor Bot` project! This project is a Python-based Telegram bot that allows users to edit and manipulate photos right within their Telegram chat. With a range of editing features and the power of Telegram's interface, this bot brings photo editing convenience to your fingertips.


## Instalation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all libraries

```bash
pip install requests
pip install pilgram
pip install Pillow
pip install python-telegram-bot
pip install asyncio
``` 

## Usage


Function **`download_image(token, file_path, br)`** is designed to download an image from a Telegram bot's server using its token and file path and save it as a local file

```python
def download_image(token, file_path, br):
    url = f'https://api.telegram.org/file/bot{token}/{file_path}'

    response = requests.get(url)
    if response.status_code == 200:
        with open(f'images//photo{br}.jpg', 'wb') as f:
            f.write(response.content)
``` 
<br/>

Function **`get_telegram_updates_text(api_url)`** is designed to retrieve text data from a specified API URL(Bot's log which have all information about every message that bot recieved)
``` python 
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
``` 
<br/>

Function **`extract_last_bot_command(text)`** is intended to extract the last bot command (commands that start with "/") from a JSON text containing all Telegram messages that bot recieved
``` python
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
``` 
<br/>

Function **`get_pictures_ids(telegram_updates_text)`** is designed to extract and collect file IDs of photos from Bots log provided as JSON text
``` python
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
``` 

<br/>

Function **`get_picture_path(pic_ids, bot_token)`** is designed to retrieve the file paths of pictures associated with their respective file IDs provided in the pic_ids list using Telegram bot api `getFile?` method
``` python
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
``` 
<br/>

Function **`get_photos(api_url, token)`** orchestrates a series of steps to retrieve and download photos from a specified Telegram API URL using a Telegram bot
``` python
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
``` 
<br/>

Function **`editing()`** performs a series of image editing tasks using the Pilgram library on a list of image files located in the "images" directory
``` python
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
``` 
<br/>

Function **`combining()`** is responsible for combining multiple photos into single combined images in batches of three. It performs this operation for each subfolder containing photos in a parent directory
``` python
def editing():
    ...
    <lines 141-203 in photoEditorMaster.py>
``` 
<br/>

Function **`lastMessage(date)`** when given a date, aims to extract the text of the last message sent to a Telegram bot before the specified date
``` python
def lastMessage(date):
    ...
    <lines 206-236 in photoEditMaster.py>
``` 
<br/>

Function **`uploudImage()`** is used to upload an image to a specified Telegram chat or group using a Telegram bot, and it does this asynchronously
``` python
async def send_image(bot, chat_ID, image_path):
    with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id=chat_ID, photo=InputFile(photo))


def uploudImage(path, api_token, chat_id):
    bot = telegram.Bot(token=api_token)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_image(bot, chat_id, path))
``` 
<br/>

Function **`selecting_photos(api_url, api_token, chat_id)`** continuously selects photos based on user input via Telegram messages and then uploads these selected photos to a specified chat or group
``` python
def selecting_photos(api_url, api_token, chat_id):
    ...
    <line 251-306 in photoEditorMaster.py>             
``` 
<br/>

Function **`main()`** serves as the entry point for the script, orchestrating a series of steps that involve retrieving, editing, combining, and selecting photos and then uploading them to a specified Telegram chat
``` python
def main():
    api_token = "YOUR API TOKEN"
    api_url = f"https://api.telegram.org/bot{api_token}/getUpdates"
    chat_id = 'YOUR CHAT ID'

    if not os.path.exists('images'):
        os.makedirs('images')
        
    get_photos(api_url, api_token)

    editing()
    combining()

    finalImages = selecting_photos(api_url, api_token, chat_id)
    for i in finalImages:
        uploudImage(i, api_token, chat_id)
``` 
<br/>

## Configuration
### 1. API Token
To interact with the Telegram Bot API, you must obtain an API token from the BotFather on Telegram. Once you have the token, replace `"YOUR API TOKEN"` in the `main()` function with your actual API token.

### 2. Chat ID
The chat_id is the unique identifier for the Telegram chat or group where the final images will be uploaded. Replace `"YOUR CHAT ID"` in the `main()` function with your actual chat or group ID.


## How to run

1. You need to send pictures to the bot in private chat following the bot command('/') with the number of how many pictures you sent to the bot
2. Run the code with the correct configurations
3. Go to the group chat that has your bot in it and write `/Start` 
4. Wait for the bot to send you combined images and then for each combined image you can write him command which picture you like(`/!`, `/1`, `/2`, `/3`, `/12`, `/13`, `/23`, `/123`)
5. When everything is done you will recieve all images in the telegram group chat

> **_NOTE:_**  Before running the file delete all folders that were previously created by the bot (photo{x} and photo{x}-combined) and delete all images saved inside the images folder

## Contact
If you have any questions, suggestions, or feedback about this project, feel free to reach out:

- **Name**: Borna Oršulić
- **GitHub**: [bornaorsulic](https://github.com/bornaorsulic)
- **Email**: borna.orsulic1@gmail.com
  <br/> <br/>
- **Name**: Luka Taslak
- **GitHub**: [Ltal3](https://github.com/ltal3)
