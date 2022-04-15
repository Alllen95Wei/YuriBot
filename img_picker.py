import os
import random


def random_pick(nsfw=False):
    """
    從img資料夾中隨機選取1張圖片，並回傳路徑。
    :param nsfw: 是否選取nsfw子資料夾中的圖片。
    :return:
    """
    img_folder_path = ""
    if nsfw:
        choice = random.randint(1, 2)
        if choice == 1:
            img_folder_path = os.path.dirname(os.path.abspath(__file__)) + "\\image"
        elif choice == 2:
            img_folder_path = os.path.dirname(os.path.abspath(__file__)) + "\\image\\nsfw"
    else:
        img_folder_path = os.path.dirname(os.path.abspath(__file__)) + "\\image"
    img_list = [f for f in os.listdir(img_folder_path) if os.path.isfile(os.path.join(img_folder_path, f))]
    img_path = os.path.join(img_folder_path, random.choice(img_list))
    return img_path
