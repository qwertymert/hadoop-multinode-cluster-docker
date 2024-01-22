from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import csv

# Decision tree implementation using MapReduce

class DecisionTree(MRJob):

    def __init__(self, *args, **kwargs):
        super(DecisionTree, self).__init__(*args, **kwargs)
        self.node_id = 0
        self.label_count = None
        self.feature_count = None
        self.impurity = None
        self.threshold = None
        self.feature = None
        self.left = None
        self.right = None
        self.depth = 0
        self.is_leaf = False
        self.label = None

    def configure_args(self):
        super(DecisionTree, self).configure_args()
        self.add_passthru_arg('--max_depth', type=int, default=3)
        self.add_passthru_arg('--min_samples_split', type=int, default=2)
        self.add_passthru_arg('--min_samples_leaf', type=int, default=1)
        self.add_passthru_arg('--max_features', type=int, default=2)

    def mapper(self, _, line):
        row = list(csv.reader([line]))[0]
        x = np.array(row[:-2], dtype=float)
        y = int(row[-2])
        yield self.node_id, (x, y)

    def reducer(self, node_id, values):
        X = []
        y = []
        for x, label in values:
            X.append(x)
            y.append(label)
        X = np.array(X)
        y = np.array(y)
        counts = np.bincount(y, minlength=self.label_count)
        total_count = np.sum(counts)
        self.impurity = 1 - np.sum((counts / total_count) ** 2)
        if total_count < self.min_samples_split or self.depth >= self.max_depth:
            self.is_leaf = True
            self.label = np.argmax(counts)
            yield None, self
        else:
            best_gain = 0
            self.left = DecisionTree()
            self.left.depth = self.depth + 1
            self.left.node_id = self.node_id * 2 + 1
            self.right = DecisionTree()
            self.right.depth = self.depth + 1
            self.right.node_id = self.node_id * 2 + 2
            for feature in range(self.feature_count):
                thresholds = np.unique(X[:, feature])
                for threshold in thresholds:
                    y_left_count = sum([1 for label in y if label <= threshold])
                    y_right_count = sum([1 for label in y if label > threshold])
                    y_left = np.array([1 for label in y if label <= threshold])
                    y_right = np.array([1 for label in y if label > threshold])
                    if y_left_count < self.min_samples_leaf or y_right_count < self.min_samples_leaf:
                        continue
                    gain = self.impurity - (y_left_count * self.calculate_impurity(y_left, y_left_count) + y_right_count * self.calculate_impurity(y_right, y_right_count)) / (y_right_count+ y_left_count)
                    if gain > best_gain:
                        best_gain = gain
                        self.feature = feature
                        self.threshold = threshold
                        if y_left_count < self.min_samples_split or self.left.depth >= self.max_depth:
                            self.left.is_leaf = True
                            self.left.label = np.argmax(np.bincount(y_left, minlength=self.label_count))
                        if y_right_count < self.min_samples_split or self.right.depth >= self.max_depth:
                            self.right.is_leaf = True
                            self.right.label = np.argmax(np.bincount(y_right, minlength=self.label_count))
            if self.feature is None:
                self.is_leaf = True
                self.label = np.argmax(counts)
                yield None, self
            else:
                yield None, self
                yield self.left.node_id, (X[X[:, self.feature] <= self.threshold], y[X[:, self.feature] <= self.threshold])
                yield self.right.node_id, (X[X[:, self.feature] > self.threshold], y[X[:, self.feature] > self.threshold])

    def calculate_impurity(self, counts, total_count):
        probs = counts / total_count
        return 1 - np.sum(probs ** 2)
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer)
        ]
    
    def predict(self, x):
        if self.is_leaf:
            return self.label
        if x[self.feature] <= self.threshold:
            return self.left.predict(x)
        else:
            return self.right.predict(x)

if __name__ == '__main__':
    DecisionTree.run()


    # Example usage:
    # python3 decision_tree.py data.csv --max_depth 3 --min_samples_split 2 --min_samples_leaf 1 --max_features 2
    # python3 decision_tree.py data.csv --max_depth 3 --min_samples_split 2 --min_samples_leaf 1 --max_features 2 > tree.txt
    