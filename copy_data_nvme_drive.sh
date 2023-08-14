#!/bin/bash

cd /local_scratch

echo ""
echo "Downloading Deep Phenotyping PMBC Image Set Data ..."
wget https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/343106/DeepPhenotype_PBMC_ImageSet_YSeverin.zip
unzip DeepPhenotype_PBMC_ImageSet_YSeverin.zip -d ./

rm DeepPhenotype_PBMC_ImageSet_YSeverin.zip

