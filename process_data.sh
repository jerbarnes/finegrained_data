#!/bin/bash

# Create new folder where you will keep all processed data
mkdir processed

cd processing_scripts

# Process mpqa data
python3 process_mpqa.py

# Process darmstadt data
cd ..
unzip DarmstadtServiceReviewCorpus.zip
cd DarmstadtServiceReviewCorpus
unzip services
unzip universities
grep -rl "&" universities/basedata | xargs sed -i 's/&/and/g'
cd ..
cd processing_scripts
python3 process_darmstadt.py

# Process MultiBooked data
mkdir ../processed/multibooked_ca
mkdir ../processed/multibooked_eu
python3 process_multibooked_opener.py --indir ../multibooked/corpora/ca --outdir ../processed/multibooked_ca --datasplit datasplit/multibooked_ca.json
python3 process_multibooked_opener.py --indir ../multibooked/corpora/eu --outdir ../processed/multibooked_eu --datasplit datasplit/multibooked_eu.json

# Process OpeNER data
mkdir ../processed/opener_en
mkdir ../processed/opener_es
python3 process_multibooked_opener.py --indir ../opener_en/kaf/hotel --outdir ../processed/opener_en --datasplit datasplit/opener_en.json
python3 process_multibooked_opener.py --indir ../opener_es/kaf/hotel --outdir ../processed/opener_es --datasplit datasplit/opener_es.json

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
rm -rf database.mpqa.2.0
rm -rf DarmstadtServiceReviewCorpus
rm -rf DarmstadtServiceReviewCorpus.zip
rm -rf jiang-et-al
rm -rf mitchell
rm -rf MitchellEtAl-13-OpenSentiment.tgz
rm -rf multibooked
rm -rf opener_en
rm -rf opener_es
rm -rf SemEval
rm -rf wangetal
rm -rf wangetal.zip

