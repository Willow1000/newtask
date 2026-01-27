import base64
import os

from screenshot_tool_lib import load_image_from_file_to_bytes, \
 image_encode_to_send_to_network, \
 recreate_image_from_bytes
from screenshot_tool_lib import template_matching, features_matching
from enum import Enum

"""
purpose is to:
 quickly verify if an image exists in a larger base image, or if it exists across several other images

 in a way it does the same as submitting to the discord server, but locally
  kind of a local test_actions, where you can test if the 'check' or 'verify' components 
   exist in your 'test' components image
"""


class MatchingAlgorithm(Enum):
    FEATURES_MATCH = 'FEATURES_MATCH'
    TEMPLATE_MATCH = 'TEMPLATE_MATCH'


class InvalidAlgorithmStringError(Exception):
    pass
     
 
def matching_algorithm_from_string(algorithm_str: str) -> MatchingAlgorithm:
    try:
        return MatchingAlgorithm[algorithm_str.upper()]
    except KeyError:
        raise InvalidAlgorithmStringError(f"Invalid matching algorithm: {algorithm_str}")

 
def run_algorithm_from_type(algorithm_received, icon_image, background_img_obj, precision):
    algorithm: MatchingAlgorithm = matching_algorithm_from_string(algorithm_received)
    if algorithm == MatchingAlgorithm.FEATURES_MATCH:
        return features_matching(icon_image, background_img_obj, precision=precision)
    elif algorithm == MatchingAlgorithm.TEMPLATE_MATCH:
        return template_matching(icon_image, background_img_obj, precision=precision)
     

def compare_icon_to_image_list(
    icon_image,
    background_images_to_find_icon_in,
    algorithm: MatchingAlgorithm = MatchingAlgorithm.TEMPLATE_MATCH,
    precision=0.8,
): 
    '''
    icon_image: path to the image that you want to test
    background_images_to_find_icon_in: list of paths to the test images that you want to test against
    return: a report string and a tuple with: (match_result_x, match_result_y, precision)
    '''
    report = ''
    result = None
    for background_image in background_images_to_find_icon_in:
        img_byte_array = load_image_from_file_to_bytes(background_image)
        encoded_img = image_encode_to_send_to_network(img_byte_array)
        img_b64_str = encoded_img
        img_bytes = base64.b64decode(img_b64_str)
        background_img_obj = recreate_image_from_bytes(img_bytes)

        match_result_x, match_result_y, precision = run_algorithm_from_type(algorithm, icon_image, background_img_obj, precision) 
        print("comparing images from paths:")
        print('icon image path:')
        print(icon_image)
        print('background image path:')
        print(background_image)
        match_result = (match_result_x, match_result_y)
        result = (match_result_x, match_result_y, precision)
        background_image_summarized = background_image.split("/")[:-2]
        background_image_summarized = "/".join(background_image_summarized)
        background_image_name = '/'.join(background_image.split("/")[-2:])
        icon_image_summarized = icon_image.split("/")[:-2]
        icon_image_name = '/'.join( icon_image.split("/")[-2:] )
        icon_image_summarized = "/".join(icon_image_summarized)
        report += f"background image name: { background_image_name }\nicon image name: { icon_image_name }\n"
        report += f"precision: {precision}\nposition on screen: {match_result}\n\n"
        print()
        print("precision")
        print(precision)
        print("match_result (the coordinates found where the icon is located)")
        print(match_result)
        print()
    return ( report, result )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_icon_to_compare_path_list",
                        help="list of icons(smaller images) to compare against larger image",
                        required=True)
    parser.add_argument("--base_image_path",
                        help="path of single larger image that the smaller icons will be compared against",
                        required=True)
    # TODO verify all images in a list of actions

    args = parser.parse_args()
    
    base_image_path = args.base_image_path.replace("\\", "/")
    image_icon_to_compare_path_list = [k for k in args.image_icon_to_compare_path_list.replace("\\", "/").split(",")]
    compare_icon_to_image_list(base_image_path, image_icon_to_compare_path_list)



