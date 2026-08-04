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

    def resolve_command(self, commands):

        resolved_commands = []

        for command in commands:

            cmd_type, value = command.split("||", 1)

            if cmd_type == "REFERENCE":
                value = self.asset_map.get(value, value)

            resolved_commands.append(
                f"{cmd_type}||{value}"
            )

        return resolved_commands

    def get_asset(self, scene_id):

        return self.asset_map.get(scene_id)
