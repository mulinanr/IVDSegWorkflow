from keras.preprocessing.image import ImageDataGenerator
import os

def trainGenerator( batch_size,
                    train_path,
                    image_folder,
                    mask_folder,
                    augmentation_folder,
                    image_save_prefix  = "image",
                    mask_save_prefix  = "mask",
                    #num_class = 2,
                    target_size = (512,512),
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
        batch_size = batch_size,
        save_to_dir = augmentation_folder,
        save_prefix  = image_save_prefix,
        seed = seed)

    mask_generator = mask_datagen.flow_from_directory(
        train_path,
        classes = [mask_folder],
        class_mode = None,
        target_size = target_size,
        batch_size = batch_size,
        save_to_dir = augmentation_folder,
        save_prefix  = mask_save_prefix,
        seed = seed)

    train_generator = zip(image_generator, mask_generator)

    for (img,mask) in train_generator:
        yield (img,mask)




