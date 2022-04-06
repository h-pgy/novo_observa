import json
import os
from pathlib import Path



class DataLoader:

    def __init__(self):

        self.data_path = self.solve_data_path()
        self._collection_paths = self.list_collections()
        self.collections = self._collection_paths.keys()

    def solve_data_path(self):

        file_path = Path(__file__)
        parent = file_path.parent.parent.absolute()
        data_path = os.path.join('original_data', 'scraped_data')
        return os.path.abspath(os.path.join(parent, data_path))

    def list_collections(self):

        files = os.listdir(self.data_path)

        return {file.replace('.json', '') : os.path.join(self.data_path, file)
                for file in files}

    def open_collection(self, collection_name):

        if collection_name not in self._collection_paths:
            raise ValueError(f'Collection {collection_name} not available')

        col_path = self._collection_paths.get(collection_name)

        with open(col_path) as f:
            return json.load(f)

