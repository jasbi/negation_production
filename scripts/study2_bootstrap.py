import io, argparse, csv, os, random, statistics


def check_file(file_handle):
	with io.open(file_handle, encoding = 'utf-8') as f:
		for line in f:
			toks = line.split()
			if len(toks) == 0:
				return 'Something is Wrong'

### reading in sentences in CoNLL format ###

def conll_read_sentence(file_handle):

	sent = []

	for line in file_handle:
		line = line.strip('\n')
	
		if line.startswith('#') is False :
			toks = line.split("\t")			
		
			if len(toks) == 1:
				return sent 
			else:
				if toks[0].isdigit() == True:
					sent.append(toks)

	return None


def full_sentence(sentence):

	v = ''
	subj = ''

	for tok in sentence:
		if tok[3] == 'v' and tok[7] == 'ROOT':
			v = tok[0]
		if tok[7] == 'SUBJ':
			subj = tok[0]

	if len(v) != 0 and len(subj) != 0 and int(subj) < int(v):

		return [v, subj]

	return False


def has_negation(sentence):

	negation = {}

	no = []
	nt = []
	nOt = []

	for tok in sentence:
		if tok[1] == 'no':
			no.append(tok[0])
		if tok[1] == 'not':
			if tok[2] == "n't":
				nt.append(tok[0])
			else:
				nOt.append(tok[0])

	if len(no) != 0:
		negation['no'] = no 
	if len(nt) != 0:
		negation["n't"] = nt 
	if len(nOt) != 0:
		negation['not'] = nOt

	if len(negation) != 0:
		return negation

	return None



def study2(trajectory):

	info = []

	for age, sentences in trajectory.items():

		full_sent = []
		full_sent_c = 0

		for sent in sentences:

			full = full_sentence(sent)

			if full is not False:
				full_sent.append(sent)

		if len(full_sent) != 0:
			full_sent_c = len(full_sent)

			all_duplicate = []
			all_duplicate_annotation = []
			all_pre = []
			all_inter = []
			all_post = []
			all_pre_annotation = []
			all_inter_annotation = []
			all_post_annotation = []

		#### Start bootstrapping ####

			for time in range(10000):
				sample = random.choices(full_sent, k = full_sent_c)

				duplicate = 0
				duplicate_annotation = 0

				pre = 0
				inter = 0
				post = 0

				pre_annotation = 0
				inter_annotation = 0
				post_annotation = 0

				for sent in sample:
					negation = has_negation(sent)

					if negation is not None:
						full = full_sentence(sent)
						root = full[0]
						subj = full[1]

						neg_mod = []
						neg_mod_annotation = []

						for k, v in negation.items():

							for i in v:

						### Extracting negation based on just index ###

								if int(i) < int(subj):
									pre += 1
								if int(i) > int(subj) and int(i) < int(root):
									inter += 1
								if int(i) > int(root):
									post += 1
							
								neg_mod.append(i)

					
						### Extracting negation based on dependency annotation ###

								h = sent[int(sent[int(i) - 1][6]) - 1]

						#### if negation modifies an auxiliary, which is the child of the root verb, or head of the root verb ####
						#### dealing with different treatment of AUX and head verb in CHILDES ####

								if (h[7] =='AUX' and h[6] == root) or (h[7] == 'AUX' and sent[int(root) - 1][6] == h[0]):
									neg_mod_annotation.append(i)

						#### if negation directly modifies the root verb ####

								if h[0] == root:
									neg_mod_annotation.append(i)

#						print(neg_mod)
#						print(neg_mod_annotation)
						if len(neg_mod) > 1:
							duplicate += len(neg_mod) - 1

						if len(neg_mod_annotation) > 1:
							duplicate_annotation += len(neg_mod_annotation) - 1

						for i in neg_mod_annotation:
					#	print(sent)
							if int(i) < int(subj):
								pre_annotation += 1
							if int(i) > int(subj) and int(i) < int(root):
								inter_annotation += 1
							if int(i) > int(root):
								post_annotation += 1
				
				all_duplicate.append(round(duplicate * 100 / full_sent_c,2))
				all_duplicate_annotation.append(round(duplicate_annotation * 100 / full_sent_c, 2))
				all_pre.append(round(pre * 100 / full_sent_c, 2))
				all_inter.append(round(inter * 100 / full_sent_c, 2))
				all_post.append(round(post * 100 / full_sent_c, 2))
				all_pre_annotation.append(round(pre_annotation * 100 / full_sent_c, 2))
				all_inter_annotation.append(round(inter_annotation * 100 / full_sent_c, 2))
				all_post_annotation.append(round(post_annotation * 100 / full_sent_c, 2))

			all_duplicate.sort()
			all_duplicate_annotation.sort()
			all_pre.sort()
			all_inter.sort()
			all_post.sort()
			all_pre_annotation.sort()
			all_inter_annotation.sort()
			all_post_annotation.sort()

			info.append([age, 'Duplicate', statistics.mean(all_duplicate), all_duplicate[250], all_duplicate[9750], full_sent_c, len(sentences)])
			info.append([age, 'Duplicate_annotation', statistics.mean(all_duplicate_annotation), all_duplicate_annotation[250], all_duplicate_annotation[9750], full_sent_c, len(sentences)])
			info.append([age, 'Pre', statistics.mean(all_pre), all_pre[250], all_pre[9750], full_sent_c, len(sentences)])
			info.append([age, 'Pre_annotation', statistics.mean(all_pre_annotation), all_pre_annotation[250], all_pre_annotation[9750], full_sent_c, len(sentences)])
			info.append([age, 'Post', statistics.mean(all_post), all_post[250], all_post[9750], full_sent_c, len(sentences)])
			info.append([age, 'Post_annotation', statistics.mean(all_post_annotation), all_post_annotation[250], all_post_annotation[9750], full_sent_c, len(sentences)])
			info.append([age, 'Inter', statistics.mean(all_inter), all_inter[250], all_inter[9750], full_sent_c, len(sentences)])
			info.append([age, 'Inter_annotation', statistics.mean(all_inter_annotation), all_inter_annotation[250], all_inter_annotation[9750], full_sent_c, len(sentences)])

	return info


def Expelliarmus(file_handle, directory):

	data = []

	child_trajectory = {}
	parent_trajectory = {}

	child = 'nan'

	with io.open(directory + '/' + file_handle, encoding = 'utf-8') as f:

		sent = conll_read_sentence(f)

		while sent is not None:

			age = sent[0][-1].split()[1]

			if age != 'nan':
				age = int(float(age))

				if age <= 72:

					role = sent[0][-2].split()

					child = role[0]

					if role[-1] in ['Mother', 'Father']:
						parent_trajectory[age] = []

					if role[-1] in ['Target_Child']:
						child_trajectory[age] = []

					data.append(sent)

			sent = conll_read_sentence(f)

	if len(data) != 0:

		for k, v in child_trajectory.items():
			print(k)
#		print(len(data))
		for sent in data:
		
			age = int(float(sent[0][-1].split()[1]))
			role = sent[0][-2].split()

			if role[-1] in ['Target_Child']:
				child_trajectory[age].append(sent)

			if role[-1] in ['Mother', 'Father']:
				parent_trajectory[age].append(sent)
#	print(child_trajectory)
	child_info = study2(child_trajectory)
	parent_info = study2(parent_trajectory)

	return child_info, parent_info, child


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input path to .conllu file including all English-NA data')
	parser.add_argument('--output', type = str, help = 'output negation file')

	args = parser.parse_args()

	path = args.input
	os.chdir(path)

	output = io.open(args.output, 'w', newline = '', encoding = 'utf-8')
	writer = csv.writer(output)

	writer.writerow(['Role', 'Age', 'Feature', 'Mean', 'CI25', 'CI975', 'Num_full_sentence', 'Num_of_sentence'])

	for file in os.listdir(path):

		if file.endswith('CHILDES.conllu'):

			check_file(file)
		
		#	corpus = file.split('_')[1][0 : -7]

			child_info, parent_info, target_child = Expelliarmus(file, path)

			for tok in child_info:
				tok.insert(0, 'Target_Child')
				writer.writerow(tok)

			for tok in parent_info:
				tok.insert(0, 'Parent')
				writer.writerow(tok)













