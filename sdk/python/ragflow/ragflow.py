#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import os
from abc import ABC
import requests


class RAGFLow(ABC):
    def __init__(self, user_key, base_url):
        self.user_key = user_key
        self.base_url = base_url

    def create_dataset(self, name):
        endpoint = f'{self.base_url}/api/v1/datasets'
        data = {'name': name}
        response = requests.post(endpoint, json=data)
        if response.status_code == 200:
            res = response.json()
            return {'Name': res.get('Name'), 'Id': res.get('Id')}
        else:
            return None

    def delete_dataset_by_id(self, dataset_id):
        """delete a dataset by id"""
        endpoint = f"{self.base_url}/api/v1/dataset/{dataset_id}"
        response = requests.delete(endpoint)
        if response.status_code == 200:
            return True
        else:
            return False

    def delete_dataset(self, name):
        """delete a dataset"""
        datasets = self.list_dataset()

        dataset_to_delete = None
        for dataset in datasets:
            if dataset["name"] == name:
                dataset_to_delete = dataset
                break

        # find the dataset
        if dataset_to_delete:
            dataset_id = dataset_to_delete["id"]
            result = self.delete_dataset_by_id(dataset_id)
            if result:
                print(f"You have deleted the dataset: '{name}'！")
                return True
            else:
                print(f"Failed to delete the dataset '{name}' ！")
                return False
        else:
            print(f"There is no '{name}' ！")
            return False

    def list_dataset(self):
        endpoint = f"{self.base_url}/api/v1/dataset"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()['datasets']
        else:
            return None

    def get_dataset(self, dataset_id):
        endpoint = f"{self.base_url}/api/v1/dataset/{dataset_id}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def update_dataset(self, dataset_id, params):
        endpoint = f"{self.base_url}/api/v1/dataset/{dataset_id}"
        response = requests.put(endpoint, json=params)
        if response.status_code == 200:
            return True
        else:
            return False

    # --------------------file management--------------
    def create_directory(self, path):
        pass

    def delete_directory(self, path):
        pass

    def move_directory(self, old_path, new_path):
        pass

    def get_directory(self, path):
        """return attributes about dir"""
        pass

    def copy_directory(self, new_path):
        pass

    def update_directory(self, path, new_info):
        pass

    # a file
    def create_file(self, file, kb_id):
        """return file_id"""
        pass

    def get_file(self, file_id):
        pass

    def list_file(self, kb_id, page_size, page):
        pass

    def update_file(self, file_id, file_name, enable, chunk_method, chunk_token_number, use_raptor):
        pass

    def delete_file(self, file_id):
        pass

    def download_file(self, file_id):
        pass

    def move_file(self, old_path, new_path):
        pass

