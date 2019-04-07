import sys
from model import *
from data import *

#os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def prepare():
    data_gen_args = dict(rotation_range=0.2,
                        width_shift_range=0.05,
                        height_shift_range=0.05,
                        shear_range=0.05,
                        zoom_range=0.05,
                        horizontal_flip=True,
                        fill_mode='nearest')
    myGenerator = trainGenerator(20, '../../cnn_data/train', 'image', 'label', data_gen_args, image_color_mode = "rgb", save_to_dir = '../../cnn_data/train/augm')

    #you will see 60 transformed images and their masks in data/membrane/train/aug
    num_batch = 10
    for i,batch in enumerate(myGenerator):
        if(i >= num_batch):
            break

    #mage_arr,mask_arr = geneTrainNpy("data/membrane/train/aug/","data/membrane/train/aug/")
    #np.save("data/image_arr.npy",image_arr)
    #np.save("data/mask_arr.npy",mask_arr)


def train():
    model = unet()
    model_checkpoint = ModelCheckpoint('ivd_unet_003.hdf5', monitor='loss',verbose=1, save_best_only=True)
    #model.fit_generator(myGene,steps_per_epoch=300,epochs=5,callbacks=[model_checkpoint])
    imgs_train, imgs_mask_train = geneTrainNpy("../../cnn_data/train/augm/", "../../cnn_data/train/augm/")
    model.fit(imgs_train, imgs_mask_train, batch_size=10, nb_epoch=5, verbose=1,validation_split=0.2, shuffle=True, callbacks=[model_checkpoint])

def predict():
    testGene = testGenerator("../../cnn_data/test", num_image = 23)
    model = unet()
    model.load_weights("ivd_unet_003.hdf5")
    results = model.predict_generator(testGene, 23, verbose=1)
    saveResult("../../cnn_data/result", results)





def main():
    print ('start')
    if len(sys.argv) == 2 and sys.argv[1] == 'prepare':
        prepare()
    elif len(sys.argv) == 2 and sys.argv[1] == 'train':
        train()
    elif len(sys.argv) == 2 and sys.argv[1] == 'predict':
        predict()
    elif len(sys.argv) == 2 and sys.argv[1] == 'all':
        prepare()
        train()
        predict()
    else:
        print('incorrect arguments')


if __name__ == "__main__":
    main()
