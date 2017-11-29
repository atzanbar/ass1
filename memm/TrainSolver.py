# Save Model Using Pickle
from sklearn.linear_model import LogisticRegression
import pickle
import sys
from sklearn.datasets import load_svmlight_file

from utilty import get_abs_file


def train_model(in_file):
    X, Y = load_svmlight_file(in_file)

    model = LogisticRegression(solver='sag',max_iter=1000,multi_class='multinomial')
    model.fit(X, Y)
    return model

def save_model(out_file,model):
    pickle.dump(model, open(out_file, 'wb'))

def main(args):
    if (len(args)<3):
        print("wrong args")
        return
    model = train_model(args[1])
    save_model(args[2],model)
    # verify_model(args[2])
    pass
if __name__ == "__main__":
    main(sys.argv)
    # in_file = get_abs_file('..\\out\\feature_map')
    # model_file = ('..\\out\\model_test1')
    # main(["",in_file,model_file])

