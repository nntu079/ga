import numpy as np
import matplotlib.pyplot as plt

# Dãy giá trị cho trước
data = [99,
99,
96,
96,
92,
92,
91,
88,
87,
86,
85,
76,
74,
72,
69,
67,
67,
62,
61,
56,
52,
51,
49,
46,
44,
42,
40,
40,
33,
33,
30,
30,
29,
28,
28,
27,
25,
24,
23,
22,
21,
20,
17,
14,
13,
11,
10,
7,
7,
3]

# Vẽ histogram
plt.hist(data, bins=10, edgecolor='black')

# Cài đặt tiêu đề và nhãn cho trục x và y
plt.title("Histogram")
plt.xlabel("Giá trị")
plt.ylabel("Tần suất")

# Hiển thị đồ thị
plt.show()
