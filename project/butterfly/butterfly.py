import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change this to rename title, legend etc in graph
test_case = "WRITE" 

# Reading the data from LTSpice txt files
df = pd.read_table(r'C:\Users\srich\OneDrive\Desktop\IITM\sem8\ee6331_EMD\project\butterfly\curve_data\write_vl_1.txt')
df1 = pd.read_table(r'C:\Users\srich\OneDrive\Desktop\IITM\sem8\ee6331_EMD\project\butterfly\curve_data\write_vr_0.txt')

# Define the angle of rotation in radians
theta = np.radians(45)

# Convert DataFrame columns to numpy arrays
original_coords_1 = df[['v8', 'V(vl1)']].values
original_coords_2 = df1[['V(vr_1)', 'v11']].values

def find_max_dist(original_coords_1, original_coords_2, eps=0.01):
    N1, _ = original_coords_1.shape
    N2, _ = original_coords_2.shape
    max_dist = -1*np.inf
    max1_point = 0
    max2_point = 0
    for i in range(N1):
        point1 = original_coords_1[i]
        for j in range(N2):
            point2 = original_coords_2[j]
            point_diff = point1 - point2
            distance = np.sqrt(np.sum(np.square(point_diff)))
            slope = point_diff[1]/point_diff[0]
            if slope >= 1 - eps and slope <= 1 + eps:
                if max_dist <= distance:
                    max_dist = distance
                    max1_point = point1
                    max2_point = point2
    return max_dist, max1_point, max2_point 

max_dist, point1, point2 = find_max_dist(original_coords_1, original_coords_2, 0.01)
margin = round(max_dist/np.sqrt(2),3)
print(f'Margin = {margin}')

square_arr = np.zeros((5, 2))
square_arr[0] = [point1[0], point1[1]]
square_arr[1] = [point1[0], point2[1]]
square_arr[2] = [point2[0], point2[1]]
square_arr[3] = [point2[0], point1[1]]
square_arr[4] = [point1[0], point1[1]]

plt.figure(figsize=(10, 10))
plt.scatter(df['v8'], df['V(vl1)'])
plt.scatter(df1['V(vr_1)'], df1['v11'])
plt.plot(square_arr[:, 0], square_arr[:, 1], color = 'green')

plt.title(rf'Butterfly curve for {test_case} op')
plt.xlabel(r'$V_{right}\longrightarrow$')
plt.ylabel(r'$V_{left}\longrightarrow$')
plt.text(0.52, 0.75, f"{test_case} Margin = {int(margin*1e3)} mV", fontsize = 15, bbox = dict(facecolor = 'green', alpha = 0.5))
plt.grid()
plt.show()