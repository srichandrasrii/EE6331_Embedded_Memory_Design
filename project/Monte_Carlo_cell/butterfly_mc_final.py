import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change this to rename title, legend etc in graph
test_case = "READ" 

def parse_data(file_path):
    data = []
    current_run = -1

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith("Step Information"):
                current_run += 1
                data.append([])
            elif line and not line.startswith("v8") and not line.startswith("v11") and not line.startswith("Step Information"):
                values = line.split()
                data[current_run].append((float(values[0]),float(values[1])))

    return data

# Path to your text file
file_path_1 = r'C:\Users\srich\OneDrive\Desktop\IITM\sem8\ee6331_EMD\project\Monte_Carlo_cell\graphs\read_Vl.txt'
file_path_2 = r'C:\Users\srich\OneDrive\Desktop\IITM\sem8\ee6331_EMD\project\Monte_Carlo_cell\graphs\read_Vr.txt'
runs_data_1 = parse_data(file_path_1)
runs_data_2_old = parse_data(file_path_2)

runs_data_2 = [[(y, x) for x, y in sub_array[::-1]] for sub_array in runs_data_2_old]

x_target_1 = 0.2
x_target_2 = 0.6

def interpolate_y(curve, x_target):
    x = np.array([point[0] for point in curve])
    y = np.array([point[1] for point in curve])
    
    # Check if x_target is exactly in the x array
    if x_target in x:
        return y[np.where(x == x_target)[0][0]]
    
    # If not, interpolate
    return np.interp(x_target, x, y)

def find_max_min_y_at_x(curves, x_target_min, x_target_max):
    max_y = -np.inf
    min_y = np.inf
    max_index = -1
    min_index = -1
    
    for i, curve in enumerate(curves):
        y_at_x_min = interpolate_y(curve, x_target_min)
        y_at_x_max = interpolate_y(curve, x_target_max)
        if y_at_x_max > max_y:
            max_y = y_at_x_max
            max_index = i
        if y_at_x_min < min_y:
            min_y = y_at_x_min
            min_index = i

    return max_index, min_index

max_ind_dat1, min_ind_dat1 = find_max_min_y_at_x(runs_data_1, x_target_1, x_target_2)
max_ind_dat2, min_ind_dat2 = find_max_min_y_at_x(runs_data_2, x_target_2, x_target_1)

# Define the angle of rotation in radians
theta = np.radians(45)

def find_max_dist(original_coords_1, original_coords_2, eps=0.01):
    N1 = len(original_coords_1)
    N2 = len(original_coords_2)
    max_dist_Uh = -1*np.inf # max dist for upper half
    max_dist_Lh = -1*np.inf # max dist for lower half
    max1_point_Uh = 0
    max2_point_Uh = 0
    max1_point_Lh = 0
    max2_point_Lh = 0

    data_x_1 = [point[0] for point in original_coords_1]
    data_y_1 = [point[1] for point in original_coords_1]
    data_x_2 = [point[0] for point in original_coords_2]
    data_y_2 = [point[1] for point in original_coords_2]

    # Not including initial end points to find the middle intersection point
    points_1 = np.column_stack((data_x_1[50:N1-50], data_y_1[50:N1-50]))
    points_2 = np.column_stack((data_x_2[50:N2-50], data_y_2[50:N2-50]))

    # Compute the distance between each pair of points from the two datasets
    distances = np.linalg.norm(points_1[:, np.newaxis] - points_2, axis=2)

    # Find the index of the minimum distance
    min_dist_idx = np.unravel_index(np.argmin(distances), distances.shape)

    # Get the closest points
    closest_point_1 = points_1[min_dist_idx[0]]
    closest_point_2 = points_2[min_dist_idx[1]]

    # Find the index of the minimum value
    mid_pt_1 = data_x_1.index(closest_point_1[0])
    mid_pt_2 = data_x_2.index(closest_point_2[0])

    # First half lobe max margin
    for i in range(mid_pt_1):
        point1 = original_coords_1[i]
        for j in range(mid_pt_2):
            point2 = original_coords_2[j]
            point_diff = (point1[0] - point2[0], point1[1] - point2[1])
            distance = np.sqrt(np.sum(np.square(point_diff)))
            
            if(point_diff[0] == 0):
                slope = 1e10
            else:
                slope = point_diff[1]/point_diff[0]

            if slope >= 1 - eps and slope <= 1 + eps:
                if max_dist_Uh <= distance:
                    max_dist_Uh = distance
                    max1_point_Uh = point1
                    max2_point_Uh = point2
            
    # Second lobe max margin
    for i in range(N1 - mid_pt_1):
        point1 = original_coords_1[mid_pt_1 + i]
        for j in range(N2 - mid_pt_2):
            point2 = original_coords_2[mid_pt_2 + j]
            point_diff = (point1[0] - point2[0], point1[1] - point2[1])
            distance = np.sqrt(np.sum(np.square(point_diff)))
            
            if(point_diff[0] == 0):
                slope = 1e10
            else:
                slope = point_diff[1]/point_diff[0]

            if slope >= 1 - eps and slope <= 1 + eps:
                if max_dist_Lh <= distance:
                    max_dist_Lh = distance
                    max1_point_Lh = point1
                    max2_point_Lh = point2

    print(f'max dist Lh = {max_dist_Lh}, max dist Uh = {max_dist_Uh}')
    max_dist = min([max_dist_Lh, max_dist_Uh])

    if(max_dist == max_dist_Uh):
        max1_point = max1_point_Uh
        max2_point = max2_point_Uh
    elif(max_dist == max_dist_Lh):
        max1_point = max1_point_Lh
        max2_point = max2_point_Lh
    else:
        print("Error")

    return max_dist, max1_point, max2_point 

coords_1 = runs_data_1[min_ind_dat1]
coords_2 = runs_data_2[max_ind_dat2]
coords_3 = runs_data_1[max_ind_dat1]
coords_4 = runs_data_2[min_ind_dat2]
max_dist_1, point1, point2 = find_max_dist(coords_1, coords_2, 0.01) # Upper half lobe
max_dist_2, point3, point4 = find_max_dist(coords_3, coords_4, 0.01) # Bottom half lobe

min_margin = min([max_dist_1,max_dist_2])

if(min_margin == max_dist_2):
    point1,point2 = point3, point4

margin = round(min_margin/np.sqrt(2),3)
print(f'Margin = {margin}')
point1 = point1
point2 = point2

square_arr = np.zeros((5, 2))
square_arr[0] = [point1[0], point1[1]]
square_arr[1] = [point1[0], point2[1]]
square_arr[2] = [point2[0], point2[1]]
square_arr[3] = [point2[0], point1[1]]
square_arr[4] = [point1[0], point1[1]]

plt.figure(figsize=(10, 10))
for i in range(0,100):
    data_x_1 = [point[0] for point in runs_data_1[i]]
    data_y_1 = [point[1] for point in runs_data_1[i]]
    data_x_2 = [point[0] for point in runs_data_2[i]]
    data_y_2 = [point[1] for point in runs_data_2[i]]
    color = np.random.rand(3,)  # Generate a random color
    plt.scatter(data_x_1, data_y_1, color=color)
    plt.scatter(data_x_2, data_y_2, color=color)
plt.plot(square_arr[:, 0], square_arr[:, 1], color = 'green')

plt.title(rf'Butterfly curve for {test_case} op')
plt.xlabel(r'$V_{right}\longrightarrow$')
plt.ylabel(r'$V_{left}\longrightarrow$')
plt.text(0.52, 0.75, f"{test_case} Margin = {int(margin*1e3)} mV", fontsize = 15, bbox = dict(facecolor = 'green', alpha = 0.5))
plt.grid()
plt.show()