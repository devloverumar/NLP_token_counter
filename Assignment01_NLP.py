import argparse
import string
import re

parser = argparse.ArgumentParser(description='Data Normalization Script')

# Required file name argument
parser.add_argument('input_file', type=str,
                    help='File Name to normalize data')

parser.add_argument('--lower', action='store_true',
                    help='To lower case the text')

parser.add_argument('--stem', action='store_true',
                    help='To stem the tokens')

parser.add_argument('--stopwords', action='store_true',
                    help='To remove stopwords')

parser.add_argument('--sort', action='store_true',
                    help='To sort vocabulary')


args = parser.parse_args()
print(args)

if args.input_file == None:
    print('Input file not provided')

vocab = set([])

stop_words=[]
if args.stopwords:
    with open('stopwords.txt', 'r') as f:
        for word in f:
            word = word.split('\n')
            stop_words.append(word[0])

try:        
    with open('./'+args.input_file,'r') as infile:
        data = infile.read()
        # simple sentence sengmentation: split on .
        sentences = data.split('.')
        all_words=[]
        for sentence in sentences:
            # simple tokenization: split on whitespace
            if args.lower:
                words = sentence.lower().split()
            else:
                words = sentence.split()
            # Update 2: remove punctuation characters from all words then remove empty words
            if args.stem:
                words = [
                        # next line finds patterns and remove them from the string.
                        re.sub(r'less|ship|ing|les|ful|ly|es|s', '', word)
                        for word in words
                    ]
 
            words = [word.translate(str.maketrans('', '', string.punctuation)) for word in words]
            words = [word for word in words if word]
            if args.stopwords:
                words = [word for word in words if word not in stop_words]
            # print(words)
            all_words.extend(words)
            for word in words:
                vocab.add(word)
        
        vocab_dict=dict.fromkeys(vocab, 0)
        # print(all_words)
        for word in all_words:
            vocab_dict[word] +=1
        
        if args.sort:
            vocab_dict=sorted(vocab_dict.items(), key=lambda x:x[1],reverse=True)
        print(vocab_dict)

        print('File reading successful')
        # print(vocab)
        # print(vocab_dict)
            

except IOError as e:
    print(f"I/O error({0}): {1}",e.errno, e.strerror)