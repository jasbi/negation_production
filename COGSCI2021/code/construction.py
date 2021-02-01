import io, os, argparse

AUX = ['can', 'could', 'ca', 'dare', 'do', 'did', 'does', 'have', 'had', 'has', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']
COP = ['be', 'is', 'was', 'am', 'are', 'were']
SUBJ = ['I', 'you', 'she', 'he', 'they', 'it', 'we']

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

					neg = ''
				
					try:
						potential = sent[int(tok[0]) - 2]
						if potential[1] in ['not', 'no', "n't"]:
							neg = potential

					except:
						try:
							far = sent[int(tok[0]) - 3] 
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

						function = 'rejection'
			
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

					#	if subj == 'I' or subj == 'NONE':
						saying = ' '.join(w[1] for w in sent)

						data.append(['emotion', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

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
							far = sent[int(tok[0]) - 3] 
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

					#	if subj == 'I' or subj == 'NONE':
						saying = ' '.join(w[1] for w in sent)

						data.append(['theory of mind', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


### motor control ###

def motor(file):

	data = []
	check = 0

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:
				if tok[2] in ['do', 'can']:

					idx = int(tok[0])

					pre = ''
					try:
						pre = sent[int(tok[0]) - 2][2]
					except:
						pre = ''

					post = ''
					try:
						post = sent[idx + 1][2]
					except:
						post = ''
				
					if idx < len(sent) and sent[idx][1] in ['not', 'no', "n't"] and post not in SUBJ:
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

						if pre in SUBJ and subj == 'NONE':
							subj = pre 
							subj_stem = pre
					
						head = ''
						head_lemma = ''
					
						if tok[6] == '0':
							head = 'root'
						else:
							head = sent[int(tok[6]) - 1]
							head_lemma = head[2]

						if head != 'root':
							head_d = dependents(head[0], sent)

							for d in head_d:

								if d[7] == 'SUBJ':
									subj_idx = d[0]
									subj = d[1]
									subj_stem = d[2]

						saying = ' '.join(w[1] for w in sent)

						if int(neg[0]) == len(sent): 

							data.append(['motor_control', function, head[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

						if int(neg[0]) < len(sent):

							### exclude emotion ###

							if sent[int(neg[0])][2] not in ['like', 'want', 'know', 'think', 'remember', 'have']:
								if head_lemma not in ['like', 'want', 'know', 'think', 'remember', 'have']:
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

						post = ''
						try:
							post = sent[int(tok[0]) + 1][2]
						except:
							post = ''

						tok_d = dependents(tok[0], sent)

						pred = ''
						pred_stem = ''
						pred_pos = ''

						for d in tok_d:
							if d[7] == 'PRED' and (d[3] in ['n', 'n:pt'] or d[3].startswith('adj') or d[3].startswith('pro')):
								pred = d[1]
								pred_stem = d[2]
								pred_pos = d[3]

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

						if pred != '' and subj_stem not in ['there', 'There'] and post not in SUBJ:
							saying = ' '.join(w[1] for w in sent)

							data.append(['learning', function, head[2], neg[1], pred_pos, pred_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


### Perception ###

def perception(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:

				if tok[2] in ['no', "not", "n't"] and int(tok[0]) < len(sent):

					h = sent[int(tok[6]) - 1]
					pre = ''

					try:
						pre = sent[int(tok[0]) - 2][2]
					except:
						pre = ''
					
					if (sent[int(tok[0])][2] in ['have', 'HAVE']) or (pre not in AUX and (h[3] in ['n', 'n:pt'] or h[3].startswith('pro')) and h[2] not in ['not', 'thank_you'] and sent[int(tok[0])][3].startswith('v') is False and sent[int(tok[0])][2] not in ['Mom', 'mom', 'mum', 'Mum', 'Mummy', 'mummy', 'mommy', 'Mommy', 'dad', 'Daddy', 'daddy', 'Dad']):
						existence = ''
						copula = ''

						try:
							copula = sent[int(h[6]) - 1]

							if copula[2] in ['be']:
								try:
									temp = sent[int(copula[0]) - 2]

									if temp[2] in ['there', 'There']:
										existence = 'YES'
								except:
									existence = 'NO'
							else:
								existence = ''
						except:
							existence = ''

					
						function = ''

						if existence in ['YES']:
							function = 'existence'

						else:
							if existence not in ['YES', 'NO'] and (sent[int(tok[0])][2] in ['have', 'Have'] or sent[int(tok[0])][2] in ['mine', 'yours', 'hers', 'his', 'theirs', 'ours', 'its'] or "'s" in sent[int(tok[0])][3]):
								function = 'possession'
							else:
								if existence not in ['YES', 'NO'] and (h[3] in ['n', 'n:pt'] or sent[int(tok[0])] not in ['mine', 'yours', 'hers', 'his', 'theirs', 'ours', 'its']):
									function = 'existence'

						saying = ' '.join(w[1] for w in sent)

						if function != '':
							data.append(['perception', function, h[2], tok[2], '_', '_', '_', '_', speaker_role, saying, age])
					
				### no more ###

					if sent[int(tok[0])][2] == 'more':

						h = ''

						try:
							h = sent[int(tok[0]) + 1]
						except:
							h = ''

						pre = ''

						try:
							pre = sent[int(tok[0]) - 2][2]
						except:
							pre = ''

						if h != '' and ((sent[int(tok[0])][2] in ['have', 'HAVE']) or (pre not in AUX and (h[3] in ['n', 'n:pt'] or h[3].startswith('pro')) and h[2] not in ['not', 'thank_you'] and sent[int(tok[0])][3].startswith('v') is False and sent[int(tok[0])][2] not in ['Mom', 'mom', 'mum', 'Mum', 'Mummy', 'mummy', 'mommy', 'Mommy', 'dad', 'Daddy', 'daddy', 'Dad'])):
				
							existence = ''
							copula = ''

							try:
								copula = sent[int(h[6]) - 1]

								if copula[2] in ['be']:
									try:
										temp = sent[int(copula[0]) - 2]

										if temp[2] in ['there', 'There']:
											existence = 'YES'
									except:
										existence = 'NO'
								else:
									existence = ''
							except:
								existence = ''

							function = ''

							if existence in ['YES']:
								function = 'existence'

							else:
								if existence not in ['YES', 'NO'] and (sent[int(tok[0])][2] in ['have', 'Have'] or sent[int(tok[0])][2] in ['mine', 'yours', 'hers', 'his', 'theirs', 'ours', 'its'] or "'s" in sent[int(tok[0])][3]):
									function = 'possession'
								else:
									if existence not in ['YES', 'NO'] and (h[3] in ['n', 'n:pt'] or sent[int(tok[0])] not in ['mine', 'yours', 'hers', 'his', 'theirs', 'ours', 'its']):
										function = 'existence'

							if int(tok[0]) == 1 and function != 'possession':							
								function = 'existence'

							saying = ' '.join(w[1] for w in sent)

							if function != '':
								data.append(['perception', function, h[2], tok[2], '_', '_', '_', '_', speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data

### causal###

def causal(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:

				if tok[2] in ['why', 'Why']: 

					neg = ''
					follow = ''
				
					try:
						potential = sent[int(tok[0])]
						if potential[1] in ['not', 'no', "n't"]:
							neg = potential

							try:
								follow = sent[int(tok[0]) + 1]
								if follow[2] in ['like', 'want', 'know', 'think', 'remember', 'have']:
									follow = 'EXCLUDE'
							except:
								follow = 'INCLUDE'

					except:
						try:
							far = sent[int(tok[0]) + 1] 
							if far[1] in ['not', 'no', "n't"]:
								neg = far

								try:
									follow = sent[int(tok[0]) + 2]
									if follow[2] in ['like', 'want', 'know', 'think', 'remember', 'have']:
										follow = 'EXCLUDE'
								except:
									follow = 'INCLUDE'

						except:
							neg = ''

					if neg != '' and follow == 'INCLUDE':

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

						function = 'causal'
			
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

					#	if subj == 'I' or subj == 'NONE':
						saying = ' '.join(w[1] for w in sent)

						data.append(['unknown', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


### Event description ###

def event(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
		
			speaker_role = sent[0][-2].split()[-1]
			age = sent[0][-1].split()[1]

			for tok in sent:

				if tok[3].startswith('v') and tok[2] not in ['like', 'want', 'know', 'think', 'remember', 'have']: 

					neg = ''
					pre = ''
				
					try:
						potential = sent[int(tok[0]) - 2]
						if potential[1] in ['not', 'no', "n't"]:
							neg = potential
							try:
								pre = sent[int(tok[0]) - 3]
								if pre[2] in ['why', 'Why']:
									pre = 'EXCLUDE'
							except:
								pre = 'INCLUDE'

					except:
						try:
							far = sent[int(tok[0]) - 3] 
							if far[1] in ['not', 'no', "n't"]:
								neg = far
								try:
									pre = sent[int(tok[0]) - 3]
									if pre[2] in ['why', 'Why']:
										pre = 'EXCLUDE'
								except:
									pre = 'INCLUDE'
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

						function = 'event'
			
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

					#	if subj == 'I' or subj == 'NONE':
						saying = ' '.join(w[1] for w in sent)

						data.append(['perception', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age])

			sent = conll_read_sentence(f)

	return data


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'negation .conllu file')
	parser.add_argument('--output', type = str, help = 'output file')
	parser.add_argument('--domain', type = str, help = 'concept domain')

	args = parser.parse_args()

	path = args.input

	all_domain = {'emotion': emotion, 'motor': motor, 'learning': learning, 'epistemic': epistemic, 'perception': perception}

	with io.open(args.output, 'w', encoding = 'utf-8') as f:
		f.write('Domain' + '\t' + 'Function' + '\t' + 'Head' + '\t' + 'Negator' + '\t' + 'Aux' + '\t' 'Aux_stem' + '\t' + 'Subj' + '\t' + 'Subj_stem' + '\t' + 'Role' + '\t' + 'Utterance' + '\t' + 'Age' + '\n')
		for tok in all_domain[args.domain](args.input):
			f.write('\t'.join(w for w in tok) + '\n')



