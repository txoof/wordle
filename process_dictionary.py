#!/usr/bin/env python3
# coding: utf-8





word_list = './valid-wordle-words.txt'
min_word_length = 5
max_word_length = 5
max_letter_combinations = 3
rounding_places = 8






import json
import random
from collections import OrderedDict
from operator import getitem
from itertools import product 
import csv






# local
from pathlib import Path
word_file = Path(word_list)






def range_char(start, stop):
    '''generator for all characters in range `start:stop`
    
    works effectively for upper:upper or lower:lower case letters'''
    return (chr(n) for n in range(ord(start), ord(stop) + 1))






def sample_dict(d, n):
    r = {}
    for i in random.sample(sorted(d), n):
        r[i] = d[i]
    return r






def flatten_dict(d, h):
    fd = []

    for key, values in d.items():
        entry = {}
        entry[h] = key
        entry.update(values)
        fd.append(entry)
        
    return fd






all_words = {}
with open(word_file, 'r') as f:
    for line in f:
        all_words[line.strip()] = len(line.strip())
    
    






# sort dictionary by word length
new_d = {}
for k in sorted(all_words_dict, key=len, reverse=False):
    new_d[k] = all_words_dict[k]






accepted_words = {}
for k in new_d:
    # pull words of matching length
    if len(k) >= min_word_length and len(k) <= max_word_length:
        accepted_words[k] = {}
        
    # stop after first word that is too long
    if len(k) > max_word_length:
        break






# create dictionary of letter combination dictionaries with all cartesian product of characters a..z:
c_product_dicts = {}
for length in range(1, max_letter_combinations+1):
    # create a dictionary for each length
    c_product_dicts[length] = {}
#     for i in permutations(''.join(range_char('a', 'z')), length):
    for i in product(range_char('a', 'z'), repeat = length):
        c_product_dicts[length][''.join(i)] = {'total': 0, 'percent': 0, 'score': None}






for word in accepted_words:
    for i, letter in enumerate(word):
        for j in range(1, max_letter_combinations+1):
            if i+j > len(word):
                pass
            else:
                w_slice=(f'{word[i:i+j]}')
                c_product_dicts[j][w_slice]['total'] += 1






dictionary_bins = {}
for dictionary, letter_space in c_product_dicts.items():
    # create bins for values
    dictionary_bins[dictionary] = {'total': 0, 'bins': []}
    # sum up the total occurences of each value in the letter space
    for key, value in letter_space.items():
        dictionary_bins[dictionary]['total'] += value['total']
    # assign a percent score for each value
    value_list = []
    for key, value in letter_space.items():
        value['percent'] = round(value['total']/dictionary_bins[dictionary]['total'], rounding_places)
        value_list.append(value['percent'])
    # re-order the space by highest percent value first
    c_product_dicts[dictionary] = OrderedDict(
        sorted(letter_space.items(), key=lambda x: getitem(x[1], 'percent'), reverse=True))
    dictionary_bins[dictionary]['bins'] = sorted(set(value_list), reverse=True)
    
    # score each value in letter_space using bin index (lower scores are better)
    for key, value in letter_space.items():
        value['score'] = dictionary_bins[dictionary]['bins'].index(value['percent'])






# consider stripping out all values in letter space with score of 0






# pull N random words from dictionary

# test_words = sample_dict(accepted_words, 10)
# test_words






# this is expensive to run!
# calculate the score of each word for each value in the letter spaces
for word, data in accepted_words.items():
    for dictionary, letter_space in c_product_dicts.items():
        score = 0
        for item in letter_space:
            count = word.count(item)
            score += letter_space[item]['score'] * count           
        data[dictionary] = score






# create CSV friendly rendering of frequency data
freqeuncy_csv = []
for d, values in c_product_dicts.items():
    freqeuncy_csv.extend(flatten_dict(values, 'letter'))
accepted_words_csv = flatten_dict(accepted_words, 'word')

# remove all words with duplicate characters
accepted_words_no_dupes_csv = []
for word in accepted_words_csv:
    if len(set(word['word'])) == len(word['word']):
        accepted_words_no_dupes_csv.append(word)
        

# sort based lowest score for first three keys
accepted_words_sorted_csv = sorted(accepted_words_csv, key=lambda d: (d[1], d[2], d[3]))
accepted_words_no_dupes_sorted_csv = sorted(accepted_words_no_dupes_csv, key=lambda d: (d[1], d[2], d[3]))






csv_files = [
    {'file_name': 'frequency.csv', 'var': freqeuncy_csv, 'fieldnames': freqeuncy_csv[0].keys()},
    {'file_name': 'accepted_words.csv', 'var': accepted_words_csv, 'fieldnames': accepted_words_csv[0].keys()},
    {'file_name': 'accepted_words_sorted.csv', 'var': accepted_words_sorted_csv, 'fieldnames': accepted_words_sorted_csv[0].keys()},
    {'file_name': 'accepted_words_no_dupes_sorted.csv', 'var': accepted_words_no_dupes_csv, 'fieldnames': accepted_words_no_dupes_csv[0].keys()}
]






for file in csv_files:
    with open(file['file_name'], 'w') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=file['fieldnames'])
        writer.writeheader()
        writer.writerows(file['var'])
    









