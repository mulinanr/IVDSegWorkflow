import sys
from model import *
from data import *

def train():
    print ('train')
    generator = trainGenerator( 23,
                                '../../cnn_data',
                                'train',
                                'mask',
                                '../../cnn_data/augm')
    
    model = unet()
    model_checkpoint = ModelCheckpoint('unet_images.hdf5', monitor='loss', verbose=1, save_best_only=True)
    model.fit_generator(generator, steps_per_epoch=15, epochs=15, shuffle=True, callbacks=[model_checkpoint])


def predict():
    model = unet('unet_images.hdf5')
    

    


def main():
    print ('start')
    if len(sys.argv) == 2 and sys.argv[1] == 'train':
        train()
    elif len(sys.argv) == 2 and sys.argv[1] == 'predict':
        predict()
    else:
        print('incorrect arguments')


if __name__ == "__main__":
    main()
