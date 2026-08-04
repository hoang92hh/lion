"""
Veo 3 Storyboard Station
prompt_builder.py
"""
import config
import re

PLACEHOLDER = re.compile(r"\{(\d+)\.(\d+)\}")
# ==========================================================
# List
# ==========================================================

def normalize_list(value):

    if not value:
        return []

    if isinstance(value,list):
        return [str(item).strip() for item in value if str(item).strip()]

    value = str(value).replace("\n",",").replace(";",",")

    return [item.strip() for item in value.split(",") if item.strip()]


# ==========================================================
# Prompt
# ==========================================================


def replace_placeholder(prompt, index, asset_list):

    def replace(match):
        asset_index = int(match.group(1))
        return asset_list[asset_index] if asset_index < len(asset_list) else ""

    pattern = rf"\{{{index}\.(\d+)\}}"
    return re.sub(pattern, replace, prompt)


import re

def build_command(scene_id, template, prompt_core, character_list, reference_list):

    prompt = template.replace("{0}", prompt_core)

    commands = []
    last = 0

    pattern = r"\{(\d+)\.(\d+)\}"

    for match in re.finditer(pattern, prompt):

        # Text trước placeholder
        if match.start() > last:
            commands.append(
                f"TEXT||{prompt[last:match.start()]}"
            )

        asset_type = int(match.group(1))
        asset_index = int(match.group(2))

        if asset_type == 1:

            if asset_index >= len(character_list):
                raise IndexError(
                    f"Character index {asset_index} out of range."
                )

            commands.append(
                f"CHARACTER||{character_list[asset_index]}"
            )

        elif asset_type == 2:

            if asset_index >= len(reference_list):
                raise IndexError(
                    f"Reference index {asset_index} out of range."
                )

            commands.append(
                f"REFERENCE||{reference_list[asset_index]}"
            )

        else:
            raise ValueError(
                f"Unknown asset type: {asset_type}"
            )

        last = match.end()

    # Text cuối
    if last < len(prompt):
        commands.append(
            f"TEXT||{prompt[last:]}"
        )

    return commands



