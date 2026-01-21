import argparse
import sys
import os
import shutil
import subprocess
import base64

import cv2
import numpy as np
import io
from PIL import ImageGrab
from PIL import Image


path = os.environ["PATH_CONTAINING_COMMON_ACTION_FRAMEWORK"]
sys.path.append(path)
from common_action_framework.common_action_framework.image_matching_logic import template_matching


try:
    docker_path = os.environ["DOCKER_PATH"]
except Exception as e:
    # windows default docker path
    if os.name == 'nt':
        # windows default docker path for all
        docker_path = "C:/Program Files/Docker/Docker/resources/bin/docker.exe" 
    else: 
        docker_path = "/usr/bin/docker"
     

def recreate_image_from_bytes(img_byte_arr):
    stream = io.BytesIO(img_byte_arr)
    img = Image.open(stream)
    return img


def image_encode_to_send_to_network(img_byte_array):
    img_b64 = base64.b64encode(img_byte_array)
    img_str_b64 = img_b64.decode('ascii')
    return img_str_b64
 

def load_image_from_file_to_bytes(filename):
    with open(filename, "rb") as f:
        img_byte_arr = f.read()
    return img_byte_arr


def record_image_to_bytes_windows(initial_x=1, initial_y=1, final_x=1279, final_y=1023):
    # according to: https://stackoverflow.com/questions/61537007/pillow-was-built-without-xcb-support
    x = initial_x
    y = initial_y
    w = final_x - initial_x
    h = final_y - initial_y
    img = ImageGrab.grab(bbox=(x, y, w, h))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def features_matching(path_of_image_to_find, base_image, precision=0.8, offset=(0, 0)):
    """
    Perform feature matching between two images using ORB detector and BFMatcher.

    Args:
        path_of_image_to_find (str): Path to the image to find.
        base_image (numpy.ndarray): Base image in which to find the test image (as a NumPy array).
        precision (float): Match ratio threshold between 0 and 1.
        offset (tuple): Not used in this implementation.

    Returns:
        tuple: (x, y, match_ratio)
        x, y (int): Coordinates of the center of the found image in the base image. Returns (-1, -1) if not found.
        match_ratio (float): The calculated match ratio.
    """
    # Read the test image in grayscale
    test_image = cv2.imread(path_of_image_to_find, cv2.IMREAD_GRAYSCALE)

    img_bgr = np.array(base_image)
    base_image_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Check if test image is loaded properly
    if test_image is None:
        raise IOError(f"Cannot open test image at {path_of_image_to_find}")

    # Initialize the ORB detector
    sift = cv2.SIFT_create()

    # Find keypoints and descriptors with SIFT in both images
    kp1, des1 = sift.detectAndCompute(base_image_gray, None)
    kp2, des2 = sift.detectAndCompute(test_image, None)

    # Check if descriptors are found in both images
    if des1 is None or des2 is None:
        print("No descriptors found in one of the images.")
        return (-1, -1, 0.0)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1  # Algorithm used for the FLANN matcher
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # How many times the tree(s) in the index should be recursively traversed

    # Create FLANN matcher
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Match descriptors using KNN matcher
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply Lowe's ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < precision * n.distance:
            good_matches.append(m)

    # Calculate match ratio
    total_matches = len(matches)
    match_ratio = len(good_matches) / total_matches if total_matches > 0 else 0.0
    print(f"Match ratio: {match_ratio:.2f}")

    # Minimum number of matches required to compute homography
    MIN_MATCH_COUNT = 10

    if len(good_matches) >= MIN_MATCH_COUNT:
        # Extract location of good matches in both images
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Compute homography
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        if M is not None:
            h, w = test_image.shape
            # Define corners of the test image
            pts = np.float32([[0, 0],
                              [0, h - 1],
                              [w - 1, h - 1],
                              [w - 1, 0]]).reshape(-1, 1, 2)
            # Map the corners to the base image
            dst = cv2.perspectiveTransform(pts, M)

            # Compute the center of the matched area in the base image
            center_point = np.mean(dst, axis=0).flatten()
            x, y = int(center_point[0]), int(center_point[1])
            print(f"Found match at position: ({x}, {y})")
            return (x, y, 1)
        else:
            print("Homography could not be computed.")
            return (-1, -1, match_ratio)
    else:
        print(f"Not enough good matches ({len(good_matches)}/{MIN_MATCH_COUNT}) to compute homography.")
        return (-1, -1, match_ratio)
 

def delete_any(path):
  """
  deletes anything on a given path
  should delete file, folder and all its contents recursively
  :param path:
  :return:
  """
  try:
    os.remove(path)
  except Exception as e:
    try:
      shutil.rmtree(path)
    except FileNotFoundError as e:
      print("not dir nor file, couldn't delete path: " + path)


def create_unexisting_dir(dirname_path):
  if not os.path.exists(dirname_path):
    os.mkdir(dirname_path)
  # else:
  # print("directory already exists: " + dirname_path)


def read_lines_from_file(file_path):
  f = open(file_path)
  lines = f.readlines()
  return lines


def write_lines_to_file(text_list, filename):
  text_file = open(filename, "w+b")
  lines = ""
  for line in text_list:
    line = str(line)
    lines += line
  text_file.write(lines.encode())
  text_file.close()


def stop_docker_container(container_name: str):
  command = 'docker' + " " + "stop " + container_name
  subprocess.call(command)


def docker_exec(container_id, command_to_run):
  """
  Execute a command inside a Docker container, supporting both Windows and Linux.
  By default, uses environment variables (that's why `bash -ic` was added).
  """
  docker_path = "docker"
  cmd = [docker_path, "exec", "-it", container_id, command_to_run]
  command = " ".join(cmd)
  # Determine the platform and adjust the call accordingly
  subprocess.call(command,  shell=True)  # On Windows, shell=True is usually required


def docker_start_hidden(container_name):
    '''
    docker start but with no output, runs in the background, you can run this in a thread,
     and it should be fine I suppose
    '''
    # docker_path = "C:/'Program Files'/Docker/Docker/resources/bin/docker.exe"
    cmd_list = ["docker", "start", container_name]
    outp = run_command_get_output(cmd_list)
    print(outp)


def run_command_get_output(cmd_list, inp=None):
    """
    :param cmd_list: list w/ 1st command, (2nd, 3rd, ...) args as parameters to command
    :return: returns a string w/ command output
    """
    if inp is not None:
        result = subprocess.run(cmd_list, stdout=subprocess.PIPE, input=inp)
    else:
        result = subprocess.run(cmd_list, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip().lower()


def copy_file(src, dst):
  shutil.copyfile(src, dst)


def recursive_copy_and_overwrite(src, dest, ignored=None):
  # from: https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
  if os.path.isdir(src):
    if not os.path.isdir(dest):
      os.makedirs(dest)
    files = os.listdir(src)
    if ignored is None:
      ignored = set()
    for f in files:
      if f not in ignored:
        recursive_copy_and_overwrite(os.path.join(src, f), os.path.join(dest, f), ignored)
  else:
    shutil.copyfile(src, dest)


def screenshot_tool_get_args(parser: argparse.ArgumentParser):
  parser.add_argument(
    "--coords",
    help="(tuple of coords (ex.: 1,1,1000,700) -> (1,1,1000,700) no for none, coordinates, if appliable, if not appliable, 'no' id must be set",
    default="no",
  )
  parser.add_argument(
    "--app_to_test",
    help="name of the actions repository associated to the app (ex: runescape_actions)",
    required=True,
  )
  parser.add_argument(
    "--actions_to_put_images_in", help="name of the action to test (ex: login)", required=True
  )
  parser.add_argument(
    "--screenshot_file_name_list",
    help="list of names of all screenshots to take, must end in the picture file extension, ex: (first_pic.png)",
    default=None,
  )
  parser.add_argument(
    "--callback_type_str",
    help="[keyboard/mouse_onclick]string identifier to the type of callback to be used (keyboard key is left control or caps lock)",
    required=True,
  )
  parser.add_argument(
    "--recording_method",
    help="[BORDER/fullscreen] record fullscreen when clicking the image (fullscreen), or record a square on the main image (BORDER)",
    default="border",
  )
  parser.add_argument(
    "--template_match_image_to_test_photo_against_list",
    help="uses this image path to try and find the screenshot taken against the corresponding element in this list",
    default=None,
  )


def normalize_path(path):
  """
  return path without final /
  """
  path_list = path.split("/")[::]
  path_list = [i + "/" for i in path_list if i != ""]
  # add initial / to path
  path_list[0] = "/" + path_list[0]
  # remove final / from path
  path_list[-1] = path_list[-1].replace("/", "")
  return "".join(path_list)
