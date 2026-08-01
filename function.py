"""
Veo 3 Storyboard Station
function.py
"""
import config
from excel_manager import get_type_scenario, load_scenario_data, get_template_dict
from prompt_builder import normalize_list, build_prompt, build_filename

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

        reference_list

        final_prompt = build_prompt(
            scene["scene_id"],
            template,
            scene["prompt_core"],
            character_list,
            reference_list
        )

        scene_data.append({

            "scene_id": scene["scene_id"],

            "final_prompt": final_prompt,

            "character_list": character_list,

            "reference_list": reference_list,

            "file_name": build_filename(final_prompt)
        })

    return scene_data


