#example way to run
#python create_splits.py --source data/waymo/training_and_validation/ --destination data/output/

import argparse
import glob
import os
import random
import math
import shutil

import numpy as np

from utils import get_module_logger

from sklearn.model_selection import train_test_split


train_ratio = 0.7
test_ratio = 0.2
validation_ratio = 1.0 - train_ratio - test_ratio


def split(source, destination):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    print(f"source: '{source}'     destination: '{destination}'")

    files = glob.glob(os.path.join(source, "*.tfrecord"))
    
    train_path = os.path.join(destination, "train")
    val_path = os.path.join(destination, "val")
    test_path = os.path.join(destination, "test")
    print(f"train_path '{train_path}', val_path '{val_path}', test_path '{test_path}'")
    
    #reset data
    #removing is not working, low on list to TODO
    if os.path.exists(train_path):
        os.rmdir(train_path)
    if os.path.exists(val_path):
        os.rmdir(val_path)
    if os.path.exists(test_path):       
        os.rmdir(test_path)
    os.makedirs(train_path)
    os.makedirs(val_path)
    os.makedirs(test_path)
    
    
    #allow to repduce output 
    #todo make configurable in future
    seed = 1
    
    #split out training data
    remaining_files, train_files,  = train_test_split(files, test_size = train_ratio, random_state = seed, shuffle = True)
    
    #2nd split is already shuffled from first call
    test_files, validation_files = train_test_split(remaining_files, test_size = (validation_ratio / (test_ratio + validation_ratio)))
    
    
    
    #split remaining files into validation and test data
    #quick size sanity check. Some rounding errors are expected but sum should be all files
    print(f"total files {len(files)}")
    print(f"{len(train_files)} exp {len(files) * train_ratio}")
    print(f"{len(test_files)} exp {len(files) * test_ratio}")
    print(f"{len(validation_files)} exp {len(files) * validation_ratio}")
    assert( len(train_files) + len(test_files) + len(validation_files) == len(files))
    
    copyFiles(train_files, train_path)
    copyFiles(test_files, test_path)
    copyFiles(validation_files, val_path)
    
  
def copyFiles(files, dest_path):
    for src in files:
        file = os.path.basename(src)
        dst = os.path.join(dest_path, file)
        shutil.copyfile(src, dst)
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--source', required=True,
                        help='source data directory')
    parser.add_argument('--destination', required=True,
                        help='destination data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.source, args.destination)