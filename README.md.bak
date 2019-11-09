# BRDNet
## Image denoising using deep CNN with batch renormalization

##Absract
### Deep convolutional neural networks (CNNs) have attracted great attention in the field of image denoising. However, there are two drawbacks: (1) It is very difficult to train a deeper CNN for denoising tasks, and (2) most of deeper CNNs suffer from performance saturation. In this paper, we report the design of a novel network called a batch-renormalization denoising network (BRDNet).
### Specifically, we combine two networks to increase the width of the network, and thus obtain more
### features. Because batch renormalization is fused into BRDNet, we can address the internal covari-
### ateshiftandsmallmini-batchproblems. Residuallearningisalsoadoptedinaholisticwaytofacil-
### itate network training. Dilated convolutions are exploited to extract more information for denois-
### ing tasks. Extensive experimental results show that BRDNet outperforms state-of-the-art image-
### denoising methods. The code of BRDNet is accessible at http://www.yongxu.org/lunwen.html.


## Requirements (Keras)
### tensorflow 1.3.0
### keras 2.0  
### Numpy 
### Opencv

## Commands
## Training for gray noisy images
### train gray noisy image
### python mainimprovement.py

## Training for color noisy images
### train color noisy image
### python mainimprovement.py

## Test for gray noisy images
### test gray noisy image with noise level of 25
### python mainimprovement.py  --only_test True --pretrain 25/model_50.h5 

## Test for color noisy images
## test color noisy image with noise level of 25
## python mainimprovementcolor.py  --only_test True --pretrain 25/model_50.h5 

## Training datasets 
The  training dataset of the gray noisy images is downloaded at https://pan.baidu.com/s/13jDZfayiM-KxLAOVWvFlUA
The  training dataset of the color noisy images is downloaded at https://pan.baidu.com/s/1cx3ymsWLIT-YIiJRBza24Q

## Network architecture
![RUNOOB 图标](./result/1.png)

## Resluts
### Gaussian gray noisy image denoising
#### Average PSNR (dB) results of different methods on BSD68 dataset with noise levels of 15, 25 and 50.
![RUNOOB 图标](./result/2.png)
#### PSNR (dB) results for different methods on 12 widely used images with noise levels of 15, 25 and 50.
![RUNOOB 图标](./result/3.png)

### Visual results for gray noisy images
#### Denoising results of one image from the BSD68 dataset with noise level 25 using for different methods: (a) original image, (b) noisy image /20.30 dB, (c) WNNM/29.75 dB, (d) E-PLL/29.59 dB, (e) TNRD/29.76 dB, (f) DnCNN/30.16 dB, (g) BM3D/29.53 dB, (h) IRCNN/30.07 dB, and(i) BRDNet/30.27 dB.
![RUNOOB 图标](./result/4.png)
#### Denoising results of image “monar” from Set12 with noise level 50 using different methods: (a) original image, (b) noisy image/14.71 dB, (c) WNNM/26.32 dB, (d) EPLL/25.94dB, (e) TNRD/26.31 dB, (f) DnCNN/26.78 dB, (g) BM3D/25.82 dB, (h) IRCNN/26.61 dB, and(i) BRDNet/26.97 dB.
![RUNOOB 图标](./result/5.png)

### Gaussian color noisy image Denoising
#### Average PSNR (dB) results of different methods on the CBSD68, Kodak24, and McMaster datasets with noise levels of 15, 25, 35, 50, and 75.
![RUNOOB 图标](./result/6.png)

### Visual results for color noisy images
#### Denoising results for one color image from the McMaster dataset with noise level 35: (a) original image/ σ = 35, (b) noisy image/18.62 dB, (c) CBM3D/31.04 dB, (d) FFDNet/31.94dB, and (e) BRDNet/32.25 dB.
![RUNOOB 图标](./result/7.png)
#### Denoising results for one color image from the Kodak24 dataset with noise level 60:(a) original image/ σ = 60, (b) noisy image/13.45 dB, (c) CBM3D/31.00 dB, (d) FFDNet/31.49 dB, and (e) BRDNet/31.85 dB.
![RUNOOB 图标](./result/8.png)

### Real noisy image denoising
#### PSNR (dB) results for different methods on real noisy images.
![RUNOOB 图标](./result/9.png)

### Complexity and complexity of different methods for image denoising
#### Complexity analysis of BRDNet, DnCNN and two DnCNNs.
![RUNOOB 图标](./result/10.png)

### Running time of different methods on an image different size 
#### Running time for different methods in denoising images of sizes 256 × 256, 512 × 512, and 1024 × 1024.
![RUNOOB 图标](./result/11.png)

