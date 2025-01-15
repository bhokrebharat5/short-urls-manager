from pydantic import BaseModel
import os.path
import json
import uuid

urls_path = 'data/urls.json'

class UrlSchema(BaseModel):
    short_id: str
    url: str

def is_file_exist() -> bool:
    return os.path.exists(urls_path)

def load_file():
    isExistFile = is_file_exist()
    if isExistFile:
        with open(urls_path, 'r') as file:
            return json.load(file);

def add_url(url, email):
    get_urls = load_file();

    user_urls = get_urls.get(email,[]);

    short_id = str(uuid.uuid4())[:8];
    user_urls.append({"short_id": short_id, "url": url})

    get_urls[email] = user_urls
    save_url(get_urls)

    return True;

def save_url(urls: dict) -> bool:
    
    with open(urls_path, 'r+') as file:
        file_data = load_file();
        
        if type(file_data) == 'NoneType':
            file_data = {};
            
        file_data.update(urls)
        json.dump(file_data, file, indent=4)
    return True;

def save_all_data(data):
    with open(urls_path, "w") as f:
        json.dump(data, f, indent=4)
