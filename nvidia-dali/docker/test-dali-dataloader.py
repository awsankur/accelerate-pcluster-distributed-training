import os
import time
from nvidia.dali.pipeline import pipeline_def
import nvidia.dali.types as types
import nvidia.dali.fn as fn
from nvidia.dali.plugin.pytorch import DALIGenericIterator

import numpy as np
import glob
import multiprocessing as mp


IMG_DIR = '/data/data/DeepPhenotype_PBMC_ImageSet_YSeverin/Training/'
TRAIN_BS = 30

multichannel_tiff_files = glob.glob(IMG_DIR + '/**/*.tiff', recursive=True)

for num_threads in range(8):
    # From https://github.com/NVIDIA/DALI/blob/main/dali/test/python/test_pipeline_multichannel.py
    @pipeline_def(num_threads=num_threads, device_id=0)
    def get_dali_pipeline():

        encoded, label = fn.readers.file(files=multichannel_tiff_files, name="Reader")
        decoded = fn.experimental.decoders.image(encoded, device="mixed", output_type=types.ANY_DATA)

        images = decoded.gpu()
        images = fn.resize(images,resize_y=220, resize_x=224)
        images = fn.crop(images,crop_h=220)

    return images, label

    train_loader = DALIGenericIterator(
        [get_dali_pipeline(batch_size=TRAIN_BS)],
        ['data', 'label'],
        reader_name='Reader'
    )

    num_epochs = 3
    start = time.time()
    for epoch in range(num_epochs):
        for i, data in enumerate(train_loader, 0):
            pass
    end = time.time()
    time_taken_secs = end - start
    avg_time_per_epoch_secs = time_taken_secs/num_epochs
    print("Dali Avg time per epoch:{} second, num_threads={}".format(avg_time_per_epoch_secs, num_threads))


