from config import *
from typing import List
from hashlib import sha256
import os
from werkzeug.datastructures import FileStorage
import subprocess

uid = os.getuid()
gid = os.getgid()


def get_compile_dir(file: bytes) -> str:
    hash_key = sha256(file).hexdigest()
    print(f"{hash_key=}")
    # make it shorter
    hash_key = hash_key[:16]
    path = f"{DIST_DIR}/{hash_key}"
    # create directory recursively
    os.makedirs(path, exist_ok=True)
    return path


def save_file(file: FileStorage, path: str) -> str:
    save_name = f"src.{file.filename.split('.')[-1]}"
    if not os.path.exists(f"{path}/{save_name}"):
        file.stream.seek(0)
        file.save(f"{path}/{save_name}")
    return save_name


def get_result_files(dir: str) -> List[str]:
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".dump") or file.endswith(".data"):
                file_list.append(os.path.join(root, file))
    return file_list


def compile(file: FileStorage, march: str, target: str) -> list[str]:
    dir_path = get_compile_dir(file.stream.read())
    save_filename = save_file(file, dir_path)  # only name, without path
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{COMPILER_PATH}:/app",
            "-v",
            f"{dir_path}:/app/src",
            "-w",
            "/app",
            "--user",
            f"{uid}:{gid}",
            DOCKER_IMAGE,
            "make",
            f"MARCH_STRING={march}",
            f"TARGET={target}",
            f"SRC_FILE=src/{save_filename}",
        ],
        check=True,
        timeout=COMPILE_TIMEOUT,
    )
    return get_result_files(dir_path)
