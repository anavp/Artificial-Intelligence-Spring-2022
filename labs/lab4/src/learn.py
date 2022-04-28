import io_helper
import helper
import knn
import naive_bayes

def get_classifier():
    if helper.CONSTANTS.ALGO == helper.ALGORITHM.NAIVE_BAYES:
        return naive_bayes.NAIVE_BAYES_CLASSIFIER()
    else:
        return knn.kNN_CLASSIFIER()

if __name__ == '__main__':
    assert issubclass(naive_bayes.NAIVE_BAYES_CLASSIFIER, helper.CLASSIFIER)
    assert issubclass(knn.kNN_CLASSIFIER, helper.CLASSIFIER)
    args = io_helper.parse_args()
    io_helper.init(args)
    classifier = get_classifier()
    classifier.read_input()