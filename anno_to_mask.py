"""
Make mask for segmentation training from the annotation data of
MoNuSegTrainingData.

"""

import math
import argparse
from lxml import etree
from pathlib import Path
import numpy as np
import cv2


def read_annotation(path):
    """
    [Summary]
        Read annotation file into buffer and parse it.

    [Arguments]
        path {pathlib.PosixPath}
        -- path to the annotation file.

    [Returns]:
        annotations {list}
        -- list of annotations with each annotation encoded
           as numpy.ndarray values.
    """
    tree = etree.parse(str(path))
    regions = tree.xpath("/Annotations/Annotation/Regions/Region")
    annotations = []
    for region in regions:
        points = []
        for point in region.xpath("Vertices/Vertex"):
            points.append([math.floor(float(point.attrib["X"])),
                           math.floor(float(point.attrib["Y"]))])
        annotations.append(np.array(points, dtype=np.int32))
    return annotations


def read_img(path):
    """
    [Summary]
        Read an image file corresponding to the annotation file.

    [Arguments]
        path {pathlib.PosixPath}
        -- path to the image file.

    [Returns]
        height {int}
        -- height value of image encoded as numpy.ndarray values.

        width {int}
        -- height value of image encoded as numpy.ndarray values.
    """
    img = cv2.imread(str(path), 1)
    height, width = img.shape[0:2]
    return height, width


def to_mask(annotations, height, width):
    """
    [Summary]
        Make the mask image from the annotation and image sizes.

    [Arguments]
        # Described as above.

    Returns:
        mask {numpy.ndarray}
        -- mask image with each pixels {0, 1}.
    """
    mask = np.zeros([height, width], dtype=np.uint8)
    for annotation in annotations:
        mask = cv2.drawContours(mask, [annotation], 0, True, thickness=cv2.FILLED)
    return mask


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path")
    # TODO::convert to asap
    parser.add_argument("-c", "--convert_to_asap")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    dir_path = Path(args.dir_path)
    out_path = dir_path/"masks"
    out_path.mkdir(exist_ok=True)

    imgs = dir_path.glob("Tissue images/*.tif")

    for path in imgs:
        height, width = read_img(path)
        anno_path = str(dir_path/"Annotations"/path.stem) + ".xml"
        annotations = read_annotation(anno_path)
        mask = to_mask(annotations, height, width)
        cv2.imwrite(f"{str(out_path)}/{path.stem}.png",
                    mask, (cv2.IMWRITE_PXM_BINARY, 1))


if __name__ == '__main__':
    main()
