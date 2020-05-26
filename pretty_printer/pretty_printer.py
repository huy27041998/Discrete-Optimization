import argparse
def solve(filename, L):
    with open(filename, 'r', encoding='utf-8') as f:
        paragraphs = f.read().splitlines()
    for index, paragraph in enumerate(paragraphs):
        words = paragraph.split()
        d = [0 for i in range(len(words)+1)]
        pre = [0 for i in range(len(words)+1)]
        for i in range(1, len(words) + 1):
            d[i] = d[i-1] + (L - len(words[i-1])) ** 2
            s = len(words[i-1])
            pre[i] = i-1
            for j in range(i-1, 0, -1):
                if (s + len(words[j-1]) + 1 <= L) :
                    s += len(words[j-1]) + 1
                    tmp = d[j - 1] + (L - s) ** 2
                    if (tmp < d[i]):
                        d[i] = tmp
                        pre[i] = j-1
                else: 
                    break
        k = len(words)
        traceback = [k]
        while (k != 0):
            traceback.insert(0, pre[k])
            k = pre[k]
        for i in range(len(traceback) - 1):
            for j in range(traceback[i], traceback[i+1]):
                if j != traceback[i+1]-1:
                    print(words[j], end=' ')
                elif j == len(words)-1:
                    print(words[j], end='')
                elif j == traceback[i+1] - 1:
                    print(words[j], end='\n')
        if index != len(paragraphs) - 1:
            print('\n')
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help='Path to file', type=str)
ap.add_argument("-l", "--length", required=True, help='Length of line', type=int)
args = vars(ap.parse_args())
filename = args['file']
L = args['length']
solve(filename, L)