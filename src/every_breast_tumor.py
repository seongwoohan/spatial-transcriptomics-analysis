import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
from time import sleep
import matplotlib.pyplot as plt

# data points(x,y coordinate) for the tissue
path1 = '/Users/seongwoohan/desktop/tissue_positions_list.csv'
position = pd.read_csv(path1)

# data points (x,y coordinate) for the tissue
tissue_spots = position.iloc[:,1] == 1
position = position.loc[tissue_spots,:]

# re-index position
re_position = position.reset_index(drop=True)
new_x = re_position.iloc[:,4] 
new_y = re_position.iloc[:,5] 

# import image: comes with BGR
path2 = '/Users/seongwoohan/desktop/V1_Breast_Cancer_Block.png'
img = cv2.imread(path2)

# diameter & diameter for image 
spot_diameter_fullres = 177.4829519178534
spot_radius = int(spot_diameter_fullres/2)

# find every coordinate
# 'a' indicates all 3813 images we want - it takes some time and memory to run all of them
# try to run it with small number e.g. range(2) or range(3) to see how the code is working
a = len(new_x) 
# try with 100 images
for i in tqdm(range(a)):
    sleep(0.01)    
    # pick random number under 3813
    random_num = np.random.randint(len(new_x))
    # find random x,y coordinates in tissue_positions_list.csv
    first_x = new_x[random_num]
    first_y = new_y[random_num]

    # width
    x_label = int(first_x)
    print('x_label:', x_label)
    # height
    y_label = int(first_y)
    print('y_label:', y_label)
    # radius
    rad = spot_radius
    print('radius:',rad)

    # find x,y coordinates corresponding to the 'gene' name in tissue_positions_list.csv 
    a = position[(position['x_label']==first_x) & (position['y_label']==first_y)]['barcode']
    b = a.tolist()[0]
   
    # file directory
    square_path = '/Users/seongwoohan/desktop/ST_image/square/'
    circle_path = '/Users/seongwoohan/desktop/ST_image/circle/'
    cropped_path = '/Users/seongwoohan/desktop/ST_image/cropped/'

    # show file name
    square_file_name = b +' (square).png'
    circle_file_name = b + ' (circle).png'
    cropped_file_name = b + ' (cropped).png'
    print('square filenmae: % s' % (square_file_name))
    print('circle filename: % s' % (circle_file_name))
    print('cropped filename: % s' % (cropped_file_name))
    print()

    # square image
    roi_square = img[y_label-rad:y_label+rad, x_label-rad:x_label+rad]
    cv2.imwrite(square_path + square_file_name, roi_square)
    plt.imshow(roi_square)

    # mask and extract circle image
    circle_img = cv2.circle(img, center = (x_label, y_label), radius = rad, 
           color = (0,0,0), thickness = 1)
    mask = np.zeros_like(circle_img)
    rows, cols,_ = mask.shape

    # create a white filled circle
    mask = cv2.circle(mask, center = (x_label, y_label), radius = rad, 
            color = (255,255,255), thickness = -1)
    
    # Bitwise AND operation to black out regions outside the mask               
    cropped_img = np.bitwise_and(circle_img, mask)

    # Convert from BGR to RGB for displaying correctly in matplotlib
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)    

    # circle image
    roi_circle = circle_img[y_label-rad:y_label+rad, x_label-rad:x_label+rad]
    cv2.imwrite(circle_path  + circle_file_name, roi_circle)
    plt.imshow(roi_circle)

    # cropped image
    roi_cropped = cropped_img[y_label-rad:y_label+rad, x_label-rad:x_label+rad]
    cv2.imwrite(cropped_path + cropped_file_name, roi_cropped)    
    plt.imshow(roi_cropped)
    plt.axis('off')
