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


# Define the angle of rotation in radians
theta = np.radians(45)

def find_max_dist(original_coords_1, original_coords_2, eps=0.01):
    N1 = len(original_coords_1)
    N2 = len(original_coords_2)
    max_dist = -1*np.inf
    max1_point = 0
    max2_point = 0
    for i in range(N1):
        point1 = original_coords_1[i]
        for j in range(N2):
            point2 = original_coords_2[j]
            point_diff = (point1[0] - point2[0], point1[1] - point2[1])
            distance = np.sqrt(np.sum(np.square(point_diff)))
            slope = point_diff[1]/point_diff[0]
            if slope >= 1 - eps and slope <= 1 + eps:
                if max_dist <= distance:
                    max_dist = distance
                    max1_point = point1
                    max2_point = point2
    return max_dist, max1_point, max2_point 
margins = []
points1 = []
points2 = []

for i in range(0,100):
    coords_1 = runs_data_1[i]
    coords_2 = runs_data_2[i]
    max_dist, point1, point2 = find_max_dist(coords_1, coords_2, 0.01)
    margins.append(max_dist)
    points1.append(point1)
    points2.append(point2)
    print(i)

min_margin = min(margins)

# Find the index of the minimum value
min_index = margins.index(min_margin)

margin = round(min_margin/np.sqrt(2),3)
print(f'Margin = {margin}')
print(f'Min index = {min_index}')
point1 = points1[min_index]
point2 = points2[min_index]

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