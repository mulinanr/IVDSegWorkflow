import sys
from model import *
from data import *

def train():
    print ('train')
    generator = trainGenerator( 20,
                                '../data/train/',
                                'image',
                                'label',
                                'augm')
    
    model = unet()
    model_checkpoint = ModelCheckpoint('unet_images.hdf5', monitor='loss', verbose=1, save_best_only=True)
    model.fit_generator(generator, steps_per_epoch=30, epochs=10, callbacks=[model_checkpoint])


def predict(file):
    model = unet('unet_images.hdf5')
    

    


def main():
    print ('start')
    if len(sys.argv) == 2 and sys.argv[1] == 'train':
        train()
    elif len(sys.argv) == 3 and sys.argv[1] == 'predict':
        predict(sys.argv[2])
    else:
        print('incorrect arguments')


if __name__ == "__main__":
    main()
