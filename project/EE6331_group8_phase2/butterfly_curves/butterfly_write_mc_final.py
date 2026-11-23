import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change this to rename title, legend etc in graph
test_case = "WRITE" 

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
file_path_1 = r'C:\Users\srich\OneDrive\Desktop\IITM\sem8\ee6331_EMD\project\Monte_Carlo_cell\graphs\write_Vr.txt'
file_path_2 = r'C:\Users\srich\OneDrive\Desktop\IITM\sem8\ee6331_EMD\project\Monte_Carlo_cell\graphs\write_Vl.txt'
runs_data_1 = parse_data(file_path_1)
runs_data_2_old = parse_data(file_path_2)

runs_data_2 = [[(y, x) for x, y in sub_array[::-1]] for sub_array in runs_data_2_old]

x_target = 0.3

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

_ , min_ind_dat1 = find_max_min_y_at_x(runs_data_1, x_target, x_target)
max_ind_dat2, _ = find_max_min_y_at_x(runs_data_2, x_target, x_target)

# Define the angle of rotation in radians
theta = np.radians(45)

def find_min_dist(original_coords_1, original_coords_2, eps=0.01):
    N1 = len(original_coords_1)
    N2 = len(original_coords_2)
    min_dist = np.inf
    min1_point = 0
    min2_point = 0
   
    for i in range(200,N1):
        point1 = original_coords_1[i]
        for j in range(200, N2):
            point2 = original_coords_2[j]
            point_diff = (point1[0] - point2[0], point1[1] - point2[1])
            distance = np.sqrt(np.sum(np.square(point_diff)))
            slope = point_diff[1]/point_diff[0]
            if slope >= 1 - eps and slope <= 1 + eps:
                if min_dist >= distance:
                    min_dist = distance
                    min1_point = point1
                    min2_point = point2
    return min_dist, min1_point, min2_point 

coords_1 = runs_data_1[min_ind_dat1]
coords_2 = runs_data_2[max_ind_dat2]

margin, point1, point2 = find_min_dist(coords_1, coords_2, 0.01)

margin = round(margin/np.sqrt(2),3)
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