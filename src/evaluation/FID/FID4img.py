########### CELIAN VERSION
import numpy

# example of calculating the frechet inception distance in Keras for cifar10
import numpy as np
from numpy import cov
import itertools
from numpy import trace
from numpy import iscomplexobj
from numpy import asarray
from numpy.random import shuffle
from scipy.linalg import sqrtm
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.datasets.mnist import load_data
from skimage.transform import resize
from keras.datasets import cifar10
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import json
#pip install opencv-python
#pip install -U scikit-image
#pip install tensorflow==2.12.*
def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']
# scale an array of images to a new size
def scale_images(images, new_shape):
    images_list = list()
    for image in images:
        # resize with nearest neighbor interpolation
        new_image = resize(image, new_shape, 0)
        # store
        images_list.append(new_image)
    return asarray(images_list)
def process_img_custom(im_path):
    images1 = cv2.imread(im_path)
    if images1.dtype is False:
      images1 = images1.astype(np.float32)
    images1 = scale_images(images1, (299, 299, 3))
    return preprocess_input(images1)
# calculate frechet inception distance
def calculate_fid(model, act1, act2):
    # calculate activations
   
    
    print("compute stats")
    # calculate mean and covariance statistics
    mu1, sigma1 = act1.mean(axis=0), cov(act1, rowvar=False)
    mu2, sigma2 = act2.mean(axis=0), cov(act2, rowvar=False)
    # calculate sum squared difference between means
    ssdiff = numpy.sum((mu1 - mu2)**2.0)
    # calculate sqrt of product between cov
    covmean = sqrtm(sigma1.dot(sigma2))
    # check and correct imaginary numbers from sqrt
    if iscomplexobj(covmean):
        covmean = covmean.real
    # calculate score
    fid = ssdiff + trace(sigma1 + sigma2 - 2.0 * covmean)
    return fid
class NumpyFloatValuesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return JSONEncoder.default(self, obj)
    
# prepare the inception v3 model

if __name__ == "__main__":
    #list_QID=["Q923684"]
    list_QID=["Q215681", "Q716794", "Q923684", "Q1055776", "Q1248616", "Q3244512", "Q3606846", "Q5353616", "Q7077012", "Q7180638"]
    if(tf.test.is_gpu_available()):
       physical_devices = tf.config.list_physical_devices('GPU')
       tf.config.set_visible_devices(physical_devices[1:],'GPU')
       
    model = InceptionV3(include_top=False, pooling='avg', input_shape=(299,299,3))
    base_dir=os.path.dirname(__file__)
    # open('C:/Users/Martin/Desktop/DS_griff/result.json','w') 
    
    dict_QID_imgpath={}
    dict_measures={}
    imgs_titles=['basic_prompt', 'plain_prompt','verbalised_prompt','dbpedia_abstract_prompt']
    
    print(">>>>>>>>>>>>>GET FILES")
    for folder in os.listdir(base_dir+'/ground-truth'):
        if("Q" in folder):
            if("Q923684_John Sheppard" in folder):
                print("HEYYYYYYYYYYYYY")
            f2=folder.split("_")
            QID=f2[0]
            dict_QID_imgpath[QID]={}
            list_files=os.listdir(base_dir+'/stable-diffusion-2-1-with-images/'+folder)
            for img_title in imgs_titles:
                if(img_title+".jpg" in list_files):
                    img_path=base_dir+'/stable-diffusion-2-1-with-images/'+folder+"/"+img_title+".jpg"

                    if(os.path.exists(img_path)):
                        dict_QID_imgpath[QID][img_title]=img_path
            
            gt_path=base_dir+'/ground-truth/'+folder+"/"+folder+".jpg"
            if (os.path.exists(gt_path)):
                dict_QID_imgpath[QID]["ground-truth"]=gt_path
            else:    
                gt_path=base_dir+'/ground-truth/'+folder+"/"+folder+".png"
                if (os.path.exists(gt_path)):
                    dict_QID_imgpath[QID]["ground-truth"]=gt_path
                
                   
    
    print(">>>>>>>>>>>>>COMPUTE DIST FILES")
    for QID in dict_QID_imgpath.keys():
      
        
        if(QID in list_QID):
            print(">>>>>>>>> IN THE LIST")
            print(">>>>"+QID)
            combin = list(itertools.combinations(list(dict_QID_imgpath[QID].keys()), 2))
            print("process gt")
            gt=process_img_custom(dict_QID_imgpath[QID]["ground-truth"])
            gt_act = model.predict(gt)
            
            dict_measures[QID]={}
            print("end gt")
            
            for c in combin:
                
                if(c[0] == "ground-truth" or c[1] == "ground-truth"): 
                   if(c[0] == "ground-truth"):
                       
                       print("PROCESS > ","-".join(c))
                       image1 = process_img_custom(dict_QID_imgpath[QID][c[1]])
                   if(c[1] == "ground-truth"): 
                       image1 = process_img_custom(dict_QID_imgpath[QID][c[0]])
                       
                       print("PROCESS > ","-".join(c))
                   act2 = model.predict(image1)
                   fid = calculate_fid(model, gt_act, act2)
                   dict_measures[QID]["-".join(c)]=fid
            
    # with open(base_dir+'/FID_HumanSample_dist_img_gt.json', 'w', encoding='utf-8') as f:
    #     json.dump(dict_measures, f, ensure_ascii=False, cls=NumpyFloatValuesEncoder)