import numpy as np
import sympy
import scipy
from math import sin, cos


def rotationZ(angle_symbol):
    return sympy.Matrix(
        [[sympy.cos(angle_symbol), -sympy.sin(angle_symbol), 0],
         [sympy.sin(angle_symbol),  sympy.cos(angle_symbol), 0],
         [0, 0, 1]])


def get_revolutional_joint_transform(link_vector, angle_symbol, axis='z'):
    # TODO: implement all axis cases
    R = rotationZ(angle_symbol)
    t = R*link_vector

    # Bottom row used for homogeneity
    bot = sympy.Matrix(1, 4, [0, 0, 0, 1])
    return R.row_join(t).col_join(bot)


# TODO: Provide support for an additional end effector segment
def get_jacobian(robot):
    x_ee = sympy.Matrix(4, 1, [0, 0, 0, 1])
    q = sympy.MatrixSymbol('q', robot.n_joints(), 1)
    i = robot.n_joints()-1
    x = x_ee
    for link in robot.get_links(reverse=True):
        link_vector = sympy.Matrix([link.length, 0, 0])
        transform = get_revolutional_joint_transform(link_vector, q[i])
        x = transform * x
        i -= 1
    jacobian_symbol = x.jacobian(q)
    angles = robot.get_angles()
    for i in range(robot.n_joints()):
        jacobian_symbol = jacobian_symbol.subs(q[i], angles[i])
    return np.array(jacobian_symbol).astype(np.float64)[:3, :]


# TODO: Include angular control
def get_dq(robot, dx, include_theta=False):
    jacobian = get_jacobian(robot)
    if include_theta:
        raise NotImplemented("Theta jacobian not implemented.")
    if len(dx) == 2:
        dxv = np.array([dx[0], dx[1], 0, ])
    elif len(dx) == 3:
        dxv = np.array([dx[0], dx[1], dx[2]])
    else:  # Assume dx is full variable
        dxv = np.array(dx)

    return np.matmul(np.linalg.pinv(jacobian), dxv)


if __name__ == '__main__':
    from main import Robot
    from math import pi
    r = Robot(((100, 10), (100, 10)), [0, 0])
    r.set_rotation([pi/2, pi/2])
    J = get_jacobian(robot=r)
    print("Jacobian:")
    print(J)
    print("dq:")
    print(get_dq(r, (100, -100)))

