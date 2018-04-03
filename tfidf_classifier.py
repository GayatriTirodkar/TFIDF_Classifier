from nltk import pos_tag
from nltk import PorterStemmer
import os
import re
import json

def tfidf_classifier(fname):
	with open(fname+".txt","r") as file:
		paragraph = file.read()

	#clean the extracted content
	paragraph = " ".join(re.findall(r"\b[a-z0-9]+\b",paragraph,flags=re.I)).lower()



	#get the part of speech for every word in the content
	pos_tag_words = pos_tag(paragraph.split())
	porter_stemmer_obj = PorterStemmer()
	stem = porter_stemmer_obj.stem
	pos_tag_words = [(str(stem(tag[0])), tag[-1]) if tag[-1].startswith("VB") else tag for tag in pos_tag_words]
	paragraph = " ".join([w[0] for w in pos_tag_words])

	#extract all the nouns, adjectives, adverbs and verbs from the paragraph
	temp_noun_adj_list = []
	temp_verb_adv_list = []
	all_words = []
	all_words_count_dict = {}
	for pos_words in pos_tag_words:
		if (pos_words[-1].startswith("NN") or pos_words[-1].startswith("JJ")):
			temp_noun_adj_list.append(pos_words[0])
			if len(temp_verb_adv_list) > 1:
				adv_verb_str = " ".join(temp_verb_adv_list)
				if adv_verb_str not in all_words_count_dict: 
					all_words_count_dict[adv_verb_str] = paragraph.count(adv_verb_str)
				temp_verb_adv_list = []
			elif temp_verb_adv_list:
				if temp_verb_adv_list[0] not in all_words_count_dict:
					all_words_count_dict[temp_verb_adv_list[0]] = paragraph.count(temp_verb_adv_list[0])
				temp_verb_adv_list = []
		elif pos_words[-1].startswith("VB"):
			temp_verb_adv_list.append(pos_words[0])
			if len(temp_noun_adj_list) > 1:
				adj_noun_str = " ".join(temp_noun_adj_list)
				if adj_noun_str not in all_words_count_dict:
					all_words_count_dict[adj_noun_str] = paragraph.count(adj_noun_str)
				temp_noun_adj_list = []
			elif temp_noun_adj_list:
				if temp_noun_adj_list[0] not in all_words_count_dict:
					all_words_count_dict[temp_noun_adj_list[0]] = paragraph.count(temp_noun_adj_list[0])
				temp_noun_adj_list = []
		elif  pos_words[-1].startswith("RB"):
			temp_verb_adv_list.append(pos_words[0])
			if len(temp_noun_adj_list) > 1:
				adj_noun_str = " ".join(temp_noun_adj_list)
				if adj_noun_str not in all_words_count_dict:
					all_words_count_dict[adj_noun_str] = paragraph.count(adj_noun_str)
				temp_noun_adj_list = []
			elif temp_noun_adj_list:
				if temp_noun_adj_list[0] not in all_words_count_dict:
					all_words_count_dict[temp_noun_adj_list[0]] = paragraph.count(temp_noun_adj_list[0])
				temp_noun_adj_list = []
		else:
			if temp_noun_adj_list:
				adj_noun_str = " ".join(temp_noun_adj_list)
				if adj_noun_str not in all_words_count_dict:
					all_words_count_dict[adj_noun_str] = paragraph.count(adj_noun_str)
				temp_noun_adj_list = []
			if temp_verb_adv_list:
				adv_str = " ".join(temp_verb_adv_list)
				if adv_str not in all_words_count_dict:
					all_words_count_dict[adv_str] = paragraph.count(adv_str)
				temp_verb_adv_list = []

	if len(temp_noun_adj_list) > 0:
		adj_noun_str = " ".join(temp_noun_adj_list)
		if adj_noun_str not in all_words_count_dict:
			all_words_count_dict[adj_noun_str] = paragraph.count(adj_noun_str)
	if len(temp_verb_adv_list) > 0:
		adv_str = " ".join(temp_verb_adv_list)
		if adv_str not in all_words_count_dict:
			all_words_count_dict[adv_str] = paragraph.count(adv_str)

	with open(fname+".json","w") as file:
		json.dump(all_words_count_dict, file)

if __name__ == "__main__":

	map(lambda fname: tfidf_classifier(fname.split(".")[0]), filter(lambda x: x.endswith("txt"),os.listdir("./")))