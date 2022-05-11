import os
from src.common.globals import static_dir


class FileHelper:
    @staticmethod
    def upload_file(file_name, file):
        extension = FileHelper.extract_extension(file.filename)
        file_path = file_name + '.' + extension
        file.save(os.path.join(static_dir, file_path))

        return file_path

    @staticmethod
    def extract_extension(file_name):
        file_content = file_name.split('.')
        extension = file_content[-1]
        return  extension


