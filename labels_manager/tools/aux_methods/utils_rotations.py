import numpy as np


def get_small_orthogonal_rotation(im_input, theta, principal_axis='pitch'):

    if principal_axis == 'pitch':
        rot = np.array([[1,            0,           0,       0],
                        [0,  np.cos(theta),  -np.sin(theta), 0],
                        [0,  np.sin(theta), np.cos(theta),   0],
                        [0,             0,          0,       1]])
    elif principal_axis == 'pitch':
        rot = np.array([[np.cos(theta), 0, np.sin(theta),  0],
                        [0,             1,      0,         0],
                        [-np.sin(theta), 0, np.cos(theta), 0],
                        [0,             0,      0,         1]])
    elif principal_axis == 'pitch':
        rot = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                        [np.sin(theta), np.cos(theta),  0, 0],
                        [0,                   0,        1, 0],
                        [0,                   0,        0, 1]])
    else:
        raise IOError

    return rot  # to be multiplied on the right side as im_input.get_affine().dot(rot)


def get_rototranslation_matrix(theta, rotation_axis=np.array([1,0,0]),  translation=np.array([0, 0, 0])):

    n = np.linalg.norm(rotation_axis)
    assert not np.abs(n) < 0.001, 'rotation axis too close to zero.'
    rot = rotation_axis / n

    # rodriguez formula:
    cross_prod = np.array([[0, -rot[2], rot[1]],
                           [rot[2], 0, -rot[0]],
                           [-rot[1], rot[0], 0]])
    rot_part = np.cos(theta) * np.identity(3) + np.sin(theta) * cross_prod + np.tensordot(rot, rot, axes=0)

    # transformations parameters

    rot_transl = np.identity(4)
    rot_transl[:3, :3] = rot_part
    rot_transl[:3, 3] = translation

    return rot_transl



def basic_rot_ax(m, ax=0):
    """
    Basic rotations of a 3d matrix. Ingredient of the method axial_rotations.
    ----------
    Example:

    cube = array([[[0, 1],
                   [2, 3]],

                  [[4, 5],
                   [6, 7]]])

    axis 0: perpendicular to the face [[0,1],[2,3]] (front-rear)
    axis 1: perpendicular to the face [[1,5],[3,7]] (lateral right-left)
    axis 2: perpendicular to the face [[0,1],[5,4]] (top-bottom)
    ----------
    Note: the command m[:, ::-1, :].swapaxes(0, 1)[::-1, :, :].swapaxes(0, 2) rotates the cube m
    around the diagonal axis 0-7.
    ----------
    Note: avoid reorienting the data if you can reorient the header instead.
    :param m: 3d matrix
    :param ax: axis of rotation
    :return: rotate the cube around axis ax, perpendicular to the face [[0,1],[2,3]]
    """

    ax %= 3

    if ax == 0:
        return np.rot90(m[:, ::-1, :].swapaxes(0, 1)[::-1, :, :].swapaxes(0, 2), 3)
    if ax == 1:
        return m.swapaxes(0, 2)[::-1, :, :]
    if ax == 2:
        return np.rot90(m, 1)


def axial_rotations(m, rot=1, ax=2):
    """
    :param m: 3d matrix
    :param rot: number of rotations
    :param ax: axis of rotation
    :return: m rotate rot times around axis ax, according to convention.
    """

    if m.ndim is not 3:
        assert IOError

    rot %= 4

    if rot == 0:
        return m

    for _ in range(rot):
        m = basic_rot_ax(m, ax=ax)

    return m


def flip_data(in_data, axis='x'):
    msg = 'Input array must be 3-dimensional.'
    assert in_data.ndim == 3, msg

    msg = 'axis variable must be one of the following: {}.'.format(['x', 'y', 'z'])
    assert axis in ['x', 'y', 'z'], msg

    if axis == 'x':
        out_data = in_data[:, ::-1, :]
    elif axis == 'y':
        out_data = in_data[:, :, ::-1]
    elif axis == 'z':
        out_data = in_data[::-1, :, :]
    else:
        raise IOError

    return out_data


def symmetrise_data(in_data, axis='x', plane_intercept=10, side_to_copy='below', keep_in_data_dimensions=True):
    """
    Symmetrise the input_array according to the axial plane
      axis = plane_intercept
    the copied part can be 'below' or 'above' the axes, following the ordering.

    :param in_data: (Z, X, Y) C convention input data
    :param axis:
    :param plane_intercept:
    :param side_to_copy:
    :param keep_in_data_dimensions:
    :return:
    """

    # Sanity check:

    msg = 'Input array must be 3-dimensional.'
    assert in_data.ndim == 3, msg

    msg = 'side_to_copy must be one of the two {}.'.format(['below', 'above'])
    assert side_to_copy in ['below', 'above'], msg

    msg = 'axis variable must be one of the following: {}.'.format(['x', 'y', 'z'])
    assert axis in ['x', 'y', 'z'], msg

    # step 1: find the block to symmetrise.
    # step 2: create the symmetric and glue it to the block.
    # step 3: add or remove a patch of slices if required to keep the in_data dimension.

    out_data = 0

    if axis == 'x':

        if side_to_copy == 'below':
            s_block = in_data[:, :plane_intercept, :]
            s_block_symmetric = s_block[:, ::-1, :]
            out_data = np.concatenate((s_block, s_block_symmetric), axis=1)

        if side_to_copy == 'above':
            s_block = in_data[:, plane_intercept:, :]
            s_block_symmetric = s_block[:, ::-1, :]
            out_data = np.concatenate((s_block_symmetric, s_block), axis=1)

    if axis == 'y':

        if side_to_copy == 'below':
            s_block = in_data[:, :, :plane_intercept]
            s_block_symmetric = s_block[:, :, ::-1]
            out_data = np.concatenate((s_block, s_block_symmetric), axis=2)

        if side_to_copy == 'above':
            s_block = in_data[:, :, plane_intercept:]
            s_block_symmetric = s_block[:, :, ::-1]
            out_data = np.concatenate((s_block_symmetric, s_block), axis=2)

    if axis == 'z':

        if side_to_copy == 'below':
            s_block = in_data[:plane_intercept, :, :]
            s_block_symmetric = s_block[::-1, :, :]
            out_data = np.concatenate((s_block, s_block_symmetric), axis=0)

        if side_to_copy == 'above':
            s_block = in_data[plane_intercept:, :, :]
            s_block_symmetric = s_block[::-1, :, :]
            out_data = np.concatenate((s_block_symmetric, s_block), axis=0)

    if keep_in_data_dimensions:
        out_data = out_data[:in_data.shape[0], :in_data.shape[1], :in_data.shape[2]]

    return out_data