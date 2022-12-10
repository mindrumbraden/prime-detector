#%%

import numpy as np
import random
import warnings
import pickle

#%%

class SortedArray:
    def __init__(self, an_already_sorted_array, warn_user=True):
        if warn_user:
            warnings.warn("""
                          SortedArray is a minimal class type that assumes 
                          that the passed argument is an np.array that is 
                          already sorted in ascending order. It performs 
                          no checks and has minimal functionality.
                          
                          The sole purpose of this class is to make array 
                          element checking quick when the np.array is sorted. 
                      """)
        self.array = an_already_sorted_array
        
    def __contains__(self, item):
        for i in range(len(self.array)):
            if item == self.array[i]:
                return(True)
            if item < self.array[i]:
                return(False)
            else:
                continue
        return(False)

    def __getitem__(self, item):
         return SortedArray(self.array[item], warn_user=False)
    
#%%

def primes_text_to_array(lines):
    lines = ' '.join(lines)
    lines = lines.split()
    return(np.array([np.uint32(x) for x in lines]))

def create_np_arrays_of_primes_and_composites(file_name, n_primes):
    with open(file_name) as f:
        lines = f.readlines()
    primes = SortedArray(primes_text_to_array(lines), warn_user=False)
    primes = primes[:n_primes]
    composites = np.zeros(primes[-1].array, dtype=np.uint32)
    j = 0
    k = 0
    for i in range(primes[-1].array - 1):
        x = i + 2
        if x in primes[j:]:
            j += 1
        else:
            composites[k] = np.uint32(x)
            k += 1
    composites = np.trim_zeros(composites, trim="b")
    return(primes.array, composites)

def create_train_xy_and_test_xy(primes, composites, seed, 
                                training_size, n_primes):
    primes = np.concatenate(
        [
            np.expand_dims(primes, axis=1),
            np.ones((len(primes), 1), dtype=np.uint32)
        ],
        axis=1
    )
    composites = np.concatenate(
        [
            np.expand_dims(composites, axis=1),
            np.zeros((len(composites), 1), dtype=np.uint32)
        ],
        axis=1
    )
    integers = np.concatenate([primes, composites])
    N = primes[-1][0] - 1 # equal to len(integers), or max integer to consider
    
    random.seed(seed)
    training_indices = np.array(
        random.sample(range(N), round(N * training_size)), dtype=np.uint32
    )
    
    testing_boolean = np.array(
        [True for i in range(N)]
    )
    testing_boolean[training_indices] = False
    testing_data = integers[testing_boolean, :]

    training_boolean = np.array(
        [False for i in range(N)]
    )
    prime_training_indices = training_indices[
        np.where(training_indices < n_primes)[0]
    ]
    composite_training_indices = training_indices[
        np.array(random.sample(
            list(np.where(training_indices >= n_primes)[0]),
            len(prime_training_indices)
            ))
    ]    
    training_boolean[prime_training_indices] = True
    training_boolean[composite_training_indices] = True
    training_data = integers[training_boolean, :]
    
    train_x = training_data[:, 0]
    train_y = training_data[:, 1]
    test_x = testing_data[:, 0]
    test_y = testing_data[:, 1]
    return(train_x, train_y, test_x, test_y)

def int_to_input(n, digits):
    n = str(int(n))
    n = n.rjust(digits, "0")
    result = np.zeros(10 * digits, dtype=np.int32)
    for i, digit in enumerate(reversed(n)):
        result[i * 10 + int(digit)] = 1
    result = np.flip(result)
    #result = np.expand_dims(result, axis=0)
    return(result)

def input_to_int(result):
    result = result.squeeze()
    result = result.tolist()
    n = 0
    for i, binary_digit in enumerate(reversed(result)):
        if binary_digit != 0:
            power = i // 10
            digit = i % 10
            n += digit * 10**power
    return(n)

#%%

def main():
    file_name = "primes.txt"
    n_primes = 100000
    training_size = 0.75
    seed = 13731
    
    primes, composites = create_np_arrays_of_primes_and_composites(
        file_name, n_primes
    )
    train_x, train_y, test_x, test_y = create_train_xy_and_test_xy(
        primes, composites, seed, training_size, n_primes
    )
    train_x = np.array([int_to_input(n, 10) for n in train_x], dtype=np.int32)
    test_x = np.array([int_to_input(n, 10) for n in test_x], dtype=np.int32)
    train_y = np.array(train_y, dtype=np.int32)
    test_y = np.array(test_y, dtype=np.int32)
    
    with open("train_x.pickle", "wb") as handle:
        pickle.dump(train_x, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open("test_x.pickle", "wb") as handle:
        pickle.dump(test_x, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open("train_y.pickle", "wb") as handle:
        pickle.dump(train_y, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open("test_y.pickle", "wb") as handle:
        pickle.dump(test_y, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return(0)

#%%

if __name__ == "__main__":
    main()

#%%