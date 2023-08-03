#!/bin/bash

nohup find  /fsx/fsx/DeepPhenotype_PBMC_ImageSet_YSeverin/ -type f -print0 | xargs -0 -n 1 sudo lfs hsm_release &
