import io_helper
import classes

class kNN_CLASSIFIER(classes.CLASSIFIER):
    def __init__(self):
        super().__init__()

    def train(self, training_data) -> list:
        assert classes.CONSTANTS.ATTR_CT == -1
        assert classes.CONSTANTS.TRAIN is not None and classes.CONSTANTS.TEST is not None
        # assert type(helper.CONSTANTS.TRAIN) == list and type(helper.CONSTANTS.TEST) == list

        classes.CONSTANTS.ATTR_CT = len(classes.CONSTANTS.TRAIN[0]) - 1
    
    def test(self, training_data, testing_csv: list) -> classes.COUNTS:
        pass