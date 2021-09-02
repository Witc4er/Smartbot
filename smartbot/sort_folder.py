import re
import sys
import pathlib
import shutil

IMAGES = []
AUDIO = []
VIDEO = []
DOCUMENTS = []
ARCHIVES = []
FOLDERS = []
REGISTERED_EXTENSIONS = {
    'JPEG': IMAGES,
    'PNG': IMAGES,
    'JPG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO,
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCUMENTS,
    'DOCX': DOCUMENTS,
    'TXT': DOCUMENTS,
    'XLSX': DOCUMENTS,
    'PPTX': DOCUMENTS,
    'PDF': DOCUMENTS,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}


CYRILlIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєії'
TRANSLATION = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
               'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'y', 'e', 'u', 'ja', 'e', 'i', 'i')


TRANS = {}


for cs, trl in zip(CYRILlIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cs)] = trl
    TRANS[ord(cs.upper())] = trl.upper()


def normalize(name: str) -> str:
    trl_name = name.translate(TRANS)
    trl_name = re.sub(r'\W', '_', trl_name)
    return trl_name


def scan(folder: pathlib.Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('images', 'videos', 'documents', 'archives'):
                FOLDERS.append(item)
                scan(item)
        name, extension = item.stem, item.suffix
        new_name = normalize(name)
        new_item = folder / ''.join([new_name, extension])
        item.rename(new_item)
        if extension.upper().strip('.') in REGISTERED_EXTENSIONS:
            container = REGISTERED_EXTENSIONS[extension.upper().strip('.')]
            container.append(new_item)


def handle_image(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'images'
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/path.name)


def handle_audio(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'audio'
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/path.name)


def handle_video(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'video'
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/path.name)


def handle_archive(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'archive'
    name = path.stem
    target_folder.mkdir(exist_ok=True)
    archive_folder = target_folder / name
    archive_folder.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(str(path.absolute()), str(archive_folder.absolute()))
    except Exception:
        archive_folder.rmdir()
        return


def handle_documents(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'documents'
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / path.name)


def handle_folder(path: pathlib.Path):
    try:
        path.rmdir()
    except OSError:
        pass


def sort_folder(path):
    folder = pathlib.Path(path)
    print(f'Start in folder: "{folder}"')

    for file in IMAGES:
        handle_image(file, folder)

    for file in AUDIO:
        handle_audio(file, folder)

    for file in VIDEO:
        handle_video(file, folder)

    for file in DOCUMENTS:
        handle_documents(file, folder)

    for file in ARCHIVES:
        handle_archive(file, folder)

    for f in FOLDERS:
        handle_folder(f)


