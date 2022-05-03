import io_helper
import classes
import sys

class kNN_CLASSIFIER(classes.CLASSIFIER):
    class TRAINING_DATA(classes.DATA):
        def __init__(self):
            super().__init__()
            self.labels_list = list()
        
        def add_record(self, *values) -> None:
            self.records.append(classes.RECORD(*values))
            self.record_count += 1
            if self.records[-1].label not in self.labels_list:
                assert values[-1] == self.records[-1].label
                self.labels_list.append(self.records[-1].label)

    def __init__(self):
        assert issubclass(self.TRAINING_DATA, classes.DATA)
        super().__init__()

    def train(self, training_csv: list) -> classes.DATA:
        assert classes.CONSTANTS.ATTR_CT == -1
        assert classes.CONSTANTS.TRAIN is not None and classes.CONSTANTS.TEST is not None
        training_data = self.TRAINING_DATA()

        for row in training_csv:
            training_data.add_record(*row)
        return training_data
    
    def __compute_distance(self, point1: classes.RECORD, point2: classes.RECORD) -> int:
        assert len(point1.attributes) == len(point2.attributes)
        assert point1.attribute_ct == point2.attribute_ct
        assert point1.attribute_ct == len(point1.attributes)
        dist = 0.0
        for i in range(point1.attribute_ct):
            dist += ((int(point1.attributes[i]) - int(point2.attributes[i]))**2)
        return dist
    
    def test(self, training_data: TRAINING_DATA, testing_csv: list) -> classes.COUNTS:
        counts = classes.COUNTS()
        for row in testing_csv:
            votes = dict()
            distances = list()
            cur_record = classes.RECORD(*row)
            for record in training_data.records:
                distances.append((record.label, self.__compute_distance(record, cur_record)))
            distances.sort(key=lambda y: y[1])
            for i, distance in enumerate(distances):
                if i >= classes.CONSTANTS.K:
                    break
                cur_val = ((1.0 / distance[1]) if distance[1] != 0 else sys.maxsize)
                votes[distance[0]] = votes.get(distance[0], 0) + cur_val
            label_gt = cur_record.label
            assert label_gt == row[-1]
            best_label = max(votes, key = votes.get)
            io_helper.print_func(f"want={label_gt} got={best_label}")
            for label in training_data.labels_list:
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