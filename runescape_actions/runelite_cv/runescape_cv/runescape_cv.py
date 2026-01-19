"""
A set of computer vision utilities for use with RuneLite-based bots.
"""

from typing import List, NamedTuple 
import cv2
import numpy as np
import matplotlib.pyplot as plt

Point = NamedTuple("Point", x=int, y=int)


class InvalidColorsException(Exception):
    pass


def get_region_by_color(image: cv2.Mat, color, difference=3):
    '''
    by default this just compares the color to the same color with a default difference of 3
     this default difference hopefully is not too large as to not be too resource intensive
      a difference of 3 was set as default, from testing seems like a good idea
    color: BGR format
    difference: the difference between the color and the upper and lower bound that will be searched 
     on screen, the higher the difference the better the borders will be set, if the highlight 
      line is too thick, and the difference too low, then the line will be inside the object, 
       this makes sense because the line is thicker and fades out, therefore, it will be inside the 
        object, be careful with this
    '''
    color_x = int( color[0] )
    color_y = int( color[1] )
    color_z = int( color[2] )
    color_lower_b = ( color_x - difference, color_y - difference, color_z - difference )   
    color_upper_b = ( color_x + difference, color_y + difference, color_z + difference )  
    lower_color = np.array(color_lower_b)
    upper_color = np.array(color_upper_b)
    # Create a mask for blue color
    color_mask = cv2.inRange(image, lower_color, upper_color)
    # Display the result
    return color_mask


def to_bgr_from_rgb(color:tuple) -> tuple:
    """
    :color: hex color in bgr
    """
    return ( color[2], color[1], color[0] )


def to_numeral_tuple_from_hex(color:str) -> tuple:
    '''
    :color: color in hex format, simple hex string, ex: #FF0000 (or without the hash symbol (FF0000))
    :retuns: rgb tuple of ints, intead of tuple of hex strings
    '''
    color = color.lstrip('#')  # Remove hash symbol if exists
    lv = len(color)
    rgb_tuple = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    # Return in BGR order
    return rgb_tuple[::-1]
 
 
def extract_objects(image: cv2.Mat, color_list: list, add_debug_info=False) -> tuple:
    """
    color_list: list of colors to search for in the image, for backwards compatibility and ease of use, 
     it also accepts a single color as a string, this input color_list, the first elements in this 
      list are searched for first, and only the first color found is used
    Returns:
        FOR THE FIRST COLOR found in color_list it will return:
        a list of tuples with all the info to describe an object
         the info of the object returned: (x_min, x_max, y_min, y_max, width, height, center, axis)
        if no object for any colors was found it will return an empty list for objs, the calling 
         function must be able to handle this
    """
    for color in color_list:
        objs, black_copy_with_all_the_contours = extract_objects_for_color(image, color, add_debug_info)
        if objs:
            return objs, black_copy_with_all_the_contours
    return [], []


def extract_objects_for_color(image: cv2.Mat, color, add_debug_info=False, 
                              thickness_of_highlight_line=3) -> tuple:
    """
    Given an image of enclosed outlines, this function will extract information
    from each outlined object into a data structure.
    Args:
        image: The image to process.
        color: BGR format color of the delinear of the objects to extract
    Returns:
        a list of tuples with all the info to describe an object
         the info of the object returned: (x_min, x_max, y_min, y_max, width, height, center, axis)
        an image with all the contours drawn
        it returns a tuple of the above
    """
    # make sure the picture is in grayscale
    original_image = image.copy()
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    image = gray_image
    # Dilate the outlines
    kernel = np.ones((4, 4), np.uint8)
    mask = cv2.dilate(image, kernel, iterations=1)
    # If no objects are found, return an empty list
    if not np.count_nonzero(mask == 255):
        return []

    black_image = np.zeros(mask.shape, dtype="uint8")

    # Find the contours
    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    image = original_image

    # Create a mask for chosen color
    color_mask = get_region_by_color(original_image, color) 

    # Find contours in the mask
    contours, _ = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by size to detect thick lines
    line_contours = [cnt for cnt in contours if cv2.arcLength(cnt, True) > thickness_of_highlight_line]

    new_image = original_image.copy()
    # Draw contours on the original image for visualization
    for cnt in line_contours:
        cv2.drawContours(new_image, [cnt], -1, (0, 0, 255), 2)
    # hulls = [cv2.convexHull(cnt) for cnt in line_contours]

    # for objects in range(len(contours)):
    black_copy = black_image.copy()
    black_copy_with_all_the_contours = black_image.copy()

    # Extract the objects from each contoured object
    # objs: List[RuneLiteObject] = []
    if add_debug_info:
        black_copy_with_all_the_contours = cv2.morphologyEx(black_copy_with_all_the_contours, cv2.MORPH_OPEN, kernel)
        black_copy_with_all_the_contours = cv2.erode(black_copy_with_all_the_contours, kernel, iterations=2)

    objs = []
    for objects in range(len(line_contours)):
        if len(line_contours[objects]) > 2:
            # Fill in the outline with white pixels
            black_copy = black_image.copy()
            cv2.drawContours(black_copy, line_contours, objects, (255, 255, 255), -1)
            if add_debug_info:
                cv2.drawContours(black_copy_with_all_the_contours, line_contours, objects, (255, 255, 255), -1)
            kernel = np.ones((7, 7), np.uint8)
            black_copy = cv2.morphologyEx(black_copy, cv2.MORPH_OPEN, kernel)
            black_copy = cv2.erode(black_copy, kernel, iterations=2)
            if np.count_nonzero(black_copy == 255):
                indices = np.where(black_copy == [255])
                if indices[0].size > 0:
                    x_min, x_max = np.min(indices[1]), np.max(indices[1])
                    y_min, y_max = np.min(indices[0]), np.max(indices[0])
                    width, height = x_max - x_min, y_max - y_min
                    center = [int(x_min + (width / 2)), int(y_min + (height / 2))]
                    axis = np.column_stack((indices[1], indices[0]))
                    objs.append((x_min, x_max, y_min, y_max, width, height, center, axis))
    return objs, black_copy_with_all_the_contours


def is_point_obstructed(point: Point, im: cv2.Mat, span: int = 30) -> bool:
    """
    This function determines if there are non-black pixels in an image around a given point.
    This is useful for determining if an NPC is in combat (E.g., given the mid point of an NPC contour
    and a masked image only showing HP bars, determine if the NPC has an HP bar around the contour).
    Args:
        point: The top point of a contour (NPC).
        im: A BGR CV image containing only HP bars.
        span: The number of pixels to search around the given point.
    Returns:
        True if the point is obstructed, False otherwise.
    """
    try:
        crop = im[point[1] - span : point[1] + span, point[0] - span : point[0] + span]
        mean = crop.mean(axis=(0, 1))
        return mean != 0.0
    except Exception as e:
        print(f"Error in is_point_obstructed(): {e}")
        return True



