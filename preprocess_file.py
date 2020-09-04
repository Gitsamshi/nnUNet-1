from collections import OrderedDict
import os
import shutil
import json

if __name__ == "__main__":
    root_path = '/home/18zs11/covid_seg_baseline_nnuNet/covid_segmap_dataset'
    covid_image_path = os.path.join(root_path, 'COVID-19-CT-Seg_20cases')
    covid_infection_path = os.path.join(root_path, 'Infection_Mask')

    out_folder = os.path.join(os.environ['nnUNet_raw_data_base'], 'nnUNet_raw_data', 'Task101_Infection')
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)

    os.mkdir(out_folder)
    os.mkdir(os.path.join(out_folder, "imagesTr"))
    os.mkdir(os.path.join(out_folder, "imagesTs"))
    os.mkdir(os.path.join(out_folder, "labelsTr"))

    # handle images
    for ids in os.listdir(covid_image_path):
        src_file = os.path.join(covid_image_path, ids)
        dst_file_id = ids[:-7] + "_0000.nii.gz"
        dst_file = os.path.join(os.path.join(out_folder, "imagesTr", dst_file_id))
        shutil.copy(src_file, dst_file)

    # handle labels
    for ids in os.listdir(covid_infection_path):
        src_file = os.path.join(covid_infection_path, ids)
        dst_file = os.path.join(os.path.join(out_folder, "labelsTr", ids))
        shutil.copy(src_file, dst_file)

    json_dict = OrderedDict()
    json_dict['name'] = "COVID_infection_20"
    json_dict['description'] = "COVID_infection_20"
    json_dict['tensorImageSize'] = "3D"
    json_dict['reference'] = "see challenge website"
    json_dict['licence'] = "see challenge website"
    json_dict['release'] = "0.0"
    json_dict['modality'] = {
        "0": "CT",
    }
    json_dict['labels'] = {
        "0": "background",
        "1": "infection"
    }
    json_dict['numTraining'] = len(os.listdir(covid_image_path))
    json_dict['numTest'] = 0
    json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i[:-7],
                              "label": "./labelsTr/%s.nii.gz" % i[:-7]} for i in
                             os.listdir(covid_image_path)]
    json_dict['test'] = []

    json.dump(json_dict, open(os.path.join(out_folder, "dataset.json"), 'w'))