import io_helper
import classes

class NAIVE_BAYES_CLASSIFIER(classes.CLASSIFIER):
    class TRAINING_DATA(classes.DATA):
        records = list()
        label_counts = dict()
        attr_counts = list()
        
        def __init__(self):
            super().__init__()
            self.label_counts = dict()
            self.attr_counts = list()

        def __init_attr_counts(self):
            assert self.attribute_ct != -1
            for _ in range(self.attribute_ct):
                self.attr_counts.append(dict())

        def __update_attr_counts(self, label: str, *args):
            assert len(self.attr_counts) == self.attribute_ct
            for i in range(self.attribute_ct):
                for arg in args:
                    if arg not in self.attr_counts[i]:
                        self.attr_counts[i][arg] = dict()
                    self.attr_counts[i][arg][label] = self.attr_counts[i][arg].get(label, 0) + 1

        def add_record(self, *values) -> None:
            self.records.append(classes.RECORD(*values))
            if self.attribute_ct == -1:
                self.attribute_ct = self.records[-1].attribute_ct
                self.__init_attr_counts()
            label = self.records[-1].label
            self.label_counts[label] = self.label_counts.get(label, 0) + 1
            self.record_count += 1
            self.__update_attr_counts(label, *self.records[-1].attributes)
            assert self.record_count == len(self.records)
    
    
    def __init__(self):
        assert issubclass(self.TRAINING_DATA, classes.DATA)
        super().__init__()
    

    def train(self, training_csv: list) -> list:
        assert classes.CONSTANTS.ATTR_CT == -1
        assert classes.CONSTANTS.TRAIN is not None and classes.CONSTANTS.TEST is not None
        classes.CONSTANTS.ATTR_CT = len(training_csv[0]) - 1
        training_data = self.TRAINING_DATA()

        for row in training_csv:
            if len(row) != classes.CONSTANTS.ATTR_CT + 1:
                # io_helper.print_func(f"row: {row}")
                # continue
                break
            training_data.add_record(*row)
        
        return training_data
    
    def __compute_probability(self, training_data: TRAINING_DATA, label: str, attrs: list) -> float:
        prob = training_data.label_counts[label] / training_data.record_count
        for i in range(training_data.attribute_ct):
            prob *= (training_data.attr_counts[i][attrs[i]][label] / training_data.label_counts[label])
        return prob

## label == gt == pd -> tp
## label == gt != pd -> fn
## pd == label != gt -> fp
## gt == pd != label -> tn
## label != gt != pd -> tn

    def test(self, training_data: TRAINING_DATA, testing_csv: list) -> classes.COUNTS:
        counts = classes.COUNTS()
        for row in testing_csv:
            label_gt = row[-1]
            row = row[:-1]
            best_label, max_prob = None, 0.0
            for label in training_data.label_counts:
                prob = self.__compute_probability(training_data, label, row)
                if prob > max_prob:
                    best_label = label
                    max_prob = prob
            for label in training_data.label_counts:
                counts.true_positives[label] = counts.true_positives.get(label, 0)
                if label == label_gt and label_gt == best_label:
                    counts.true_positives[label] += 1
                elif label == label_gt and label_gt != best_label:
                    counts.false_negatives[label] = counts.false_negatives.get(label, 0) + 1
                elif best_label == label:
                    counts.false_positives[label] = counts.false_positives.get(label, 0) + 1
                else: # elif best_label == label_gt:
                    counts.true_negatives[label] = counts.true_negatives.get(label, 0) + 1
        return counts
        

    