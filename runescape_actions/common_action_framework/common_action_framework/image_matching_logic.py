import cv2
import numpy as np
import base64
from PIL import ImageGrab
from PIL import Image


def image_b64_to_image_PIL_object(image_b64):
    from io import BytesIO
    from PIL import Image
    
    # Decode base64 string to bytes
    image_data = base64.b64decode(image_b64)
    
    # Create BytesIO object from the decoded data
    image_stream = BytesIO(image_data)
    
    # Open and return PIL Image object
    return Image.open(image_stream)

 
def template_matching(path_of_image_to_find, base_image, precision=0.6, offset=(0, 0)):
    '''
    :path_of_image_to_find: path to the image to find in the base_image, (this is just the path)
    :base_image: image where to find the image (given by path_of_image_to_find), this is a PIL image,
     not a path to the image, but the image itself
    :precision: float, 0.0 to 1.0, the higher the more precise the match must be, the more precise 
     the match is means: the more the image must be similar to the template image
    :offset: tuple with x and y offset to add to the final coordinates
    '''
    # image conversion from Image (PIL object) to opencv:
    #  https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    img_bgr = np.array(base_image)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2GRAY)  # this is meant to do the same as the previous 2 lines
    template = cv2.imread(path_of_image_to_find, cv2.IMREAD_GRAYSCALE)
    width, height = template.shape[::-1]
    
    method = cv2.TM_CCOEFF_NORMED
    res = cv2.matchTemplate(img_gray, template, method)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    middle_of_the_picture = (top_left[0] + int(width/2) - 1 + offset[0], top_left[1] + int(height/2) - 1 + offset[1])
    if max_val < precision:
        return -1, -1, max_val
    return middle_of_the_picture[0], middle_of_the_picture[1], max_val


