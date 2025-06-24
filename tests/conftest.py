import sys
from pathlib import Path
import pytest

from annotation_parser.adapters.labelme_adapter import LabelMeAdapter

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="module")
def minimal_labelme_json():
    return {
        "shapes": [
            {
                "label": "person",
                "points": [[1, 2], [3, 4]],
                "shape_type": "rectangle"
            }
        ]
    }


@pytest.fixture(scope="module")
def minimal_shape():
    from annotation_parser.shape import Shape
    from annotation_parser.public_enums import ShapeType
    return Shape(label="person", coords=[[1.0, 2.0], [3.0, 4.0]], type=ShapeType.RECTANGLE)


# Параметризация для всех адаптеров, расширяйте список!
@pytest.fixture(params=[("labelme", "LabelMeAdapter", "minimal_labelme_json")])
def adapter_under_test(request):
    name, class_name, json_fixture = request.param
    module = __import__("annotation_parser.adapters.labelme_adapter", fromlist=[class_name])
    adapter_cls = getattr(module, class_name)
    json_data = request.getfixturevalue(json_fixture)
    minimal_shape = request.getfixturevalue("minimal_shape")
    return adapter_cls, json_data, minimal_shape
