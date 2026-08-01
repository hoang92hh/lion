"""
==========================================================
Veo 3 Storyboard Station
asset_manager.py
----------------------------------------------------------
Asset Management
==========================================================
"""
import re
from excel_manager import get_scenario_data_by_type


class AssetManager:

    def __init__(self, scenario_type):

        self.asset_map = {}
        self.load_asset_map(scenario_type)

    def load_asset_map(self, scenario_type):

        scene_list = get_scenario_data_by_type(scenario_type)

        for scene in scene_list:
            self.asset_map[scene["scene_id"]] = scene["file_name"]

    def add_asset(self, scene_id, file_name):

        if scene_id and file_name:
            self.asset_map[scene_id] = file_name

    def replace_reference(self, reference_list):

        if not reference_list:
            return []

        result = []

        for ref in reference_list:

            result.append(
                self.asset_map.get(ref, ref)
            )

        return result

    def get_asset(self, scene_id):

        return self.asset_map.get(scene_id)


    def replace_text(self, text):

        for key, value in self.asset_map.items():
            pattern = rf'"\s*{re.escape(key)}\s*"'
            text = re.sub(pattern, f'"{value}"', text)

        return text