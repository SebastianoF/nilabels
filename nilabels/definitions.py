import os
# from __init__ import __version__


# version = __version__
root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

info = {
        "name": "NiLabels",
        "version": '0.0.3dev',
        "description": "",
        "repository": {
                       "type": "git",
                       "url": ""
                      },
        "author": "Sebastiano Ferraris",
        "dependencies": {
                         "NiftySeg": "Vers b1bf8f08b152a093860da8fb5d0ceadfed6f4a13",
                         # requirements.txt automatically generated using pipreqs
                         "python requirements" : "{0}/requirements.txt".format(root_dir)
                         }
        }


definition_template = """ A template is the average, computed with a chose protocol, of a series of images acquisition
of the same anatomy, or in genreral of different objects that share common features.
"""

definition_atlas = """ An atlas is the segmentation of the template, obtained averaging with a chosen protocol,
the series of segmentations corresponding to the series of images acquisition that generates the template.
"""

definition_label = """ A segmentation assigns each region a label, and labels
are represented as subset of voxel with the same positive integer value.
"""

nomenclature_conventions = """ pfi_xxx = path to file xxx, \npfo_xxx = path to folder xxx,
\nin_xxx = input data structure xxx, \nout_xxx = output data structure xxx, \nz_ : prefix to temporary files and folders,
\nfin_ : file name.
"""