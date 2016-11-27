import cPickle as pickle
from q4_code_questions import load_variable,save_variable
import matplotlib.pyplot as plt
import numpy as np

def plot_error_hist(exact_freq,error,n_hashes,n_buckets):    
    plt.hist(np.log10(error),np.sqrt(len(error)),'b.')
    plt.title('n_hashes = ' + str(n_hashes) + ', n_buckets = 3*10^' + str(n_buckets))

def plot_error_evol(exact_freq,error,n_hashes,n_buckets):
    plt.plot(exact_freq,error,'b.')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('n_hashes = ' + str(n_hashes) + ', n_buckets = 10^' + str(n_buckets))
    plt.xlabel('word frequency')
    plt.ylabel('Relative error between estimated and actual frequencies')


def load_frequencies(n_hashes,n_buckets):
    return load_variable('saved/approx_word_count_'+str(n_hashes)+'_'+str(n_buckets)+'.pck')

exact_word_counts = load_variable('saved/counts.pck');
total_words = sum(exact_word_counts.values())
exact_counts = [exact_word_counts[k]*1./total_words for k in exact_word_counts.keys()]
idx_subplot = 0 
subplots_idx = [1,2,3,0]
for n_hash in [5]:
    for n_buckets in [4]:        
        approx_counts = load_frequencies(n_hash,n_buckets)
        errors = [ abs(exact_word_counts[k] - approx_counts[k])*1./exact_word_counts[k] for k in exact_word_counts.keys() ]

        plot_error_evol(exact_counts,errors,n_hash,n_buckets)
        idx_subplot += 1

plt.show()
