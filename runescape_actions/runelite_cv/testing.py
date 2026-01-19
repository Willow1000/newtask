import sys
import fire
import os
import cv2
import numpy as np
from matplotlib.collections import EllipseCollection
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
sys.path.append(os.path.join(os.getcwd(), 'LocallyAvailableActionTooling'))
from runelite_cv.runescape_cv.runescape_cv import extract_objects, get_region_by_color


def draw_cross(image_path, output_path, match_coords, color):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image from {image_path}")
        return
    x, y = match_coords
    # Define the color for the cross (BGR format in OpenCV, so (0, 0, 255) is red)
    # Define the thickness of the cross
    thickness = 3
    # Draw a cross at the match_coords
    cv2.drawMarker(img, (x, y), color, markerType=cv2.MARKER_CROSS, markerSize=20, thickness=thickness)
    # Save the modified image to a new path
    cv2.imwrite(output_path, img)
    msg = f"Image with cross saved as {output_path}\n"  
    print(msg)
    return msg


def draw_all_for_all_iters(image_path, output_image_path, objs, iteration, x_min, x_max, y_min, y_max, center):
    color = (0, 0, 255)
    draw_cross(image_path, output_image_path, center, color) 
    min = (x_min, y_min)
    color = (0, 255, 0)
    draw_cross(output_image_path, output_image_path, min, color)
    max = (x_max, y_max)
    color = (255, 0, 0)
    draw_cross(output_image_path, output_image_path, max, color)
 
 
def draw_all(image_path, output_image_path, objs, iteration, x_min, x_max, y_min, y_max, center):
    # draw all crosses in one image
    if iteration == 0:
        color = (0, 0, 255)
        draw_cross(image_path, output_image_path, center, color) 
        min = (x_min, y_min)
        color = (0, 255, 0)
        draw_cross(output_image_path, output_image_path, min, color)
        max = (x_max, y_max)
        color = (255, 0, 0)
        draw_cross(output_image_path, output_image_path, max, color)
    else:
        color = (0, 0, 255)
        draw_cross(output_image_path, output_image_path, center, color) 
        min = (x_min, y_min)
        color = (0, 255, 0)
        draw_cross(output_image_path, output_image_path, min, color)
        max = (x_max, y_max)
        color = (255, 0, 0)
        draw_cross(output_image_path, output_image_path, max, color)
         

class Testing():
    def __init__(self):
        # arguments from the command line go in here, you name the arguments in the command line
        #  the same way you name them here in the __init__ function
        pass

    def highlight(self, image_path, output_image, color_list=[ ( 255, 0, 0 ) ], add_debug_info=True, full_output_image=None) -> str: 
        '''
        default color for test is blue (bgr format)
        :arg color_list: remember this only accepts bgr format color 
        :return debug string info
        '''
        debug_str = ""
        image = cv2.imread(image_path)
        print(f"color_list bgr: {color_list}")
         
        # this is the actual test
        objs, black_copy_with_all_the_contours = extract_objects(image, color_list, add_debug_info=add_debug_info)

        if add_debug_info:
            plt.imshow(black_copy_with_all_the_contours, cmap='gray')
            plt.title('black image with all the contours')
            plt.axis('off')
            plt.show()
        # print(objs)
        iteration = 0
        output_image_path_base = output_image
        output_image_path = f'{output_image_path_base}/all.png'
        if objs:
            for i in objs:
                x_min, x_max, y_min, y_max, width, height, center, axis = i
                
                # makedir with path as name
                output_image_path_for_current_iteration = f'{output_image_path_base}/image_num_{iteration}'
                os.makedirs(f'{ output_image_path_for_current_iteration }', exist_ok=True)

                # draw for current
                output_image_path_for_current_iteration = f'{output_image_path_for_current_iteration}'
                output_image_all = f'{output_image_path_for_current_iteration}/all.png'
                color = (0, 0, 255)
                draw_cross(image_path, output_image_all, center, color) 
                min = (x_min, y_min)
                color = (0, 255, 0)
                draw_cross(output_image_all, output_image_all, 
                           min, color)
                max = (x_max, y_max)
                color = (255, 0, 0)
                draw_cross(output_image_all, output_image_all,
                           max, color)

                # draw for current min
                output_image_min = f'{output_image_path_for_current_iteration}/min.png'
                min = (x_min, y_min)
                color = (0, 255, 0)
                draw_cross(image_path, output_image_min, min, color)

                # draw for current center
                output_image_center = f'{output_image_path_for_current_iteration}/center.png'
                color = (0, 0, 255)
                draw_cross(image_path, output_image_center, center, color) 

                # draw for current max
                output_image_max = f'{output_image_path_for_current_iteration}/max.png'
                max = (x_max, y_max)
                color = (255, 0, 0)
                draw_cross(image_path, output_image_max,
                           max, color)
                draw_all(image_path, output_image_path, objs, iteration, x_min, x_max, y_min, y_max, center)
                if full_output_image is not None:
                    new_out_image_path = f'{output_image_path_base}/../{full_output_image}_iter_{iteration}.png' 
                    draw_all_for_all_iters(image_path, new_out_image_path, objs, iteration, x_min, x_max, y_min, y_max, center)
                    debug_str += f"image:{new_out_image_path} \n"
                    new_out_image_path = f'{output_image_path_base}/{full_output_image}_iter_{iteration}.png'
                    draw_all_for_all_iters(image_path, new_out_image_path, objs, iteration, x_min, x_max, y_min, y_max, center)
                    debug_str += f"image:{new_out_image_path} \n"
                else:
                    debug_str += "full image was None\n"
                iteration += 1
        else:
            print("No highlights found in the image")
            debug_str += "No highlights found in the image\n"
            height, width = 100, 100
            black_image = np.zeros((height, width, 3), dtype=np.uint8)
            cv2.imwrite(output_image_path, black_image)
            if full_output_image is not None:
                new_out_image_path = f'{output_image_path_base}/../{full_output_image}_iter_{iteration}.png'
                cv2.imwrite(new_out_image_path, black_image)
                new_out_image_path = f'{output_image_path_base}/{full_output_image}_iter_{iteration}.png'
                cv2.imwrite(new_out_image_path, black_image)
        return debug_str


    def get_blue_on_screen(self, image_path, output_image, is_showing_images=False):
        output_image_path = f'{output_image}//test.png'
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Unable to read the image file.")
            return
        color = [255, 255, 0]
        blue_mask = get_region_by_color(image, color)
        # Apply the mask to get only blue regions
        blue_regions = cv2.bitwise_and(image, image, mask=blue_mask)
        if is_showing_images:
            cv2.imshow("Blue Regions", blue_regions)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # print(region) 
        cv2.imwrite(output_image_path, blue_regions)
        # draw_cross(image_path, output_image_path, center)

    def grab_all_regions(self):
        pass


if __name__ == "__main__":
    '''
    example on how you call this with:
        python testing.py --arg1='value1' --you_can_have_more_arguments_here="value1,value2" main_test
    more on this on fire documentation
    there is a placeholder arg1 and arg2
    copy/paste this file for every new function you are testing
    '''
    fire.Fire(Testing)

