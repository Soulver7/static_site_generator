import os, shutil, sys

from copy_static import copy_src_to_dest
from page_generator import generate_pages_recursive



def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "" else "/"

    print("Deleting existing docs directory...")
    if os.path.exists("docs"):
        shutil.rmtree("docs")

    print("Copying static files to new docs directory...")
    copy_src_to_dest("./static", "./docs")

    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


main()