
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
