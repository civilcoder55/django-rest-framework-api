import uuid
import os


def gen_pic_file_path(instance, filename):
    """Generate file path for employees pictures"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('pictures/', filename)
