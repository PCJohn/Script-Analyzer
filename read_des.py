from __future__ import division
import nltk
from nltk import sent_tokenize,pos_tag,word_tokenize
import os
from tfidf import TFIDF_Model,Tokenizer
from nltk.corpus import stopwords
import numpy as np
import script_manager as sm
import script_encoder as se
from graph import Graph

class Reader():
    def __init__(self,path,scene_count,word_dim,max_chunk_len):
        self.tf = TFIDF_Model(path)
        self.SCENE_COUNT = scene_count
        self.WORD_DIM = word_dim
        self.MAX_CHUNK_LEN = max_chunk_len
        self.encoder = se.ScriptEncoder(self.WORD_DIM,self.MAX_CHUNK_LEN)

    #Returns a list of 3-tuples: (scene text, list of chars in scene,score)
    def get_char_scene(self,script,char_list,keys):
        scenes = []
        N = len(script)
        in_dialogue = False
        has_desc_tag = False
        i = 0
        scene_text = []
        scene_char = set
        while (i < N):
            line = script[i].strip()
            if line == sm.DESC_TAG:
                if in_dialogue:
                    #Find characters in the scene description
                    score = 0
                    key_count = 0
                    for line in scene_text:
                        line = line.strip()
                        for w in word_tokenize(line):
                            if w in keys:
                                score = score+keys[w]
                                key_count = key_count+1
                            w = w.lower()
                            if w in char_list:
                                scene_char = scene_char.union(set([w]))
                    if key_count > 0:
                        score = score/key_count
                    scenes.append((scene_text,list(scene_char),score))
                    #Clear text, char list buffers
                    scene_text = []
                    scene_char.clear()
                    in_dialogue = False
                    scene_text.append(line)
            elif line.isupper():
                scene_char = scene_char.union(set([line.strip().lower()]))
                in_dialogue = True
                scene_text.append(line)
            else:
                scene_text.append(line)
            i = i+1
        self.merge_scenes(scenes)
        return scenes

    #Refine the snippets -- combine consecutive snippets if they have the same characters
    def merge_scenes(self,scenes):
        i = 0
        while i < len(scenes)-1:
            while len(set(scenes[i+1][1])-set(scenes[i][1])) == 0:
                scenes[i][0].extend(scenes[i+1][0][1:])
                scenes[i] = (scenes[i][0],scenes[i][1],(scenes[i][2]+scenes[i+1][2]) )
                del scenes[i+1]
                if i >= len(scenes)-1:
                    break
            i = i+1

    def coccur_mat(self,char_list,scenes):
        char_mat = np.zeros((len(char_list),len(char_list)))
        #Collect char-char sentiment here?
        #TODO: Increase cooccurrence score based on the overal scene score?
        for scene,scene_char,score in scenes:
            for w in scene_char:
                w_id = char_list.index(w)
                for c in scene_char:
                    c_id = char_list.index(c)
                    char_mat[w_id][c_id] = char_mat[w_id][c_id]+score #TODO: CHECK HERE!!! += score OR, += 1???
                    if c_id != w_id:
                        char_mat[c_id][w_id] = char_mat[c_id][w_id]+score
        return char_mat

    def read_script(self,script):
        char_list,keywords = self.tf.get_keywords(script)
        if len(char_list) == 0:
            return None

        scenes = self.get_char_scene(script,char_list,keywords)
        
        char_mat = self.coccur_mat(char_list,scenes)
        
        scenes.sort(reverse=True, key=lambda x:x[-1])
        scenes = scenes[:self.SCENE_COUNT]
        
        g = Graph(char_mat,char_list)
        g.show()
        g.keep_most_central()
        g.show()
       
        for scene,char,score in scenes[:5]:
            print '\n'.join(scene)
            print '________________________________'
            print char
            print '____________',score,'___________'

        dialogue = ['\n'.join(["" if l.isupper() else l for l in stext]) for stext,clist,score in scenes[:self.SCENE_COUNT]]
        vectored = self.encoder.encode('\n'.join(dialogue))
        return (scenes,vectored)

#Testing
reader = Reader('/home/user/movies/new/tfidf_model1.pkl',10,50,2500)
scripts = sm.load_scripts_path('/home/user/movies/scripts_des/',count=1)
for name,script in scripts:
    print name
    reader.read_script(script)
