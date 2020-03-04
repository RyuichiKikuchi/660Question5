#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:41:37 2020

@author: ruizhihao
"""
import requests
import re
from bs4 import BeautifulSoup
import spacy
from spacy.symbols import VERB
from collections import Counter
# Get book content.
url = 'https://www.gutenberg.org/files/1342/1342-h/1342-h.htm'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
content = soup.find_all('p')
content = str(content)
book = re.findall('      (.+)\n', content)
book_parse = str(book).replace("', '", " ")
book_parse = str(book_parse).replace("\", \"", " ")
book_parse = str(book_parse).replace("\', \"", " ")
book_parse = str(book_parse).replace("\", '", " ")
book_parse = str(book_parse).replace("['", "")
book_parse = str(book_parse).replace("']", "")
book_parse = str(book_parse).replace("\\r", "")
book_parse = str(book_parse).replace("<i>", "")
book_parse = str(book_parse).replace("</i>", "")
nlp = spacy.load("en_core_web_lg")
text = str(book_parse)
doc = nlp(text)

#Question1. How many tokens are in the document?
num_tokens = 0
for token in doc:
    num_tokens = num_tokens + 1
    #print({token:token.pos_})
print("There're " + str(num_tokens) + " tokens in Pride And Prejudice.")

#2. How many verbs are in the document?
num_verbs = 0
for token in doc:
    if token.pos == VERB:
        num_verbs = num_verbs + 1
print("There're " + str(num_verbs) + " verbs in Pride And Prejudice.")

#3. What is the most frequent named entity?
named_ent = []
for ent in doc.ents:
    named_ent.append(ent.text)
    #print(ent.text, ent.start_char, ent.end_char, ent.label_)
ent_freq = Counter(named_ent)
Most_freq_ent = ent_freq.most_common(1)
print("The most frequent named entity is " + str(Most_freq_ent) + '.')

#4. How many setences are in the document?
num_sent = 0
for sent in doc.sents:
     num_sent = num_sent + 1
print("There're " + str(num_sent) + " sentences in Pride And Prejudice.")

#5. Of all the sentences in the text that are at least 10 words in length, 
#   which two are most similar (but not identical)?
sent_list = []
for sent in doc.sents:
    if str(sent).count(' ') >= 9:
        sent_list.append(sent)
print(sent_list)

similarity_max = float(0.0)
sent1_max = None
sent2_max = None
for sent1 in sent_list:
    for sent2 in sent_list:
        if sent1 != sent2:
            if similarity_max < sent1.similarity(sent2):
                similarity_max = sent1.similarity(sent2)
                sent1_max = sent1
                sent2_max = sent2
print("The highest similarity is " + str(similarity_max) + '.','\n',"Sent1: " + str(sent1_max),'\n',"Sent2: " + str(sent2_max))

#6. What is the vector representation of the first word in the 15th sentence in the document?
sent_15 = sent_list[14]
first_token_sent15 = sent_15[0]
print("The vector representation of the first word in the 15th sentence is " + str(first_token_sent15.vector_norm) + ".")

"""
Result:
Q1: There're 143851 tokens in Pride And Prejudice.
Q2: There're 17765 verbs in Pride And Prejudice.
Q3: The most frequent named entity is [('Elizabeth', 625)].
Q4: There're 6174 sentences in Pride And Prejudice.
Q5: The highest similarity is 0.9883196. 
Sent1: “I am by no means of the opinion, I assure you,” said he,
       “that a ball of this kind, given by a young man of character, 
       to respectable people, can have any evil tendency; 
       and I am so far from objecting to dancing myself, 
       that I shall hope to be honoured with the hands of 
       all my fair cousins in the course of the evening; 
       and I take this opportunity of soliciting yours, 
       Miss Elizabeth, for the two first dances especially, 
       a preference which I trust my cousin Jane will attribute
       to the right cause, and not to any disrespect for her.” 
       
Sent2: The idea of Mr. Collins, with all his solemn composure, 
       being run away with by his feelings, made Elizabeth so near 
       laughing, that she could not use the short pause he allowed 
       in any attempt to stop him further, and he continued:
       “My reasons for marrying are, first, that I think it a right 
       thing for every clergyman in easy circumstances (like myself) 
       to set the example of matrimony in his parish; secondly, that
       I am convinced that it will add very greatly to my happiness; 
       and thirdly—which perhaps I ought to have mentioned earlier, 
       that it is the particular advice and recommendation of the very
       noble lady whom I have the honour of calling patroness.
       
Question6: The vector representation of the first word in the 15th sentence
           is 4.718869.
"""
