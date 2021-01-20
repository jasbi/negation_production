## wget -r -l1 -H -t1 -nd -N -np -A.zip -erobots=off https://childes.talkbank.org/data-xml/Eng-NA/

import io, xmltodict, os, argparse

HAPPY = True

def how_old(number):
	age = 0
	number = list(number)
	if 'Y' in number:
		y_id = number.index('Y')
		age += int(' '.join(n for n in number[1 : y_id])) * 12
	if 'M' in number:
		m_id = number.index('M')
		age += int(number[m_id - 2]) * 10 + int(number[m_id - 1])
	return age


def basic_info(chat):

	ActivityType = ''
	try:
		ActivityType = chat['CHAT']['@ActivityType']
	except:
		ActivityType = 'nan'

	Lang = ''
	try:
		Lang = chat['CHAT']['@Lang']
	except:
		Lang = 'nan'

	Corpus = ''
	try:
		Corpus = chat['CHAT']['@Corpus']
	except:
		Corpus = 'nan'

	Participants = {}

	for p in chat['CHAT']['Participants']['participant']:
		speaker_id = ''
		try:
			speaker_id = p['@id']
		except:
			p = chat['CHAT']['Participants']['participant']
			speaker_id = p['@id']

		Participants[speaker_id] = {}

		try:
			Participants[speaker_id]['name'] = p['@name']
		except:
			Participants[speaker_id]['name'] = 'nan'
		try:
			Participants[speaker_id]['role'] = p['@role']
		except:
			Participants[speaker_id]['role'] = 'nan'
		try:
			Participants[speaker_id]['sex'] = p['@sex']
		except:
			Participants[speaker_id]['sex'] = 'nan'
		try:
			Participants[speaker_id]['age'] = how_old(p['@age'])
		except:
			Participants[speaker_id]['age'] = 'nan'
		try:
			Participants[speaker_id]['group'] = p['@group']
		except:
			Participants[speaker_id]['group'] = 'nan'

	GroupType = 'nan'
	try:
		GroupType = chat['CHAT']['@GroupType']
	except:
		pass

	if GroupType != 'TD':
		print(GroupType)


	return ActivityType, GroupType, Lang, Corpus, Participants


### sorting incorrect index based on their value; e.g. ['1', '3', '2'] ####

def sort_idx(id_l, tok_l, stem_l, pos_l, head_l, dep_l):

	old_id_l = []

	for t in id_l:
		old_id_l.append(int(t))

	old_id_l.sort()

	or_id_l = []
	or_tok_l = []
	or_stem_l = []
	or_pos_l = []
	or_head_l = []
	or_dep_l = []


	remove_things = {}

	for idx in old_id_l:
		for z in zip(id_l, tok_l, stem_l, pos_l, head_l, dep_l):
			if int(z[0]) == idx and z[1] in ['TAGMARKER', 'PUNCTUATION']:
			
			### dealing with cases where the only thing that's being removed is the puncuation at the end of the sentence ###

				remove_id = z[0]
				remove_h = z[4]
				remove_things[remove_id] = remove_h
#	print(remove_things)
	for k, v in remove_things.items():
		if v in remove_things:
			remove_things[k] = remove_things[v]
#	print(remove_things)
	for idx in old_id_l:
		for z in zip(id_l, tok_l, stem_l, pos_l, head_l, dep_l):
	
			if int(z[0]) == idx and z[1] not in ['TAGMARKER', 'PUNCTUATION']:

				or_id_l.append(str(z[0]))
				or_tok_l.append(z[1])
				or_stem_l.append(z[2])
				or_pos_l.append(z[3])
			
				if str(z[4]) in remove_things:
	#				print(z[4])			
					or_head_l.append(remove_things[str(z[4])])
				else:
					or_head_l.append(str(z[4]))
				or_dep_l.append(z[5])

#	print('SORT')
#	print(id_l)
#	print(old_id_l)
#	print(tok_l)
#	print(head_l)
#	print(or_id_l)
#	print(or_head_l)
	return or_id_l, or_tok_l, or_stem_l, or_pos_l, or_head_l, or_dep_l


def house_keeping(id_l, tok_l, stem_l, pos_l, head_l, dep_l, u_id):

	### dealing with multiple roots; usually cased by having a discourse marker (BEG) ###
	### sometimes it's because of annotation errors; e.g. what else is in here ###

	root_list = []
	root_c = []
	root = ''

	for i in range(len(head_l)):
		if head_l[i] == '0':
			root_list.append(i)

	if len(root_list) == 1:
		root = id_l[root_list[0]]
	else:
		for i in root_list:			
			if dep_l[i] in ['ROOT', 'INCROOT']:
				root_c.append(i)

	if len(root_c) == 1:
		root = id_l[i]
	
	if root != '':
		for i in range(len(head_l)):
			if head_l[i] == "0" and id_l[i] != root:
				head_l[i] = str(root)
				dep_l[i] == 'discourse'
		
#	else:
#		if len(tok_l) != 0:
#			print(u_id + ' ' + ' '.join(w for w in tok_l) + ' NO / MULTIPLE ROOT caused by tagMarker or punctuation')


	### dealing with inconsistent indexation, syntactic heads and inclusion of punctuation in dependency analysis ####
	
	i = 1
	correct_index = [str(i)]

	while len(correct_index) < len(tok_l):
		i += 1
		correct_index.append(str(i))

	id_p = {}
	for i in range(len(id_l)):
		id_p[id_l[i]] = correct_index[i]

	head_p = {}
	for i in range(len(id_l)):
		head_p[head_l[i]] = id_l[i]

	old_head_list = head_l

	head_l = []

	only_root = ''
	for idx in range(len(correct_index)):
		if old_head_list[idx] == '0':
			only_root = correct_index[idx]

	for h in old_head_list:
		if h in id_p:
			head_l.append(id_p[h])
		else:
			if h == '0':
				head_l.append('0')
			else:
				print(u_id + ' POTENTIAL TAGMARKER/PUNCTUATION as ROOT; NEED MANUAL CHECK')
	#		if h in head_p:
	#			

	#		if int(h) > len(correct_index):
	#			print(u_id + ' POTENTIAL TAGMARKER; NEED MANUAL CHECK')
	#			head_l.append(only_root)
	#		else:
	#			head_l.append(h)

#	print('CHECK')
#	print(old_head_list)
#	print(id_l)
#	print(correct_index)
#	print(head_l)

	for i in range(len(correct_index)):
		if correct_index[i] == head_l[i]:
			print(u_id + ' HAS CYCLE; NEED MANUAL CHECK')

	#### assign omissions a new POS tag that's easily identifiable ####
	#### this is to facilitate later-on dependency calculation ####
	#### which can just be specified in FW_POS and FW_RELS in detransform.py ####

	for i in range(len(correct_index)):
		if pos_l[i].startswith('0'):
			pos_l[i] = 'OMISSION'

	return correct_index, tok_l, stem_l, pos_l, head_l, dep_l

### dealing with tokenization and dependency relations of MULTI and e.g. possesiv###

def adapt(id_l, tok_l, stem_l, pos_l, head_l, dep_l):

	for i in range(len(id_l)):

	### negation ###
	
		if tok_l[i] == 'MULTI':
			if stem_l[i] == 'not' and pos_l[i] == 'neg':
				original_tok = tok_l[i - 1].split("'")
				pre_tok = original_tok[0][ : -1]
				tok_l[i - 1] = pre_tok
				tok_l[i] = "n't"

		### in CHILDES, negation is dependent of auxiliaries or copulas; 
		### change the head of negation to the head of its original head; e.g. I don't like kale
		### or do not change it if its original head is the root

			#	pre_tok_h = head_l[i - 1]
			#	if int(pre_tok_h) != 0:
			#		head_l[i] = pre_tok_h

	### copula; let's; we'll ###
	
			elif "'" in tok_l[i - 1] and "n't" not in tok_l[i - 1]:
				original_tok = tok_l[i - 1].split("'")
				pre_tok = original_tok[0]
				tok_l[i - 1] = pre_tok
				tok_l[i] = "'" + original_tok[-1]

	### wanna; hafta ###

			elif stem_l[i] == 'to':
				original_tok = tok_l[i - 1]
				pre_tok = original_tok[ : -2]
				tok_l[i - 1] = pre_tok
				tok_l[i] = original_tok[-2 : ]


	### lemme ###

			elif pos_l[i] == 'pro':
				original_tok = tok_l[i - 1]
				pre_tok = original_tok[ : -1 * len(stem_l[i])]
				tok_l[i - 1] = pre_tok
				tok_l[i] = stem_l[i]

	### shoulda ###
			elif tok_l[i - 1] in ['shoulda', 'coulda', 'woulda', 'musta']:
				original_tok = tok_l[i - 1]
				tok_l[i - 1] = original_tok[: -1]
				tok_l[i] = 'a'

	### cases like I did it ###
		aux_words = ['do', 'did', 'will', 'would', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'can', 'could', 'dare', 'have']
		if len(id_l) == 3 and pos_l[-1] == 'pro' and head_l[-1] == '0' and stem_l[1] in aux_words and dep_l[-2] == 'AUX' and dep_l[-1] in ['ROOT', 'INCROOT']:
			head_l[0] = '2'
			head_l[1] = '0'
			head_l[2] = '2'

			pos_l[1] = 'v'

			dep_l[1] = 'ROOT'
			dep_l[-1] = 'OBJ'

	### cases like no I don't ###
		if pos_l == ['co', 'pro', 'mod', 'neg']:
			head_l = ['3', '3', '0', '3']
			dep_l = ['COM', 'SUBJ', 'ROOT', 'NEG']


	### possesive; not tokenized in CHILDES ###

	#	if tok_l[i] != "'s" and "'s" in tok_l[i] and id_l[i] != id_l[-1]:
	#		next_tok = tok_l[i + 1]
	#		if next_tok != 'MULTI':
	#			original_tok = tok_l[i].split("'")
	#			pre_tok = original_tok[0]

	#			for r in range(i + 1, len(id_l)):
	#				id_l[r] = str(int(id_l[r]) + 1)

	#			for r in range(len(id_l)):
	#				if int(head_l[r]) >= i + 1:
	#					head_l[r] = str(int(head_l[r]) + 1)

	#			id_l.insert(i + 1, str(int(id_l[i]) + 1))
	#			tok_l.insert(i + 1, "'s")
	#			stem_l.insert(i + 1, "'s")
	#			pos_l.insert(i + 1, "part")
	#			head_l.insert(i + 1, id_l[i])
	#			dep_l.insert(i + 1, "case")

	#	if tok_l[i] != "'s" and "'s" in tok_l[i] and id_l[i] == id_l[-1]:
	#		original_tok = tok_l[i].split("'")
	#		pre_tok = original_tok[0]

	#		id_l.append(str(int(id_l[i]) + 1))
	#		tok_l.append("'s")
	#		stem_l.append("'s")
	#		pos_l.append("part")
	#		head_l.append(id_l[i])
	#		dep_l.append("case")

	### converting dependencies of e.g. what's that? that's something ###
	### treating adposition as the head actuall yields shorter dependencies ###
	### therefore even before conversion, if DLM, 
	### then after conversion only leads to stronger extent of DLM###

	#	if stem_l[i] == 'be' and pos_l[i] == 'cop'

	### adpositional phrase annotation ###

	return id_l, tok_l, stem_l, pos_l, head_l, dep_l


def get_feature(utterance, GroupType, Corpus, Participants):

	features = []
	child = ''
	child_c = 0
	try:
		child = Participants['CHI']
		child_c += 1
	except:
		for k, v in Participants.items():
			if v['role'] in ['Target_Child', 'Child']:
				child = Participants[k]
				child_c += 1

	speaker_id = utterance['@who']
	utterance_id = utterance['@uID'][1:]


	id_list = []
	pos_list = []
	tok_list = []
	stem_list = []
	head_list = []
	dependency_list = []

	w_tok_replacement = []

	#### dealing with replacement ####

	for w in utterance['w']:

		if 'replacement' in w:

			w_tok_replacement.append(w['#text'])

			w = w['replacement']['w']

			if not isinstance(w, list):
				w = [w]

			for i in range(len(w)):
				small_w = w[i]

				if 'mor' in small_w:  ### not including unintelligible tokens

					w_id = []
					w_pos = []
					w_tok = []
					w_stem = []
					w_head = []
					w_dependency = []
					say = ''
					text = ''

					try:
						say = small_w['mor']
						text = small_w['#text']
					except:
						say = utterance['w']['mor']
						text = utterance['w']['#text']

					if 'mw' in say:

						try:
							w_pos.append(say['mw']['pos']['c'])
						except:
							w_pos.append('NONE')

						try:
							w_stem.append(say['mw']['stem'])
							w_tok.append(text)
						except:
							w_stem.append('NONE')
							w_tok.append(text)

						try:
							gra = say['gra']
							w_id.append(gra['@index'])
							w_head.append(gra['@head'])
							w_dependency.append(gra['@relation'])
						except:
							w_id.append('NONE')
							w_head.append('NONE')
							w_dependency.append('NONE')

					if 'mor-post' in say:

						try:
							w_pos.append(say['mor-post']['mw']['pos']['c'])
						except:
							w_pos.append('NONE')

						try:
							w_stem.append(say['mor-post']['mw']['stem'])
							w_tok.append('MULTI')
						except:
							w_stem.append('NONE')
							w_tok.append('MULTI')

						try:
							gra = say['mor-post']['gra']
							w_id.append(gra['@index'])
							w_head.append(gra['@head'])
							w_dependency.append(gra['@relation'])
						except:
							w_id.append('NONE')
							w_head.append('NONE')
							w_dependency.append('NONE')

					if 'mwc' in say:

						try:
							w_pos.append(say['mwc']['pos']['c'])
						except:
							w_pos.append('NONE')

						try:
							w_stem.append(text)
							w_tok.append(text)
						except:
							w_stem.append('NONE')
							w_tok.append(text)

						try:
							gra = say['gra']
							w_id.append(gra['@index'])
							w_head.append(gra['@head'])
							w_dependency.append(gra['@relation'])
						except:
							w_id.append('NONE')
							w_head.append('NONE')
							w_dependency.append('NONE')

					for t in w_id:
						id_list.append(t)
					for t in w_pos:
						pos_list.append(t)
					for t in w_tok:
						tok_list.append(t)
					for t in w_stem:
						stem_list.append(t)
					for t in w_head:
						head_list.append(t)
					for t in w_dependency:
						dependency_list.append(t)

	### words from standard annotation ###

		if 'mor' in w:  ### not including unintelligible tokens

			w_id = []
			w_pos = []
			w_tok = []
			w_stem = []
			w_head = []
			w_dependency = []
			say = ''
			text = ''

			try:
				say = w['mor']
				text = w['#text']
			except:
				say = utterance['w']['mor']
				text = utterance['w']['#text']

			if 'mw' in say:

				try:
					w_pos.append(say['mw']['pos']['c'])
				except:
					w_pos.append('NONE')

				try:
					w_stem.append(say['mw']['stem'])
					w_tok.append(text)
				except:
					w_stem.append('NONE')
					w_tok.append(text)

				try:
					gra = say['gra']
					w_id.append(gra['@index'])
					w_head.append(gra['@head'])
					w_dependency.append(gra['@relation'])
				except:
					w_id.append('NONE')
					w_head.append('NONE')
					w_dependency.append('NONE')

			if 'mor-post' in say:
				
				all_mor_post = []
				if isinstance(say['mor-post'], list):
					for m in say['mor-post']:
						all_mor_post.append(m)
				else:
					all_mor_post.append(say['mor-post'])

				for m in all_mor_post:
					try:
						w_pos.append(m['mw']['pos']['c'])

					except:
						w_pos.append('NONE')

					try:
						w_stem.append(m['mw']['stem'])
						w_tok.append('MULTI')
					except:
						w_stem.append('NONE')
						w_tok.append('MULTI')

					try:
						gra = m['gra']
						w_id.append(gra['@index'])
						w_head.append(gra['@head'])
						w_dependency.append(gra['@relation'])
					except:
						w_id.append('NONE')
						w_head.append('NONE')
						w_dependency.append('NONE')

			if 'mwc' in say:

				try:
					w_pos.append(say['mwc']['pos']['c'])
				except:
					w_pos.append('NONE')

				try:
					w_stem.append(text)
					w_tok.append(text)
				except:
					w_stem.append('NONE')
					w_tok.append(text)

				try:
					gra = say['gra']
					w_id.append(gra['@index'])
					w_head.append(gra['@head'])
					w_dependency.append(gra['@relation'])
				except:
					w_id.append('NONE')
					w_head.append('NONE')
					w_dependency.append('NONE')

			for t in w_id:
				id_list.append(t)
			for t in w_pos:
				pos_list.append(t)
			for t in w_tok:
				tok_list.append(t)
			for t in w_stem:
				stem_list.append(t)
			for t in w_head:
				head_list.append(t)
			for t in w_dependency:
				dependency_list.append(t)

	#### tagMarker #####

	try:
		for w in utterance['tagMarker']:
			
			if 'mor' in w:  ### not including unintelligible tokens
			#	print(w)
				w_id = []
				w_pos = []
				w_tok = []
				w_stem = []
				w_head = []
				w_dependency = []
				say = ''
				text = 'TAGMARKER'

				try:
					say = w['mor']

				except:
					say = utterance['tagMarker']['mor']


				if 'mw' in say:

					try:
						w_pos.append(say['mw']['pos']['c'])
					except:
						w_pos.append('NONE')

					try:
						w_stem.append(say['mw']['stem'])
						w_tok.append(text)
					except:
						w_stem.append('NONE')
						w_tok.append(text)

					try:
						gra = say['gra']
						w_id.append(gra['@index'])
						w_head.append(gra['@head'])
						w_dependency.append(gra['@relation'])
					except:
						w_id.append('NONE')
						w_head.append('NONE')
						w_dependency.append('NONE')

				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

	except:

		try:
			w = utterance['tagMarker']

			if 'mor' in w:  ### not including unintelligible tokens
				
				w_id = []
				w_pos = []
				w_tok = []
				w_stem = []
				w_head = []
				w_dependency = []
				say = ''
				text = 'TAGMARKER'

				try:
					say = w['mor']

				except:
					say = utterance['w']['mor']


				if 'mw' in say:

					try:
						w_pos.append(say['mw']['pos']['c'])
					except:
						w_pos.append('NONE')

					try:
						w_stem.append(say['mw']['stem'])
						w_tok.append(text)
					except:
						w_stem.append('NONE')
						w_tok.append(text)

					try:
						gra = say['gra']
						w_id.append(gra['@index'])
						w_head.append(gra['@head'])
						w_dependency.append(gra['@relation'])
					except:
						w_id.append('NONE')
						w_head.append('NONE')
						w_dependency.append('NONE')

				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

		except:
			pass

	#### punctuation #####

	try:

		for w in utterance['t']:

			if 'mor' in w:  ### not including unintelligible tokens

				w_id = [w['mor']['gra']['@index']]
				w_pos = ['_']
				w_tok = ['PUNCTUATION']
				w_stem = ['_']
				w_head = [w['mor']['gra']['@head']]
				w_dependency = [w['mor']['gra']['@relation']]


				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)


	except:

		try:
			w = utterance['t']

			if 'mor' in w:  ### not including unintelligible tokens

				w_id = [w['mor']['gra']['@index']]
				w_pos = ['_']
				w_tok = ['PUNCTUATION']
				w_stem = ['_']
				w_head = [w['mor']['gra']['@head']]
				w_dependency = [w['mor']['gra']['@relation']]


				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

		except:
			pass

	if len(id_list) >= 1 and tok_list.count('TAGMARKER') + tok_list.count('PUNCTUATION') != len(tok_list):
	#	print(tok_list)
	#	print(id_list)
	#	print(head_list)
		ordered_id_list, ordered_tok_list, ordered_stem_list, ordered_pos_list, ordered_head_list, ordered_dependency_list = sort_idx(id_list, tok_list, stem_list, pos_list, head_list, dependency_list)
	#	print(ordered_tok_list)
	#	print(ordered_id_list)
	#	print('House keeping')
		correct_index, temp_tok_list, temp_stem_list, temp_pos_list, temp_head_list, temp_dependency_list = house_keeping(ordered_id_list, ordered_tok_list, ordered_stem_list, ordered_pos_list, ordered_head_list, ordered_dependency_list, utterance_id)
	#	print(temp_tok_list)
	
	### generating output ###
		
		old_utterance = []

		for t in temp_tok_list:
			old_utterance.append(t)

		if len(w_tok_replacement) != 0:
			old_utterance.append('REPLACEMENT')
			for r in w_tok_replacement:
				old_utterance.append(r)
		
		old_utterance = ' '.join(w for w in old_utterance if w not in ['NONE', 'MULTI', 'TAGMARKER', 'PUNCTUATION'])

		new_id_list, new_tok_list, new_stem_list, new_pos_list, new_head_list, new_dependency_list = adapt(correct_index, temp_tok_list, temp_stem_list, temp_pos_list, temp_head_list, temp_dependency_list)


		if len(set([len(new_id_list), len(new_pos_list), len(new_tok_list), len(new_stem_list), len(new_head_list), len(new_dependency_list)])) == 1:

			features.append('#' + str(utterance_id) + '\t' + old_utterance) #' '.join(w for w in tok_list if w not in ['NONE', 'MULTI']))
			for i in range(len(new_id_list)):
				if child_c == 1:
					features.append([new_id_list[i], new_tok_list[i], new_stem_list[i], new_pos_list[i], '_', '_', new_head_list[i], new_dependency_list[i], str(Participants[speaker_id]['name']) + ' ' + str(speaker_id) + ' ' + str(Participants[speaker_id]['role']), str(child['name']) + ' ' + str(child['age']) + ' ' + str(child['sex']) + ' ' + str(GroupType) + ' ' + str(Corpus)])
				else:
					features.append([new_id_list[i], new_tok_list[i], new_stem_list[i], new_pos_list[i], '_', '_', new_head_list[i], new_dependency_list[i], str(Participants[speaker_id]['name']) + ' ' + str(speaker_id) + ' ' + str(Participants[speaker_id]['role']), 'Multiple' + ' ' + 'Multiple' + ' ' + 'Multiple' + ' ' + str(GroupType) + ' ' + str(Corpus)])

		else:
			print(tok_list)

	return features


def special(utterance, GroupType, Corpus, Participants):

	features = []
	child = ''
	child_c = 0
	try:
		child = Participants['CHI']
		child_c += 1
	except:
		for k, v in Participants.items():
			if v['role'] in ['Target_Child', 'Child']:
				child = Participants[k]
				child_c += 1

	speaker_id = utterance['@who']
	utterance_id = utterance['@uID'][1:]

	id_list = []
	pos_list = []
	tok_list = []
	stem_list = []
	head_list = []
	dependency_list = []

	w = ''
	
	try:
		w = utterance['g']['w']
	except:
		w = utterance['w']

	w_tok_replacement = []

	if 'replacement' in w:

		w_tok_replacement.append(w['#text'])

		w = w['replacement']['w']

		if not isinstance(w, list):
			w = [w]

		for i in range(len(w)):
			small_w = w[i]

			if 'mor' in small_w:  ### not including unintelligible tokens

				w_id = []
				w_pos = []
				w_tok = []
				w_stem = []
				w_head = []
				w_dependency = []
				say = ''
				text = ''

				try:
					say = small_w['mor']
					text = small_w['#text']
				except:
					say = utterance['w']['mor']
					text = utterance['w']['#text']

				if 'mw' in say:

					try:
						w_pos.append(say['mw']['pos']['c'])
					except:
						w_pos.append('NONE')

					try:
						w_stem.append(say['mw']['stem'])
						w_tok.append(text)
					except:
						w_stem.append('NONE')
						w_tok.append(text)

					try:
						gra = say['gra']
						w_id.append(gra['@index'])
						w_head.append(gra['@head'])
						w_dependency.append(gra['@relation'])
					except:
						w_id.append('NONE')
						w_head.append('NONE')
						w_dependency.append('NONE')

				if 'mor-post' in say:
					all_mor_post = []
					if isinstance(say['mor-post'], list):
						for m in say['mor-post']:
							all_mor_post.append(say['mor-post'])
					else:
						all_mor_post.append(m)

					for m in all_mor_post:
						try:
							w_pos.append(m['mw']['pos']['c'])

						except:
							w_pos.append('NONE')

						try:
							w_stem.append(m['mw']['stem'])
							w_tok.append('MULTI')
						except:
							w_stem.append('NONE')
							w_tok.append('MULTI')

						try:
							gra = m['gra']
							w_id.append(gra['@index'])
							w_head.append(gra['@head'])
							w_dependency.append(gra['@relation'])
						except:
							w_id.append('NONE')
							w_head.append('NONE')
							w_dependency.append('NONE')

				if 'mwc' in say:

					try:
						w_pos.append(say['mwc']['pos']['c'])
					except:
						w_pos.append('NONE')

					try:
						w_stem.append(text)
						w_tok.append(text)
					except:
						w_stem.append('NONE')
						w_tok.append(text)

					try:
						gra = say['gra']
						w_id.append(gra['@index'])
						w_head.append(gra['@head'])
						w_dependency.append(gra['@relation'])
					except:
						w_id.append('NONE')
						w_head.append('NONE')
						w_dependency.append('NONE')

				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

	if 'mor' in w:  ### not including unintelligible tokens

		w_id = []
		w_pos = []
		w_tok = []
		w_stem = []
		w_head = []
		w_dependency = []
		say = ''
		text = ''

		say = w['mor']
		text = w['#text']

		if 'mw' in say:

			try:
				w_pos.append(say['mw']['pos']['c'])
			except:
				w_pos.append('NONE')

			try:
				w_stem.append(say['mw']['stem'])
				w_tok.append(text)
			except:
				w_stem.append('NONE')
				w_tok.append(text)

			try:
				gra = say['gra']
				w_id.append(gra['@index'])
				w_head.append(gra['@head'])
				w_dependency.append(gra['@relation'])
			except:
				w_id.append('NONE')
				w_head.append('NONE')
				w_dependency.append('NONE')

		if 'mor-post' in say:

			try:
				w_pos.append(say['mor-post']['mw']['pos']['c'])
			except:
				w_pos.append('NONE')

			try:
				w_stem.append(say['mor-post']['mw']['stem'])
				w_tok.append('MULTI')
			except:
				w_stem.append('NONE')
				w_tok.append('MULTI')

			try:
				gra = say['mor-post']['gra']
				w_id.append(gra['@index'])
				w_head.append(gra['@head'])
				w_dependency.append(gra['@relation'])
			except:
				w_id.append('NONE')
				w_head.append('NONE')
				w_dependency.append('NONE')

		if 'mwc' in say:

			try:
				w_pos.append(say['mwc']['pos']['c'])
			except:
				w_pos.append('NONE')

			try:
				w_stem.append(text)
				w_tok.append(text)
			except:
				w_stem.append('NONE')
				w_tok.append(text)

			try:
				gra = say['gra']
				w_id.append(gra['@index'])
				w_head.append(gra['@head'])
				w_dependency.append(gra['@relation'])
			except:
				w_id.append('NONE')
				w_head.append('NONE')
				w_dependency.append('NONE')

		
		### dealing with replacement ###

#		if len(w_tok_replacement) == len(w_tok):
#			w_tok = w_tok_replacement

#		if len(w_tok_replacement) != 0 and len(w_tok_replacement) != len(w_tok):
#			print(w_tok_replacement)
#			print(w_tok)
#			print(str(utterance_id) + ' CHECK REPLACEMENT')

		for t in w_id:
			id_list.append(t)
		for t in w_pos:
			pos_list.append(t)
		for t in w_tok:
			tok_list.append(t)
		for t in w_stem:
			stem_list.append(t)
		for t in w_head:
			head_list.append(t)
		for t in w_dependency:
			dependency_list.append(t)


	#### tagMarker #####

	try:
		for w in utterance['tagMarker']:
			
			if 'mor' in w:  ### not including unintelligible tokens
				w_id = []
				w_pos = []
				w_tok = []
				w_stem = []
				w_head = []
				w_dependency = []
				say = ''
				text = 'TAGMARKER'

				try:
					say = w['mor']

				except:
					say = utterance['w']['mor']


				if 'mw' in say:

					try:
						w_pos.append(say['mw']['pos']['c'])
					except:
						w_pos.append('NONE')

					try:
						w_stem.append(say['mw']['stem'])
						w_tok.append(text)
					except:
						w_stem.append('NONE')
						w_tok.append(text)

					try:
						gra = say['gra']
						w_id.append(gra['@index'])
						w_head.append(gra['@head'])
						w_dependency.append(gra['@relation'])
					except:
						w_id.append('NONE')
						w_head.append('NONE')
						w_dependency.append('NONE')

				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

	except:

		try:
			w = utterance['tagMarker']

			if 'mor' in w:  ### not including unintelligible tokens
				
				w_id = []
				w_pos = []
				w_tok = []
				w_stem = []
				w_head = []
				w_dependency = []
				say = ''
				text = 'TAGMARKER'

				try:
					say = w['mor']

				except:
					say = utterance['tagMarker']['mor']


				if 'mw' in say:

					try:
						w_pos.append(say['mw']['pos']['c'])
					except:
						w_pos.append('NONE')

					try:
						w_stem.append(say['mw']['stem'])
						w_tok.append(text)
					except:
						w_stem.append('NONE')
						w_tok.append(text)

					try:
						gra = say['gra']
						w_id.append(gra['@index'])
						w_head.append(gra['@head'])
						w_dependency.append(gra['@relation'])
					except:
						w_id.append('NONE')
						w_head.append('NONE')
						w_dependency.append('NONE')

				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

		except:
			pass

	#### punctuation #####

	try:

		for w in utterance['t']:

			if 'mor' in w:  ### not including unintelligible tokens

				w_id = [w['mor']['gra']['@index']]
				w_pos = ['_']
				w_tok = ['PUNCTUATION']
				w_stem = ['_']
				w_head = [w['mor']['gra']['@head']]
				w_dependency = [w['mor']['gra']['@relation']]


				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

	except:

		try:
			w = utterance['t']

			if 'mor' in w:  ### not including unintelligible tokens

				w_id = [w['mor']['gra']['@index']]
				w_pos = ['_']
				w_tok = ['PUNCTUATION']
				w_stem = ['_']
				w_head = [w['mor']['gra']['@head']]
				w_dependency = [w['mor']['gra']['@relation']]


				for t in w_id:
					id_list.append(t)
				for t in w_pos:
					pos_list.append(t)
				for t in w_tok:
					tok_list.append(t)
				for t in w_stem:
					stem_list.append(t)
				for t in w_head:
					head_list.append(t)
				for t in w_dependency:
					dependency_list.append(t)

		except:
			pass


	if len(id_list) >= 1 and tok_list.count('TAGMARKER') + tok_list.count('PUNCTUATION') != len(tok_list):


		ordered_id_list, ordered_tok_list, ordered_stem_list, ordered_pos_list, ordered_head_list, ordered_dependency_list = sort_idx(id_list, tok_list, stem_list, pos_list, head_list, dependency_list)

		correct_index, temp_tok_list, temp_stem_list, temp_pos_list, temp_head_list, temp_dependency_list = house_keeping(ordered_id_list, ordered_tok_list, ordered_stem_list, ordered_pos_list, ordered_head_list, ordered_dependency_list, utterance_id)
	
	### generating output ###

		old_utterance = []

		for t in temp_tok_list:
			old_utterance.append(t)

		if len(w_tok_replacement) != 0:
			old_utterance.append('REPLACEMENT')
			for r in w_tok_replacement:
				old_utterance.append(r)

		old_utterance = ' '.join(w for w in old_utterance if w not in ['NONE', 'MULTI', 'TAGMARKER', 'PUNCTUATION'])

		new_id_list, new_tok_list, new_stem_list, new_pos_list, new_head_list, new_dependency_list = adapt(correct_index, temp_tok_list, temp_stem_list, temp_pos_list, temp_head_list, temp_dependency_list)


		if len(set([len(new_id_list), len(new_pos_list), len(new_tok_list), len(new_stem_list), len(new_head_list), len(new_dependency_list)])) == 1:
			features.append('#' + str(utterance_id) + '\t' + old_utterance) #' '.join(w for w in tok_list if w not in ['NONE', 'MULTI']))
			for i in range(len(new_id_list)):
				if child_c == 1:
					features.append([new_id_list[i], new_tok_list[i], new_stem_list[i], new_pos_list[i], '_', '_', new_head_list[i], new_dependency_list[i], str(Participants[speaker_id]['name']) + ' ' + str(speaker_id) + ' ' + str(Participants[speaker_id]['role']), str(child['name']) + ' ' + str(child['age']) + ' ' + str(child['sex']) + ' ' + str(GroupType) + ' ' + str(Corpus)])
				else:
					features.append([new_id_list[i], new_tok_list[i], new_stem_list[i], new_pos_list[i], '_', '_', new_head_list[i], new_dependency_list[i], str(Participants[speaker_id]['name']) + ' ' + str(speaker_id) + ' ' + str(Participants[speaker_id]['role']), 'Multiple' + ' ' + 'Multiple' + ' ' + 'Multiple' + ' ' + str(GroupType) + ' ' + str(Corpus)])

		else:
			print(tok_list)

	return features


def Expelliarmus(file, directory, output, section):
	print(file)
	original = io.open(file).read()
	v1 = original.replace('<g>','')
	v2 = v1.replace('</g>','')
	v3 = v2.replace('<pg>','')   ### dealing with phonBank specific annotations ###
	v4 = v3.replace('</pg>','')
	chat = xmltodict.parse(v4)

	ActivityType, GroupType, Lang, Corpus, Participants = basic_info(chat)

#	chat = xmltodict.parse(io.open(file).read())
#	print(file)


	all_utterances = []

	#	outfile = io.open(output + '/' + '_'.join(d for d in directory.split('English-UK/')[1].split('/')[ : -1]) + '_' + file[ : -4] + '.conllu', 'w', encoding = 'utf-8')
	#	outfile = io.open(output + 'test.conllu', 'w', encoding = 'utf-8')
		
	try:
		utterance = get_feature(chat['CHAT']['u'], GroupType, Corpus, Participants)

		if len(utterance) > 0:
			print(file + 'ONE UTTERANCE')
			all_utterances.append(utterance)
			#	outfile.write(utterance[0] + '\n')
				
			#	for u in utterance[1 : ]:
			#		outfile.write('\t'.join(str(w) for w in u) + '\n')
				
			#	outfile.write('\n')

	except:
		
		try:
			utterance = special(chat['CHAT']['u'], GroupType, Corpus, Participants)

			if len(utterance) > 0:
				print(file + 'SPECIAL')
				all_utterances.append(utterance)

		except:
				
			try:
				for u in chat['CHAT']['u']:
					if 'w' in u:

						#	print(a['#text'] for a in u['w'])
						#	if 'replacement' in u['w']:
						#		print(a['replacement'] for a in u['w'])  #['replacement'])
						#		print(a for a in u['w']['replacement']['w'])
						utterance = []

						try:
							utterance = get_feature(u, GroupType, Corpus, Participants)		
						except:
							utterance = special(u, GroupType, Corpus, Participants)				

					#### including single utterances for now ####

						if len(utterance) > 0:

							all_utterances.append(utterance)
			#					outfile.write(utterance[0] + '\n')
				
			#					for u in utterance[1 : ]:
			#						outfile.write('\t'.join(str(w) for w in u) + '\n')
			#	
			#					outfile.write('\n')

			except:
				try:
					for u in chat['CHAT']['u']:
						if 'w' in u:
							if 'untranscribed' in u['w']:
								continue
				except:

					print('')
					print(file + 'SOMETHING WRONG WIHT THIS ONE')
					print('')

	#	child_out = io.open(output + '/' + '_'.join(d for d in directory.split(section + '/')[1].split('/')[ : -1]) + '_' + file[ : -4] + '_child.conllu', 'w', encoding = 'utf-8')
	#	parent_out = io.open(output + '/' + '_'.join(d for d in directory.split(section + '/')[1].split('/')[ : -1]) + '_' + file[ : -4] + '_parent.conllu', 'w', encoding = 'utf-8')

	if len(all_utterances) != 0:
		outfile = io.open(output + '/' + '_'.join(d for d in directory.split(section + '/')[1].split('/')[ : -1]) + '_' + file[ : -4] + '.conllu', 'w', encoding = 'utf-8')

		for utterance in all_utterances:

			if len(utterance) >= 2: # avoid unintelligible tokens

				speaker = utterance[1][-2].split()[-1]
				
				if speaker in ['Mother', 'Father', 'Target_Child', 'Child']:

						check(utterance)

					outfile.write(utterance[0] + '\n')

				### e.g. well it's not time for lunch yet ###

					for u in utterance[1 : ]:

						outfile.write('\t'.join(str(w) for w in u) + '\n')

					outfile.write('\n')

		outfile.close()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to corpus')
	parser.add_argument('--output', type = str, help = 'output CoNLL formatted file')
	parser.add_argument('--section', type = str, help = 'e.g. English-NA / English-UK')

	args = parser.parse_args()

	path = args.input
	os.chdir(path)

	for file in os.listdir(path):		
		if file.endswith('.xml'):
			Expelliarmus(file, path, args.output, args.section)
