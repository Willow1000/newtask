import os
import sys
import re

from .Movement import Movement
from .MoveLeaf import MoveLeaf
from .MoveComposition import MoveComposition
from .PressHighlightLeaf import PresHighlightLeaf

projects_path = os.environ["CLIENT_MANAGER_PROJECTS_PATH"]
runescape_actions_path = os.path.join(projects_path, "runescape_actions")
sys.path.append(runescape_actions_path)

from runelite_cv.runescape_cv.runescape_cv import to_bgr_from_rgb, to_numeral_tuple_from_hex


def parsecolor(path: str, map_colors: dict) -> dict[str, str]:
    """
    every color in the output map (map_colors) is in BGR format
    """
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            map_colors[line.split(":")[0].strip()] = line.split(":")[1].strip()
    return map_colors_to_bgr_map_colors(map_colors)


def map_colors_to_bgr_map_colors(map_colors):
    new_map_colors = {}
    for id_assigned_to_color, color in map_colors.items():
        tup = to_numeral_tuple_from_hex(color)
        new_map_colors[id_assigned_to_color] = tup
    return new_map_colors


def parseAllMovementFiles(path: str, map_colors: dict) -> list[Movement]:
    """
    returns a list of steps
    """
    ignore_file_list = [
        "HOW_TO_CREATE_MOVEMENTS",
    ]
    movements = []
    for file in os.listdir(path):
        if file in ignore_file_list:
            continue
        movements.append(parseFile(os.path.join(path, file), map_colors))
    return movements


def parseFile(filepath: str, map_colors: dict) -> Movement:
    """
    returns a list of steps
    """
    # if the file starts with a filename, it's a composition file
    # if the file starts with a initial color, it's a leaf file
    # if the file starts with a final color, it's a special leaf file
    with open(filepath, "r") as file:
        line = file.readline().strip()
        if line.startswith("InitialColor:"):
            return parseLeaf(filepath, map_colors)

        elif line.startswith("Composition"):
            return parseComposition(filepath, map_colors)

        elif line.startswith("FinalColor:"):
            return parseSpecialLeaf(filepath, line, map_colors)
        else:
            raise ValueError(f"Erro ao processar o arquivo {filepath}.")


def parseComposition(file_path: str, map_colors: dict) -> MoveComposition:
    leafs = []
    print("Parsing composition file: " + file_path)

    base_dir = os.path.dirname(file_path)

    # Open the file and read it line by line

    with open(file_path, "r") as file:
        for line in file:
            next_file = line.strip()
            if next_file.endswith(".txt"):
                next_file_path = os.path.join(base_dir, next_file)
                # Call parseLeaf for each line
                leaf = parseLeaf(
                    next_file_path, map_colors
                )  # this can be a compositionFile or a LeafFile, we will handle that in parseLeaf
                if isinstance(leaf, MoveComposition):
                    leafs.extend(leaf.getMovements())
                else:
                    leafs.append(
                        leaf
                    )

    composition = MoveComposition(file_path)
    composition.addAllMovements(leafs)

    print("\n------------------->\nComposition Summary:\n")
    for leaf in leafs:
        if isinstance(leaf, PresHighlightLeaf):
            print(f"PressHighlightLeaf: {leaf.getId()}")
        else:
            print(f"Leaf: {leaf.getId()}")
    print("\n<-------------------")
    return composition


def parseSpecialLeaf(filepath: str, first_line: str, map_colors: dict) -> PresHighlightLeaf:
    with open(filepath, "r") as file:
        line = file.readline().strip()
        if line.startswith("FinalColor:"):
            final_color = line.split(":")[1].strip()
    if final_color:
        try:
            final_color = map_colors[final_color]
        except:
            print(f"Cor final {final_color} não encontrada.")
        return PresHighlightLeaf(final_color, filepath)


def parseLeaf(filepath: str, map_colors: dict):
    print("Parsing leaf file: " + filepath)
    initial_color = None
    final_color = None
    color_pattern = []

    with open(filepath, "r") as file:
        lines = file.readlines()
        first_line = lines[0].strip()
        if first_line.startswith("Composition"):
            # If it's a composition file, call parseComposition
            composition = parseComposition(filepath, map_colors)
            return composition

        if first_line.startswith("FinalColor:"):
            return parseSpecialLeaf(filepath, first_line, map_colors)

        for line in lines:
            line = line.strip()

            # Verifica e extrai a cor inicial
            if line.startswith("InitialColor:"):
                initial_color = line.split(":")[1].strip()

            # Verifica e extrai a cor final
            elif line.startswith("FinalColor:"):
                final_color = line.split(":")[1].strip()

            # Verifica e extrai o padrão de cores
            elif line.startswith("ColorPattern"):
                # Extrai o padrão de cores entre os parênteses
                pattern_match = re.search(r"\((.*?)\)", line)
                if pattern_match:
                    color_pattern = pattern_match.group(1).split(",")
    if initial_color and final_color and color_pattern:
        try:
            initial_color = map_colors[initial_color]
        except:
            raise ValueError(f"Cor inicial {initial_color} não encontrada.")
        try:
            final_color = map_colors[final_color]
        except:
            print(f"Cor final {final_color} não encontrada.")

    if initial_color and final_color and color_pattern:
        return MoveLeaf(
            initial_color, final_color, color_pattern, -1, filepath
        )  # movementId = filepath
    else:
        raise ValueError(f"Erro ao processar o arquivo {filepath}.")


