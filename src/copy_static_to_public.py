import os
import shutil


def copy_static_to_public():
    public_dir = "./public"
    static_dir = "./static"

    # clean up existing public files
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    __copy_folder_content(static_dir, public_dir)


def __copy_folder_content(source_dir, target_dir):
    os.mkdir(target_dir)
    for entry in os.listdir(source_dir):
        entry_path = os.path.join(source_dir, entry)
        target_path = os.path.join(target_dir, entry)
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, target_path)
        else:
            __copy_folder_content(entry_path, target_path)
