# BRDNet
Dependence
tensorflow
keras2
numpy
opencv

train gray noisy image
python mainimprovement.py

test gray noisy image with noise level of 25
python mainimprovement.py  --only_test True --pretrain 25/model_50.h5 



train color noisy image
python mainimprovement.py

test color noisy image with noise level of 25
python mainimprovementcolor.py  --only_test True --pretrain 25/model_50.h5 


The  training dataset of the gray noisy images is downloaded at https://pan.baidu.com/s/13jDZfayiM-KxLAOVWvFlUA
The  training dataset of the color noisy images is downloaded at https://pan.baidu.com/s/1cx3ymsWLIT-YIiJRBza24Q
