import os, shutil

from copy_static import copy_src_to_dest
from page_generator import generate_pages_recursive


def main():
    print("Deleting existing public directory...")
    if os.path.exists("public"):
        shutil.rmtree("public")

    print("Copying static files to new public directory...")
    copy_src_to_dest("./static", "./public")

    generate_pages_recursive("./content", "./template.html", "./public")



main()