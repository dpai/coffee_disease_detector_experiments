from sklearn.model_selection import train_test_split
from pathlib import Path

class BaseDataProcessor(object):
    _processName = 'Base'
    def __init__(self) -> None:
        pass

class SiameseDataProcessor(BaseDataProcessor):
    _processName = 'Siamese1x1'
    _className = 'SiameseDataProcessor'

    def __init__(self, dataFolder):
        self._rootdir = Path(dataFolder)
        self.traindir = self.rootdir / 'train'
        self.testdir = self.rootdir / 'test'
        self.isproccessed = False
        self.isSplit = False
        self.isSimiPair = False

    @property
    def rootdir(self):
        return self._rootdir
    
    @property
    def traindir(self):
        return self._traindir
    
    @traindir.setter
    def traindir(self, folder):
        self._traindir = folder
    
    @property
    def testdir(self):
        return self._testdir
    
    @testdir.setter
    def testdir(self, folder):
        self._testdir = folder
    
    def buildData(self):
        pass

    def getData(self, splitidx='TRAIN'):
        pass

    def _makePairs(self):
        pass

    def _splitData(self, splitratio, subsplitratio, random_state, shuffle, stratify):
        pass
        # alt_images, alt_test_images, alt_id, alt_test_id, alt_class, alt_test_class = \
        # train_test_split(coffee_test_images, coffee_test_ids, coffee_test_classes,
        #          test_size=0.8, random_state=1234, shuffle=True, stratify=coffee_test_classes)

        # val_images, test_images, val_id, test_id, val_class, test_class = \
        # train_test_split(alt_test_images, alt_test_id, alt_test_class,
        #          test_size=0.5, random_state=1234, shuffle=True, stratify=alt_test_class)