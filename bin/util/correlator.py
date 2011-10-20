#!/usr/bin/python

import sys
import itertools

INF = float('inf')

def main():
    try:
        input_path = sys.argv[1]
    except IndexError:
        print_usage()
        exit(0)

    classifiers = None
    relations = [[], ]
    ic = 0

    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue

            if classifiers is None:
                classifiers = line.split(' ')
                print('Found classifiers: {0}'.format(
                        ', '.join(classifiers)))
            else:
                ic += 1
                line_relations = [float(v) for v in line.split(' ')]
                assert len(line_relations) == ic, (
                    'Expected {0} relations, found {1}: {2}'.format(
                        ic, len(line_relations), line)
                    )
                relations.append(line_relations)

                
    best_cls_combinations = []
    classifiers_combinations = ''.join(str(r) for r in range(len(relations)))    
    
    result_comb = []

    for c in range(1, len(relations)):
        min_val = INF
        min_comb = []
        for cls_comb in itertools.combinations(classifiers_combinations, 
                                               c + 1):
            tval = 0
            for pair in (cpair for cpair in itertools.combinations(cls_comb, 2)):
                pair = (int(pair[0]), int(pair[1]))
                if pair[1] > pair[0]:
                    pair = (pair[1], pair[0])
                tval += relations[pair[0]][pair[1]] 

            if tval < min_val:
                min_val = tval
                min_comb = [cls_comb]
            elif tval == min_val:
                min_comb.append(cls_comb)
    
            cls_str = ', '.join(classifiers[int(cid)] for cid in cls_comb)
            result_comb.append((tval, cls_str))

        # for comb in min_comb:
        #     cls_str = ', '.join(classifiers[int(cid)] for cid in comb)
        #     print ('{0} with score: {1}'.format(cls_str, min_val))
    result_comb = sorted(result_comb, key = lambda item: item[0])
    for comb in result_comb:
        print(comb)

def print_usage():
    print('Correlation optimizer')
    print('Usage: ')
    print('{0} [INPUT FILE]'.format(sys.argv))



if __name__ == '__main__':
    main()
