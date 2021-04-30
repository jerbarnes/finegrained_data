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

# move NoReC
mv norec processed

###########################################
# CLEAN UP
###########################################

cd ..
rm -rf database.mpqa.2.0
rm -rf DarmstadtServiceReviewCorpus
rm -rf DarmstadtServiceReviewCorpus.zip
rm -rf multibooked
rm -rf opener_en
rm -rf opener_es

