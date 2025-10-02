import os
import argparse
import shutil
from pathlib import Path
from PIL import Image

TOPOMAP_IMAGES_DIR = "../topomaps/images"

def remove_files_in_dir(dir_path: str):
    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

def main(args: argparse.Namespace):
    topomap_name_dir = os.path.join(TOPOMAP_IMAGES_DIR, args.dir)

    if not os.path.isdir(topomap_name_dir):
        os.makedirs(topomap_name_dir)
    else:
        print(f"{topomap_name_dir} already exists,  Removing previous images...")
        remove_files_in_dir(topomap_name_dir)

    images = sorted([p for p in Path(args.input_dir).iterdir() if p.is_file()])
    images = images[args.start_idx : args.end_idx]

    i = 0
    j = 0

    while True:
        img = Image.open(images[j])
        img.save(os.path.join(topomap_name_dir, f"{i}.png"))
        i += 1
        j += 10
        if (len(images) - j) < 10:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"script to generate topologiocal memory for testing NoMaD"
    )

    parser.add_argument(
        "--input-dir",
        default = None,
        type = str,
        help = "path to the input sequence"
    )

    parser.add_argument(
        "--start-idx",
        default = None,
        type = int,
        help = "the starting index of the trajectory for topological map"
    )

    parser.add_argument(
        "--end-idx",
        default = None,
        type = int,
        help = "the last index of the trajectory for topological map"
    )

    parser.add_argument(
        "--dir",
        "-d",
        default="topomap",
        type=str,
        help="path to topological map images in ../topomaps/images directory (default: topomap)",
    )

    args = parser.parse_args()

    main(args)