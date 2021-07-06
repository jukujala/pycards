""" Upload input folder images to given deck in the gamecrafter.
"""
import os
import requests #Found at python-requests.org/
import time

from utils import absolute_file_paths

url="https://www.thegamecrafter.com/api" 
api_key_id = '' #Replace with yours
username = '' #Replace with yours
password = '' #Replace with yours
deck_id = '' # Replace with yours
INPUT_PATH = "./gamecrafter/processed_cards/"


def create_session(api_key_id, username, password):
  params = {'api_key_id': api_key_id, 'username' : username, 'password': password}
  response = requests.post(url + "/session", params=params)
  if response.status_code != 200:
    assert False, f"error accessing session: {response.json()}"
  session = response.json()['result']
  return session


def get_root_folder_id(session):
  params = {'session_id': session['id']}
  response = requests.get(url + "/user/" + session['user_id'], params=params)
  user = response.json()['result']
  root_folder_id = user['root_folder_id']
  return root_folder_id


def upload_file_to_deck(session, root_folder_id, deck_id, file_path):
  basename = os.path.basename(file_path)
  # upload the file first to root folder id
  params = {
    'name': basename,
    'folder_id': root_folder_id,
    'session_id': session['id'],
    'has_proofed_face': True,
  }
  files = { 'file': open(file_path,'rb') }
  response = requests.post(url + "/file", params=params, files=files)
  file_id = response.json()["result"]["id"]
  # add card to the given deck
  params = {
    'session_id': session['id'],
    'name': basename,
    'deck_id': deck_id,
    'quantity': 1,
    'face_id': file_id,
  }
  response = requests.post(url + "/card", params=params)
  assert response.status_code == 200


input_files = absolute_file_paths(INPUT_PATH)
input_files = [x for x in input_files if x.endswith('.png')]
session = create_session(api_key_id, username, password)
root_folder_id = get_root_folder_id(session)

for input_file in input_files:
  print(f"Processing file {input_file}")
  upload_file_to_deck(session, root_folder_id, deck_id, input_file)
  time.sleep(1.0)

