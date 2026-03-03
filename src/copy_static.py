import os, shutil, logging



logging.basicConfig(filename="src/copy_src_to_dest_log.txt", level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def copy_src_to_dest(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
        logger.info(f'Replicated directory: {dest}')
    
    for item in os.listdir(src):
        source_item = os.path.join(src, item)
        destination_item = os.path.join(dest, item)

        if os.path.isdir(source_item):
            logger.info(f'Entering directory: {source_item}')
            copy_src_to_dest(source_item, destination_item)
        else:
            shutil.copy2(source_item, dest)
            logger.info(f'Copied file: {source_item} to {dest}')