import numpy as np
import matplotlib.pyplot as plt

# Tạo dãy giá trị từ 25 đến 75 với phân phối đồng nhất
numbers = np.random.uniform(45, 55, size=50)
numbers = np.round(numbers).astype(int)

# Sắp xếp dãy số theo thứ tự giảm dần
numbers_sorted = np.sort(numbers)[::-1]

# In các giá trị của dãy số theo thứ tự giảm dần
print("Các giá trị của dãy số (theo thứ tự giảm dần):")
for number in numbers_sorted:
    print(number)

# Vẽ histogram với trục hoành là giá trị và trục tung là tần suất
plt.hist(numbers, bins=5, orientation='horizontal', edgecolor='black')

# Cài đặt tiêu đề và nhãn cho trục x và y
plt.title("Tần suất xuất hiện của dãy số")
plt.xlabel("Tần suất")
plt.ylabel("Giá trị")

# Hiển thị đồ thị
plt.show()