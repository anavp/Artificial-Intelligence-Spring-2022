import io_helper
import classes

class NAIVE_BAYES_CLASSIFIER(classes.CLASSIFIER):
    def __init__(self):
        super().__init__()

    def train(self, training_csv) -> list:
        assert classes.CONSTANTS.ATTR_CT == -1
        assert classes.CONSTANTS.TRAIN is not None and classes.CONSTANTS.TEST is not None
        classes.CONSTANTS.ATTR_CT = len(training_csv[0]) - 1
        training_data = classes.DATA()

        for row in training_csv:
            training_data.add_record(*row)
        
        return training_data
    
    def test(self, training_data) -> None:
        pass
        

    