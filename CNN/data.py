from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import os
import skimage.io as io
import skimage.transform as trans

def adjustData(img,mask):
    if(np.max(img) > 1):
        img = img / 255.0
        mask = mask /255.0
        mask[mask > 0.5] = 1
        mask[mask <= 0.5] = 0
    return (img,mask)

def trainGenerator( batch_size,
                    train_path,
                    image_folder,
                    mask_folder,
                    augmentation_folder,
                    image_save_prefix  = "image",
                    mask_save_prefix  = "mask",
                    #num_class = 2,
                    target_size = (192,192),
                    seed = 2):

    image_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        #rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

    mask_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        #rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

    image_generator = image_datagen.flow_from_directory(
        train_path,
        classes = [image_folder],
        class_mode = None,
        target_size = target_size,
        color_mode= 'grayscale',
        batch_size = batch_size,
        save_to_dir = augmentation_folder,
        save_prefix  = image_save_prefix,
        seed = seed)

    mask_generator = mask_datagen.flow_from_directory(
        train_path,
        classes = [mask_folder],
        class_mode = None,
        target_size = target_size,
        color_mode= 'grayscale',
        batch_size = batch_size,
        save_to_dir = augmentation_folder,
        save_prefix  = mask_save_prefix,
        seed = seed)

    train_generator = zip(image_generator, mask_generator)

    for (img,mask) in train_generator:
        img,mask = adjustData(img,mask)
        yield (img,mask)

    for (img,mask) in train_generator:
        yield (img,mask)

def testGenerator(test_path,num_image = 30,target_size = (192,192),flag_multi_class = False,as_gray = True):
    for i in range(num_image):
        img = io.imread(os.path.join(test_path,"%d.png"%i),as_gray = as_gray)
        img = img / 255
        img = trans.resize(img,target_size)
        img = np.reshape(img,img.shape+(1,)) if (not flag_multi_class) else img
        img = np.reshape(img,(1,)+img.shape)
        yield img

def saveResult(save_path,npyfile,flag_multi_class = False,num_class = 2):
    for i,item in enumerate(npyfile):
        img = labelVisualize(num_class,COLOR_DICT,item) if flag_multi_class else item[:,:,0]
        io.imsave(os.path.join(save_path,"%d_predict.png"%i),img)





