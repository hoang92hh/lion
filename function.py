"""
Veo 3 Storyboard Station
function.py
"""
import config
from excel_manager import get_type_scenario, load_scenario_data, get_template_dict
from prompt_builder import normalize_list, build_command


# ==========================================================
# Build Scene
# ==========================================================

def build_scene(scenario_type):

    sheet = get_type_scenario(scenario_type)

    scenario_list = load_scenario_data(sheet)

    template_dict = get_template_dict()

    scene_data = []

    for scene in scenario_list:

        if scene["status_time"] == config.STATUS_DONE:
            continue

        template = template_dict.get(
            str(scene["template_key"]).strip().lower(),
            ""
        )

        character_list = normalize_list(
            scene["character_list"]
        )

        reference_list = normalize_list(
            scene["reference_list"]
        )

        command_List = build_command(
            scene["scene_id"],
            template,
            scene["prompt_core"],
            character_list,
            reference_list
        )

        scene_data.append({

            "scene_id": scene["scene_id"],

            "command": command_List,

            "character_list": character_list,

            "reference_list": reference_list,

            "file_name": scene["scene_id"]+ "is creating"
        })

    return scene_data

def command_to_prompt(commands):

    prompt = ""

    for command in commands:

        cmd_type, value = command.split("||", 1)

        if cmd_type in ("TEXT", "CHARACTER", "REFERENCE"):
            prompt += value

    return prompt


