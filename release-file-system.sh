#!/bin/bash

nohup find local/directory -type f -print0 | xargs -0 -n 1 sudo lfs hsm_release &
