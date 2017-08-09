import numpy as np

from labels_manager.tools.manipulations.relabeller import keep_only_one_label
from labels_manager.tools.aux_methods.utils import binarise_a_matrix


def lncc_distance(values_patch1, values_patch2):
    """
    Import values below the patches, containing the same number of eolem
    :param values_patch1:
    :param values_patch2:
    :return:
    """
    patches = [values_patch1.flatten(), values_patch2.flatten()]
    np.testing.assert_array_equal(patches[0].shape, patches[1].shape)

    for index_p, p in enumerate(patches):
        den = float(np.linalg.norm(p))
        if den == 0: patches[index_p] = np.zeros_like(p)
        else: patches[index_p] = patches[index_p] / den

    return patches[0].dot(patches[1])


def centroid(im, labels, real_space_coordinates=True):
    """

    :param im:
    :param labels: list of labels, e.g. [3] or [2, 3, 45]
    :param real_space_coordinates: if true the answer is in mm if false in voxel indexes.
    :return: centroid of the labels of an image, in the order of the labels
    """
    centers_of_mass = [np.array([0, 0, 0]) ] * len(labels)
    for l_id, l in enumerate(labels):
        coordinates_l = np.where(im.get_data() == l)  # returns [X_vector, Y_vector, Z_vector]
        centers_of_mass[l_id] = (1 / float(len(coordinates_l[0]))) * np.array([np.sum(k) for k in coordinates_l])
    if real_space_coordinates:
        centers_of_mass = [im.affine[:3, :3].dot(cm.astype(np.float64)) for cm in centers_of_mass]
    else:
        centers_of_mass = [np.round(cm).astype(np.uint64) for cm in centers_of_mass]
    return centers_of_mass


def box_sides(in_segmentation, label_to_box=1):
    """
    We assume the component with label equals to label_to_box is connected
    :return:
    """
    one_label_data = keep_only_one_label(in_segmentation, label_to_keep=label_to_box)
    ans = []
    for d in range(len(one_label_data.shape)):
        ans.append(np.sum(binarise_a_matrix(np.sum(one_label_data, axis=d), dtype=np.int)))
    return ans


def hausdoroff_distance():
    pass