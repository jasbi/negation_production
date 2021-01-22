import io, os, argparse


### reading in sentences in CoNLL format ###

def conll_read_sentence(file_handle):
	sent = []
	for line in file_handle:
		line = line.strip('\n')
		if line.startswith('#') is False:
			toks = line.split("\t")
			if len(toks) != 10 and sent not in [[], ['']]:
				return sent 
			if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
				sent.append(toks)	

	return None


def Expelliarmus(file):

	neg = []

	age_list = []
	corpus_list = []
	speaker_list = []
	speaker_role_list = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			check = 0

			corpus_info = sent[0][-1].split()
			age = corpus_info[1]
			corpus = corpus_info[-1]
			speaker = sent[0][-2].split()[0]
			speaker_role = sent[0][-2].split()[-1]

			if len(sent) > 1 and age not in ['nan', 'Multiple'] and int(age) >= 12 and int(age) <= 72 and speaker_role in ['Child', 'Target_Child', 'Mother', 'Father']: 

				for tok in sent:
					if tok[1] in ['no', 'not', "n't"]:
					
						check += 1

			if check > 0:
				neg.append(sent)

				age_list.append(age)
				corpus_list.append(corpus)
				speaker_list.append(speaker + ' ' + corpus)
				speaker_role_list.append(speaker_role)

			sent = conll_read_sentence(f)

	return neg, age_list, corpus_list, speaker_list, speaker_role_list


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to all .conllu files')
	parser.add_argument('--neg', type = str, help = 'output .conllu negation file')
	parser.add_argument('--age', type = str, help = 'output file of age distribution')

	args = parser.parse_args()

	path = args.input
	os.chdir(path)

	all_c = 0
	
	all_age_list = []
	all_corpus_list = []
	all_speaker_list = []
	all_speaker_role_list = []

	with io.open(args.neg, 'w', encoding = 'utf-8') as f:

		for file in os.listdir(path):		
			if file.endswith('.conllu'):
				neg_data, age_list, corpus_list, speaker_list, speaker_role_list = Expelliarmus(file)

				for tok in age_list:
					all_age_list.append(tok)

				for tok in corpus_list:
					all_corpus_list.append(tok)

				for tok in speaker_list:
					all_speaker_list.append(tok)

				for tok in speaker_role_list:
					all_speaker_role_list.append(tok)
			
				all_c += len(neg_data)
			
				for neg in neg_data:
					for tok in neg:
						f.write('\t'.join(w for w in tok) + '\n')

					f.write('\n')

	print(all_c)
	print(len(set(all_speaker_list)))
	print(len(set(all_corpus_list)))

	with io.open(args.age, 'w', encoding = 'utf-8') as f:

		f.write('Speaker' + '\t' + 'Role' + 'Age' + '\n')
	
		for z in zip(all_speaker_list, all_speaker_role_list, all_age_list):
			f.write(z[0] + '\t' + z[1] + '\t' + z[2] + '\n')




