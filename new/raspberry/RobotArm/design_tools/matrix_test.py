import numpy as np

def dh_matrix(a, alpha, d, theta):
    c_theta = np.cos(theta)
    s_theta = np.sin(theta)
    c_alpha = np.cos(alpha)
    s_alpha = np.sin(alpha)

    return np.array([
        [c_theta, -s_theta * c_alpha, s_theta * s_alpha,  a * c_theta],
        [s_theta, c_theta * c_alpha,  -c_theta * s_alpha, a * s_theta],
        [0,       s_alpha,            c_alpha,                      d],
        [0,       0,                  0,                            1]
    ])

def foward_kinematics(q1, q2, q3, q4, q5):
    A1 = dh_matrix(0, np.pi / 2, 23, q1)
    A2 = dh_matrix(152, 0, 0, q2 + np.pi / 2)
    A3 = dh_matrix(155, 0, 0, q3)
    A4 = dh_matrix(0, -np.pi / 2, 0, q4 - np.pi / 2)
    A5 = dh_matrix(0, 0, 65, q5)

    t05 = A1 @ A2 @ A3 @ A4 @ A5

    T05 = np.round(t05, 6)
    return T05

T = foward_kinematics(0, 0, 0, 0, 0)


print(T)

position = T[:3, 3]
rotation = T[:3, :3]

print("posizione: ")
print(position)

print("rotation: ")
print(rotation)