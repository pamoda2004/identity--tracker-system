from pathlib import Path
from app.utils.file_utils import load_json, save_json


class NamedRegistryService:
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.registry_path.exists():
            save_json(self.registry_path, [])

    def list_all(self):
        return load_json(self.registry_path, [])

    def add_named_person(self, unknown_id: str, name: str, signature: dict, image_path: str):
        data = self.list_all()

        for item in data:
            if item["unknown_id"] == unknown_id:
                item["name"] = name
                item["signature"] = signature
                item["image_path"] = image_path
                save_json(self.registry_path, data)
                return item

        new_item = {
            "unknown_id": unknown_id,
            "name": name,
            "signature": signature,
            "image_path": image_path,
        }
        data.append(new_item)
        save_json(self.registry_path, data)
        return new_item

    def find_best_match(self, current_features, matcher):
        data = self.list_all()

        best_item = None
        best_score = 0.0

        for item in data:
            score = matcher.compare(
                current_features,
                item["signature"],
                center_a=None,
                center_b=None,
                gait_a=None,
                gait_b=None,
            )
            if score > best_score:
                best_score = score
                best_item = item

        return best_item, best_score