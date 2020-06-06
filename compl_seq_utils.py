#!/usr/bin/env python3

import argparse

"""
Script to find complementary subsequences inside of a main sequence.


Copyright 2020 Margherita Maria Ferrari.


This file is part of ComplSeqUtils.

ComplSeqUtils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ComplSeqUtils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ComplSeqUtils.  If not, see <http://www.gnu.org/licenses/>.
"""


class ComplSeqUtils:
    MAPPING_DNA = {'A': ('T',),
                   'T': ('A',),
                   'C': ('G',),
                   'G': ('C',)
                   }

    MAPPING_RNA = {'A': ('U',),
                   'U': ('A', 'G'),
                   'C': ('G',),
                   'G': ('C', 'U')
                   }

    SEQ_TYPE_MAPPING = {'dna': MAPPING_DNA, 'rna': MAPPING_RNA}

    @classmethod
    def __get_complementary_sequence(cls, sequence, seq_type='rna'):
        ret = list()
        mapping = cls.SEQ_TYPE_MAPPING.get(seq_type.lower(), dict())

        for c in sequence[::-1]:
            if c.upper() not in mapping.keys():
                raise AssertionError('Unknown char or mapping not found for "' + c.upper() + '"')

            compl = mapping.get(c.upper(), list)

            if len(compl) > 0:
                if len(ret) == 0:
                    for i in compl:
                        ret.append(i)
                else:
                    for i in range(len(ret)):
                        tmp = ret[i]
                        ret[i] += compl[0]
                        for j in range(1, len(compl)):
                            ret.append(tmp + compl[j])

        return ret

    @classmethod
    def __find(cls, sequence, complementary, num_chars):
        ret = list()

        for start in range(0, len(sequence) - num_chars + 1):
            end = start + num_chars
            if complementary == sequence[start:end]:
                ret.append(str(start + 1) + '-' + str(end))

        return ret

    @classmethod
    def get_args(cls):
        parser = argparse.ArgumentParser(description='Complementary sequences utils')
        parser.add_argument('-i', '--input-file', metavar='IN_FILE', type=str, required=True, help='Input file')
        parser.add_argument('-o', '--output-file', metavar='OUT_FILE', type=str, required=False, help='Output file',
                            default='output.txt')
        parser.add_argument('-n', '--num-chars', metavar='N', type=int, required=True,
                            help='Number of characters in subsequence')
        parser.add_argument('-t', '--seq-type', type=str, required=True, choices=('dna', 'rna'), default='rna',
                            help='Sequence type')
        return parser.parse_args()

    @classmethod
    def find_complementary_sequences(cls, num_chars=0, input_file=None, seq_type='rna', output_file='out.txt'):
        if not input_file or not output_file or num_chars <= 0:
            raise AssertionError('You must specify input file, output file and the character number')

        with open(input_file, 'r') as fin:
            sequence = fin.readline().strip().upper()

        complementary_sequences = dict()
        for start in range(0, len(sequence) - num_chars + 1):
            end = start + num_chars
            subsequence = sequence[start:end]

            if subsequence in complementary_sequences.keys():
                complementary_sequences.get(subsequence, dict())['positions'] = \
                    complementary_sequences.get(subsequence, dict()).get('positions', '') + ', ' + str(start + 1) + \
                    '-' + str(end)
                continue

            complementary = cls.__get_complementary_sequence(subsequence, seq_type)

            for c in complementary:
                res = cls.__find(sequence, c, num_chars)

                if len(res) > 0:
                    results = ''

                    for i in res:
                        results += i + ', '

                    results = results[:len(results) - 2]

                    if complementary_sequences.get(subsequence, None) is None:
                        complementary_sequences[subsequence] = {'positions': str(start + 1) + '-' + str(end),
                                                                'set': ', '.join(map(str, complementary)),
                                                                'items': [{'complementary': c,
                                                                           'num_results': len(res),
                                                                           'results': res,
                                                                           'locations': results
                                                                           }]
                                                                }
                    else:
                        complementary_sequences[subsequence]['items'].append({'complementary': c,
                                                                              'num_results': len(res),
                                                                              'results': res,
                                                                              'locations': results
                                                                              })

        with open(output_file, 'w') as fout:
            fout.write('Sequence: ' + sequence + '\n')
            fout.write('Subsequence Length: ' + str(num_chars) + '\n')

            for k, v in complementary_sequences.items():
                fout.write('\nSubsequence: ' + k + '\n')
                fout.write('Positions: ' + v.get('positions', '') + '\n')
                fout.write('Set of complementary sequences: ' + v.get('set', '') + '\n')
                for item in v.get('items', list()):
                    fout.write('Complementary: ' + item.get('complementary', '') + '\n')
                    fout.write('Locations: ' + item.get('locations', '') + '\n')


if __name__ == '__main__':
    args = vars(ComplSeqUtils.get_args())
    ComplSeqUtils.find_complementary_sequences(args.get('num_chars', 0), args.get('input_file', None),
                                               args.get('seq_type', 'rna'), args.get('output_file', None))
