from pydantic import BaseModel
import os.path
import json
import hashlib

users_path = 'data/users.json'



class UserSchema(BaseModel):
    username: str
    email: str
    password:  str

def is_file_exist() -> bool:
    return os.path.exists(users_path)

def is_existing_user( email_data: str ) -> bool:
    users_data = get_users();
    if not users_data:
        return False
    return any(email_data in user for user_dict in users_data for user in user_dict.values())

def password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_users():
    isExistFile = is_file_exist()
    if isExistFile:
        with open(users_path, 'r') as file:
            return json.load(file);
    return None;

def save_user(user: dict) -> bool:
    
    with open(users_path, 'r+') as file:
        file_data = get_users();
        
        if type(file_data) == 'NoneType':
            file_data = [];
            
        file_data.append(user)
        json.dump(file_data, file, indent=4)
    return True;

def handleLogin( formData ) -> bool:
    email_data = str(formData['email']);
    password_data = password_hash(formData['password'])

    isExisting = is_existing_user(email_data=email_data);
    if isExisting:
        users_data = get_users();
        if(users_data):
            for user in users_data:
                if user["email"] == email_data and user["password"] == password_data:
                    return True
    return False;




