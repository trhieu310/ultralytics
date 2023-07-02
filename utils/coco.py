import numpy as np
import json
import datetime

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

class Segment2COCO:
    """
    This class to handle data extracted from the extractor and then store it in COCO json Format
    """
    def __init__(self, categories=None):
        """
        Args:
            categories (dict): Dictionary represent the labels
        """
        # Create empty data first
        # self.reference_json = reference_json
        self.coco_format = {
            "info": {
                "year": 2023,
                "version": "1.0",
                "description": "Annotated of Segmented images",
                "contributor": "",
                "date_created": str(datetime.datetime.now())
            },
            "licences": [
                {
                    "id": 1,
                    "name": "",
                    "url": ""
                }
            ],
            "categories": [],   # [{}]
            "images": [],     #  [{}]
            "annotations": []  # [{}]
        }
        # Then create the category part
        if categories is None:
            categories = {1: "Illustration", 2: "Text", 3: "ScienceText"}
        self._set_category_annotation(categories)

    def _get_img_id_by_name(self, name):
        pass


    def _set_category_annotation(self, category_dict):
        """
        Expect category_dict as {1: "Illustration", 4: "Text", 12: "ScienceText"}
        """
        category_list = []
        for key, value in category_dict.items():
            category = {
                "id": key,
                "name": value,
                "supercategory": "",
            }
            category_list.append(category)
        self.coco_format["categories"] = category_list
    def add_an_image_annotation(self, file_name, width, height, image_id):
        """
        Add image information inside the coco format
        """
        image = {
            "file_name": file_name,
            "height": height,
            "width": width,
            "id": image_id
        }
        self.coco_format["images"].append(image)

    # This can be add during the extraction phase.
    def add_an_annotation_format(self, bbox, segmentation, image_id, category_id, annotation_id, score, polyon_area=None, attributes={}):
        area = polyon_area
        annotation = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": bbox,
            "segmentation": segmentation,
            "area": area,
            "score": score,
            "iscrowd": 0
        }
        if len(attributes.keys()) > 0:
            temp = {}
            for k in attributes.keys():
                temp[k] = attributes.get(k)
            annotation["attributes"] = temp
        self.coco_format["annotations"].append(annotation)

    def save(self, path_to_file_name):
        with open(path_to_file_name, 'w', encoding='utf-8') as json_file:
            json.dump(self.coco_format, json_file, sort_keys=False, indent=4, ensure_ascii=False, cls=NpEncoder)