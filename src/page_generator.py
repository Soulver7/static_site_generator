import os, sys

from block_markdown import markdown_to_html_node, extract_title
from pathlib import Path



def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path) as f:
        from_content = f.read()
    with open(template_path) as f:
        template_content = f.read()
    
    from_html_node = markdown_to_html_node(from_content)
    from_html = from_html_node.to_html()
    from_title = extract_title(from_content)

    full_content = template_content.replace("{{ Title }}", from_title).replace("{{ Content }}", from_html)
    full_content = full_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path) and os.path.dirname(dest_dir_path) != "":
        os.makedirs(dest_dir_path)
    
    with open(dest_path, "w") as f:
        f.write(full_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, item)
        dest_item = os.path.join(dest_dir_path, item)

        if os.path.isdir(src_item):
            generate_pages_recursive(src_item, template_path, dest_item, basepath)
        
        elif os.path.isfile(src_item) and src_item.endswith(".md"):
            dest_item = Path(dest_item).with_suffix(".html")
            generate_page(src_item, template_path, dest_item, basepath)
