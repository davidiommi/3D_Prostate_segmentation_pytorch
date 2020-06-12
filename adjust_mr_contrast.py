
import os
import shutil
from time import time
import re
import numpy as np
import SimpleITK as sitk
import scipy.ndimage as ndimage

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def lstFiles(Path):

    images_list = []  # create an empty list, the raw image data files is stored here
    for dirName, subdirList, fileList in os.walk(Path):
        for filename in fileList:
            if ".nii.gz" in filename.lower():
                images_list.append(os.path.join(dirName, filename))
            elif ".nii" in filename.lower():
                images_list.append(os.path.join(dirName, filename))
            elif ".mha" in filename.lower():
                images_list.append(os.path.join(dirName, filename))

    images_list = sorted(images_list, key=numericalSort)
    return images_list


list_images=lstFiles('./volumes')
print(len(list_images))

for i in range(len(list_images)):

    a = list_images[19+i]

    case = a
    case = case.split('/')

    case = case[2]
    print(case)

    image = sitk.ReadImage(a)

    castImageFilter = sitk.CastImageFilter()
    castImageFilter.SetOutputPixelType(sitk.sitkFloat32)
    image = castImageFilter.Execute(image)

    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    corrector.SetMaximumNumberOfIterations((500,400,300))
    output = corrector.Execute(image)

    label_directory = os.path.join('./volumes_N4', case)

    sitk.WriteImage(output, label_directory)


# ct = sitk.ReadImage('./volumes_N4/Patient_40_MR.mha')
# ct_array = sitk.GetArrayFromImage(ct)
#
# array = np.transpose(ct_array, axes=(2, 1, 0))
# plot3d_axial(array)
#
# upper = 1723
# lower = -80
#
# ct_array[ct_array > upper] = upper
# ct_array[ct_array < lower] = lower
#
#
# array = np.transpose(ct_array, axes=(2, 1, 0))
# plot3d_axial(array)
#
# new_ct = sitk.GetImageFromArray(ct_array)
# new_ct.SetDirection(ct.GetDirection())
# new_ct.SetOrigin(ct.GetOrigin())
# new_ct.SetSpacing(ct.GetSpacing())
#
#
# sitk.WriteImage(new_ct, './volumes/Patient_40_MR.mha')