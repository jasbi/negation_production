import io, os, argparse

AUX = ['can', 'could', 'ca', 'dare', 'do', 'did', 'does', 'have', 'had', 'has', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']
COP = ['be', 'is', 'was', 'am', 'are', 'were']

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


### dependents ###

def dependents(index, sent):

	idx_list = []
	d_list = []

	for d in sent:
		if int(d[6]) == int(index):
			idx_list.append(int(d[0]))

	idx_list.sort()

	for idx in idx_list:
		d_list.append(sent[idx - 1])

	return d_list


### has negation marker as dependent? ###

def has_neg(index, sent):

	neg_d = []

	d_list = dependents(index, sent)

	for d in d_list:
		if d[1] in ['not', 'no', "n't"] and d[3] in ['neg', 'qn'] and d[7] not in ['ENUM', 'BEG', 'END', 'COM']:	
			neg_d.append(d)

	return neg_d


### emotion: rejection ###

def emotion(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]
		
			for tok in sent:
				if tok[2] in ['like', 'want', 'wan']:

					idx = int(tok[0]) - 2
				
					if sent[idx][1] in ['not', 'no', "n't"]:
						neg = sent[idx]

						aux = 'NONE'
						aux_stem = 'NONE'
						aux_idx = ''
				
						try:
							idx = int(neg[0]) - 2
							potential = sent[idx]
							if potential[1] in AUX:
								aux_idx = idx
								aux = potential[1]
								aux_stem = potential[2]
						except:
							aux = 'NONE'
							aux_stem = 'NONE'
			
						subj = 'NONE'
						subj_stem = 'NONE'
						subj_idx = ''

						d_list = dependents(tok[0], sent)

						for d in d_list:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]

						head = ''
					
						if tok[2] == 'like':
							head = 'like'
						else:
							head = 'want'

						saying = ' '.join(w[1] for w in sent)

						data.append(['emotion', 'rejection', head, neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


### motor control: rejection ###

def motor(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:
				if tok[2] in ['do', 'can']:

					idx = int(tok[0])
				
					if idx < len(sent) and sent[idx][1] in ['not', 'no', "n't"]:
						neg = sent[idx]

						aux = tok[1]
						aux_stem = tok[2]

						function = ''
						if aux_stem == 'do':
							function = 'prohibition'
						if aux_stem == 'can':
							function = 'inability'
			
						subj = 'NONE'
						subj_stem = 'NONE'
						subj_idx = ''

						d_list = dependents(tok[0], sent)

						for d in d_list:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]

						neg_d = dependents(neg[0], sent)

						for d in neg_d:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]


						head = ''
					
						if tok[6] == '0':
							head = 'root'
						else:
							head = sent[int(tok[6]) - 1]

						if head != 'root':
							head_d = dependents(head[0], sent)

							for d in head_d:

								if d[7] == 'SUBJ':
									subj_idx = d[0]
									subj = d[1]
									subj_stem = d[2]

						saying = ' '.join(w[1] for w in sent)

						data.append(['motor_control', function, head[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


### motor control: rejection ###

def motor(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:
				if tok[2] in ['do', 'can']:

					idx = int(tok[0])
				
					if idx < len(sent) and sent[idx][1] in ['not', 'no', "n't"]:
						neg = sent[idx]

						aux = tok[1]
						aux_stem = tok[2]

						function = ''
						if aux_stem == 'do':
							function = 'prohibition'
						if aux_stem == 'can':
							function = 'inability'
			
						subj = 'NONE'
						subj_stem = 'NONE'
						subj_idx = ''

						d_list = dependents(tok[0], sent)

						for d in d_list:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]

						neg_d = dependents(neg[0], sent)

						for d in neg_d:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]


						head = ''
					
						if tok[6] == '0':
							head = 'root'
						else:
							head = sent[int(tok[6]) - 1]

						if head != 'root':
							head_d = dependents(head[0], sent)

							for d in head_d:

								if d[7] == 'SUBJ':
									subj_idx = d[0]
									subj = d[1]
									subj_stem = d[2]

						saying = ' '.join(w[1] for w in sent)

						data.append(['motor_control', function, head[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


### language learning: labeling ###

def learning(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:

				if tok[2] in ['be']: # and tok[1] in ['am', 'was', 'is', 'are', 'were']:

					neg = ''
				
					try:
						potential = sent[int(tok[0])]
						if potential[1] in ['not', 'no', "n't"]:
							neg = potential
					except:
						neg = ''

					if neg != '':

						tok_d = dependents(tok[0], sent)

						pred = ''
						pred_stem = ''

						for d in tok_d:
							if d[7] == 'PRED' and d[3] in ['n', 'n:pt']:
								pred = d[1]
								pred_stem = d[2]

						function = 'labeling'
			
						subj = 'NONE'
						subj_stem = 'NONE'
						subj_idx = ''

						d_list = dependents(tok[0], sent)

						for d in d_list:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]

						neg_d = dependents(neg[0], sent)

						for d in neg_d:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]

						head = ''
					
						if tok[6] == '0':
							head = 'root'
						else:
							head = sent[int(tok[6]) - 1]

						if head != 'root':
							head_d = dependents(head[0], sent)

							for d in head_d:

								if d[7] == 'SUBJ':
									subj_idx = d[0]
									subj = d[1]
									subj_stem = d[2]

						if pred != '':
							saying = ' '.join(w[1] for w in sent)

							data.append(['learning', function, head[2], neg[1], pred, pred_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


### theory of mind: epistemic ###

def epistemic(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:

				if tok[2] in ['know', 'think', 'remember']: 

					neg = ''
				
					try:
						potential = sent[int(tok[0]) - 2]
						if potential[1] in ['not', 'no', "n't"]:
							neg = potential

					except:
						try:
							far = sent[int(tok[0]) - 2] 
							if far[1] in ['not', 'no', "n't"]:
								neg = far
						except:
							neg = ''

					if neg != '':

						aux = 'NONE'
						aux_stem = 'NONE'
						aux_idx = ''
				
						try:
							idx = int(neg[0]) - 2
							potential = sent[idx]
							if potential[1] in AUX:
								aux_idx = idx
								aux = potential[1]
								aux_stem = potential[2]
						except:
							aux = 'NONE'
							aux_stem = 'NONE'

						function = 'epistemic'
			
						subj = 'NONE'
						subj_stem = 'NONE'
						subj_idx = ''

						d_list = dependents(tok[0], sent)

						for d in d_list:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]

						neg_d = dependents(neg[0], sent)

						for d in neg_d:

							if d[7] == 'SUBJ':
								subj_idx = d[0]
								subj = d[1]
								subj_stem = d[2]

						head = ''
					
						if tok[6] == '0':
							head = 'root'
						else:
							head = sent[int(tok[6]) - 1]

						if head != 'root':
							head_d = dependents(head[0], sent)

							for d in head_d:

								if d[7] == 'SUBJ':
									subj_idx = d[0]
									subj = d[1]
									subj_stem = d[2]

						if subj == 'I' or subj == 'NONE':
							saying = ' '.join(w[1] for w in sent)

							data.append(['theory of mind', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'negation .conllu file')
	parser.add_argument('--output', type = str, help = 'output file')
	parser.add_argument('--domain', type = str, help = 'concept domain')

	args = parser.parse_args()

	path = args.input

	all_domain = {'emotion': emotion, 'motor': motor, 'learning': learning, 'epistemic': epistemic}

	with io.open(args.output, 'w', encoding = 'utf-8') as f:
		f.write('Domain' + '\t' + 'Function' + '\t' + 'Head' + '\t' + 'Negator' + '\t' + 'Aux' + '\t' 'Aux_stem' + '\t' + 'Subj' + '\t' + 'Subj_stem' + '\t' + 'Role' + '\t' + 'Utterance' + '\t' + 'Age' + '\n')
		for tok in all_domain[args.domain](args.input):
			f.write('\t'.join(w for w in tok) + '\n')



