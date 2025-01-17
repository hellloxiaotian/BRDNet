# -*- coding: utf-8 -*-

import argparse
import logging
import os, time, glob
import PIL.Image as Image
import numpy as np
import pandas as pd
#from keras import backend as K
import tensorflow as tf
from keras.callbacks import CSVLogger, ModelCheckpoint, LearningRateScheduler
from keras.models import load_model
from keras.optimizers import Adam
from skimage.measure import compare_psnr, compare_ssim
import models 
from multiprocessing import Pool
import random

## Params
parser = argparse.ArgumentParser()
parser.add_argument('--model', default='BRDNet', type=str, help='choose a type of model')
parser.add_argument('--batch_size', default=20, type=int, help='batch size') #128
parser.add_argument('--train_data', default='./data/waterloo5050step40grayimage/', type=str, help='path of train data') #201807081928tcw
parser.add_argument('--test_dir', default='./data/Test/Set68', type=str, help='directory of test dataset') #original path ./data/Test/Set68
parser.add_argument('--sigma',default = 25, type =int,help='noise level')
parser.add_argument('--epoch', default=50, type=int, help='number of train epoches')
parser.add_argument('--lr', default=1e-3, type=float, help='initial learning rate for Adam')
parser.add_argument('--save_every', default=5, type=int, help='save model at every x epoches') #every x epoches save model
parser.add_argument('--pretrain', default=None, type=str, help='path of pre-trained model')
parser.add_argument('--only_test', default=False, type=bool, help='train and test or only test')
args = parser.parse_args()

if not args.only_test:
    save_dir = './snapshot/save_'+ args.model + '_' + 'sigma' + str(args.sigma) + '_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # log
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y %H:%M:%S',
                    filename=save_dir+'info.log',
                    filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-6s: %(levelname)-6s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    logging.info(args)
    
else:
    save_dir = '/'.join(args.pretrain.split('/')[:-1]) + '/'


def step_decay(epoch):
    
    initial_lr = args.lr
    if epoch<30:   #tcw
        lr = initial_lr #tcw
    else:
        lr = initial_lr/10
    
    return lr

def train_datagen(y_, batch_size=8): #201807081925tcw
    while(True):
	    for i in range(0,len(y_),batch_size):
		img1 = []
		for j in range(i,min(i+batch_size,len(y_))): #read batchsize images, which uses to train
		   img = np.array(Image.open(y_[j]).convert('L'),dtype='uint8') #dtype='float32')/255.0#.convert('L') #tcw 2018041
		   img1.append(img)
		get_batch_y = img1
		get_batch_y= np.array(get_batch_y)
                get_batch_y = get_batch_y.astype('float32')/255.0
		#print((get_batch_y.shape[0], get_batch_y.shape[1], get_batch_y.shape[2], 1)) #get_batch_y.shape[0] is the number of batchsize, 1 is channel and represents gray image
		get_batch_y = get_batch_y.reshape(get_batch_y.shape[0], get_batch_y.shape[1], get_batch_y.shape[2], 1)
	#	np.random.shuffle(get_batch_y)
		noise =  np.random.normal(0, args.sigma/255.0, get_batch_y.shape)    # noise
		get_batch_x = get_batch_y + noise  # input image = clean image + noise
		yield get_batch_x, get_batch_y

#201807081928tcw
def load_images(data_path):
    images = [];
    file_dictory1 = glob.glob(args.train_data+'*.bmp') #notice the data format
    for file in file_dictory1:
        #print file
         images.append(file)
    random.shuffle(images)     
    return images
def train():
    images = load_images(args.train_data)
    if args.pretrain:   model = load_model(args.pretrain, compile=False) 
    else:   
        if args.model == 'BRDNet': model = models.BRDNet() #orginal format tcw 20180429
    model.compile(optimizer=Adam(), loss=['mse'])
    # use call back functions
    ckpt = ModelCheckpoint(save_dir+'/model_{epoch:02d}.h5', monitor='val_loss', 
                    verbose=0, period=args.save_every)
    csv_logger = CSVLogger(save_dir+'/log.csv', append=True, separator=',')
    lr = LearningRateScheduler(step_decay)
    history = model.fit_generator(train_datagen(images, batch_size=args.batch_size),
                    steps_per_epoch=len(images)//args.batch_size, epochs=args.epoch, verbose=1, 
                    callbacks=[ckpt, csv_logger, lr])
    return model

def test(model):
    
    print('Start to test on {}'.format(args.test_dir))
    out_dir = save_dir + args.test_dir.split('/')[-1] + '/'
    if not os.path.exists(out_dir):
            os.mkdir(out_dir)
            
    name = []
    psnr = []
    ssim = []
    file_list = glob.glob('{}/*.png'.format(args.test_dir)) #notice: it is easy to generate error  $201804101000tcw
    for file in file_list:
        # read image
        img_clean = np.array(Image.open(file), dtype='float32') / 255.0
        np.random.seed(0) #obtain the same random data when it is in the test phase tcw201804151350
        img_test = img_clean + np.random.normal(0, args.sigma/255.0, img_clean.shape)
        img_test = img_test.astype('float32')
        # predict
        x_test = img_test.reshape(1, img_test.shape[0], img_test.shape[1], 1)
        y_predict = model.predict(x_test) #tcw
        # calculate numeric metrics
        img_out = y_predict.reshape(img_clean.shape)
        img_out = np.clip(img_out, 0, 1)
        psnr_noise, psnr_denoised = compare_psnr(img_clean, img_test), compare_psnr(img_clean, img_out)
        ssim_noise, ssim_denoised = compare_ssim(img_clean, img_test), compare_ssim(img_clean, img_out)
        psnr.append(psnr_denoised)
        ssim.append(ssim_denoised)
        # save images
        filename = file.split('/')[-1].split('.')[0]    # get the name of image file
        name.append(filename)
        img_test = Image.fromarray((img_test*255).astype('uint8'))
        img_test.save(out_dir+filename+'_sigma'+'{}_psnr{:.2f}.png'.format(args.sigma, psnr_noise))
        img_out = Image.fromarray((img_out*255).astype('uint8')) 
        img_out.save(out_dir+filename+'_psnr{:.2f}.png'.format(psnr_denoised))
    #    print psnr_denoised
    #	print len(psnr)
        #print psnr
    psnr_avg = sum(psnr)/len(psnr)
    ssim_avg = sum(ssim)/len(ssim)
    name.append('Average')
    psnr.append(psnr_avg)
    ssim.append(ssim_avg)
    print('Average PSNR = {0:.2f}, SSIM = {1:.2f}'.format(psnr_avg, ssim_avg))
    
    pd.DataFrame({'name':np.array(name), 'psnr':np.array(psnr), 'ssim':np.array(ssim)}).to_csv(out_dir+'/metrics.csv', index=True)
    
if __name__ == '__main__':   
    
    if args.only_test:
        model = load_model(args.pretrain, compile=False)
        test(model)
    else:
        model = train()
        test(model)       
    
