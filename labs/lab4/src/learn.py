import io_helper
import classes
import knn
import naive_bayes


def get_classifier() -> classes.CLASSIFIER:
    if classes.CONSTANTS.ALGO == classes.ALGORITHM.NAIVE_BAYES:
        return naive_bayes.NAIVE_BAYES_CLASSIFIER()
    else:
        assert classes.CONSTANTS.ALGO == classes.ALGORITHM.kNN
        return knn.kNN_CLASSIFIER()


def supervised_learning(training_csv: list, testing_csv: list) -> None:
    algo = get_classifier()
    training_data = algo.train(training_csv)
    counts = algo.test(training_data, testing_csv)
    io_helper.print_output(counts)


if __name__ == '__main__':
    assert issubclass(naive_bayes.NAIVE_BAYES_CLASSIFIER, classes.CLASSIFIER)
    assert issubclass(knn.kNN_CLASSIFIER, classes.CLASSIFIER)
    args = io_helper.parse_args()
    training_csv, testing_csv = io_helper.init(args)
    supervised_learning(training_csv, testing_csv)