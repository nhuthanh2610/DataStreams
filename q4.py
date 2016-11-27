import sys
import cPickle as pickle
from collections import Counter
from math import log10,floor

def parse_tsv_fields(line):
    return [int(s) for s in line.strip().split('\t')]

def count_lines_of_file(filename):
    count = 0
    with open(filename) as fp:
        for line in fp:
            count +=1
    return count

def get_exact_count_from_file(counts_file):
    count = {}
    with open(counts_file) as fp:
        for line in fp:
            index, count_for_index = parse_tsv_fields(line)
            count[index] = count_for_index
    filename = counts_file.split('.')
    save_variable(count,'saved/'+filename[0].split('/')[-1]+'.pck')
    return count

def load_hash_params(hash_params_file):
    hash_params = []
    with open(hash_params_file) as fp:
        for line in fp:
            a, b = parse_tsv_fields(line)
            hash_params.append((a,b))
    return hash_params

def is_prime(p):
    for i in range(2, p):
        if (p % i) == 0:
            return False
    return True

def print_frequency_of_first(k, word_count, tot_word_count):
    for i in range(1,k+1):
        print "Word %d has count: %d \t (frequency %f)" % (i, word_count[i], float(word_count[i])/tot_word_count)

def hash_fun(a, b, p, n_buckets, x):
    y = x % p
    hash_val = (a*y + b) % p
    return hash_val % n_buckets

def approximate_count(word, count, n_buckets, n_hashes, p, hash_params):
    min_count = None
    for j in range(n_hashes):
        a, b = hash_params[j]
        hash_bucket = hash_fun(a, b, p, n_buckets, word)
        new_count = count[j][hash_bucket]

        
        if min_count:
            min_count = min(min_count, new_count)
        else:
            min_count = new_count
    return min_count

def ds_algorithm(dataset_file, count, n_buckets, n_hashes, p, hash_params, n_lines, report_freq,):
    print "Starting data stream algorithm"
   
    repor_freq = 1000
    report_iters = [(n_lines * i) / report_freq for i in range(1,report_freq)]

    with open(dataset_file) as fp:
        for line_number, line in enumerate(fp):
            word, = parse_tsv_fields(line)
            for j in range(n_hashes):
                a, b = hash_params[j]
                hash_bucket = hash_fun(a, b, p, n_buckets, word)
                count[j][hash_bucket] += 1

           
            if line_number in report_iters:
                completion = 1 + report_iters.index(line_number)
                print "Completion: %d / %d" % (completion, report_freq)

def compare_first_words_from(dataset_file, counts_file, k, report_freq, p, n_buckets,n_hashes):

    print "*** Data_stream algorithm, Cs246 Hw4q4 ***"
    print "Input dataset: %s (counts file: %s)" % (dataset_file, counts_file)

    n_lines = count_lines_of_file(dataset_file)
    exact_word_count = get_exact_count_from_file(counts_file)
    hash_params = load_hash_params("hash_params.txt")


    print "Input stream has %d entries of %d distinct words" % (n_lines, len(exact_word_count))
    print "DS Algorithm uses %d buckets" %(n_hashes*n_buckets)

    count = {}
    for j in range(n_hashes):
        count[j] = {}
        for x in range(n_buckets):
            count[j][x]=0

    ds_algorithm(dataset_file, count, n_buckets, n_hashes, p, hash_params, n_lines, report_freq)

    approx_word_count = {}

    if k == -1:
        k = max(exact_word_count.keys())

    for word in range(1,k + 1):
        approx_word_count[word] = approximate_count(word, count, n_buckets, n_hashes, p, hash_params)

    if k < 20:
        print "--- First %d words, exact counts ---" % k
        print_frequency_of_first(k, exact_word_count, n_lines)
        print "--- First %d words, approx counts ---" % k
        print_frequency_of_first(k, approx_word_count, n_lines)
    else:
        filename = 'saved/approx_word_count_' + str(n_hashes)+'_'+str(int(floor(log10(n_buckets))))+'.pck'
        save_variable(approx_word_count,filename);

def save_variable(var,filename):
    print 'saving ',filename
    pickle.dump(var,open(filename,'wb'))
    return True

def load_variable(filename):
    print 'loading ',filename
    return pickle.load(open(filename,'rb'));

def generate_filename(lst):
    return '_'.join(lst)

def main():
    """
    very_small_counts = get_exact_count_from_file('counts_very_small.txt')
    save_variable(very_small_counts,'saved/counts_very_small.pck')
    small_counts = get_exact_count_from_file('counts_small.txt')
    save_variable(small_counts,'saved/counts_small.pck')
    """

    p = 123457 
    n_buckets = 3*10**4 
   
    if len(sys.argv[1:]) not in [4,5]:
        print "Usage: python q4_code.py words.txt counts.txt n_hashes k n_buckets [reporting_freq]"
        return
    if len(sys.argv[1:]) == 5:
        dataset_file, counts_file, n_hashes, k,n_buckets = sys.argv[1:]
        reporting_frequence = 100
    else:
        dataset_file, counts_file, n_hashes, k, n_buckets, reporting_frequence = sys.argv[1:]

    compare_first_words_from(dataset_file, counts_file, int(k), int(reporting_frequence), int(p), int(n_buckets),int(n_hashes))

if __name__ == "__main__":
    main()
