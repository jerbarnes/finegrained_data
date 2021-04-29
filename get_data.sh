#!/bin/bash

# First download the mpqa 2.0 data from http://mpqa.cs.pitt.edu/corpora/mpqa_corpus/mpqa_corpus_2_0 and change the following path to point to the tar file
mpqa_tar_file="./mpqa_2_0_database.tar.gz"
tar -xvf $mpqa_tar_file

# download darmstadt data
wget https://tudatalib.ulb.tu-darmstadt.de/bitstream/handle/tudatalib/2448/DarmstadtServiceReviewCorpus.zip

# download MultiBooked
git init multibooked
cd multibooked
git remote add -f origin https://github.com/jerbarnes/multibooked
git config core.sparseCheckout true
echo "/corpora/*" >> .git/info/sparse-checkout
git pull origin master
cd ..

# download OpeNER English
git init opener_en
cd opener_en
git remote add -f origin https://github.com/opener-project/opinion_annotations_en
git config core.sparseCheckout true
echo "/kaf/*" >> .git/info/sparse-checkout
git pull origin master
cd ..

# download OpeNER Spanish
git init opener_es
cd opener_es
git remote add -f origin https://github.com/opener-project/opinion_annotations_es
git config core.sparseCheckout true
echo "/kaf/*" >> .git/info/sparse-checkout
git pull origin master
cd ..


# download semeval data
git init SemEval
cd SemEval
git remote add -f origin https://github.com/jiangqn/aspect_extraction
git config core.sparseCheckout true
echo "/data/official_data/*" >> .git/info/sparse-checkout
git pull origin master
cd ..

# download mitchell et al (2013) Open Domain Targeted Sentiment
wget www.m-mitchell.com/code/MitchellEtAl-13-OpenSentiment.tgz


# download wang, et al. (2017) Multi-target-specific sentiment recognition on twitter
wget -O wangetal.zip https://ndownloader.figshare.com/articles/4479563/versions/1


# download Jiang et al. (2019) A Challenge Dataset and Effective Models for Aspect-Based Sentiment Analysis
git init jiang-et-al
cd jiang-et-al
git remote add -f origin https://github.com/siat-nlp/MAMS-for-ABSA
git config core.sparseCheckout true
echo "/data/*" >> .git/info/sparse-checkout
git pull origin master
cd ..
