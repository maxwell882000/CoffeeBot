import os


def save_file(file, path, recreate=False):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    if recreate:
        if os.path.exists(path):
            os.remove(path)
    file.save(path)


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
