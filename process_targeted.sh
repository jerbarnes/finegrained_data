#!/bin/bash

# Create new folder where you will keep all processed data
mkdir processed

cd processing_scripts

# Process semeval data
python3 process_semeval.py

# Process mitchell et al
cd ..
mkdir mitchell
tar -xvf MitchellEtAl-13-OpenSentiment.tgz -C mitchell
grep -Prl "TELEPHONE\tNUMBER" mitchell/en/10-fold/* | xargs sed -iE 's/TELEPHONE\tNUMBER/TELEPHONE-NUMBER/g'
cd processing_scripts
python3 process_mitchell.py

# Process wang, et al.
cd ..
mkdir wangetal
unzip wangetal.zip -d wangetal
cd wangetal
tar -xvf annotations.tar.gz
tar -xvf tweets.tar.gz
cd ../processing_scripts
python3 process_wang.py


# Process Jiang et al.
python3 process_jiang.py


###########################################
# CLEAN UP
###########################################

cd ..
rm -rf jiang-et-al
rm -rf mitchell
rm -rf MitchellEtAl-13-OpenSentiment.tgz
rm -rf SemEval
rm -rf wangetal
rm -rf wangetal.zip

