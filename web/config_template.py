import os

current_file_path = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_file_path)
compiler_directory = os.path.join(parent_directory, "compiler")

PORT = 8000
COMPILER_PATH = os.path.abspath(compiler_directory)
DIST_DIR = "/var/rvc-dist"
ROOT_URI = "/riscvc" # the path hiden by proxy
DIST_URI = f"{ROOT_URI}/dist"

DOCKER_IMAGE = "testcase:compile"

COMPILE_TIMEOUT = 20

