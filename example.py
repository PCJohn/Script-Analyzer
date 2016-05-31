from tfidf import Tokenizer
import script_reader as sr
import script_manager as sm
import scene_extractor as se

#Create a reader
reader = sr.Reader()
#Create a scene extractor with the default TFIDF model provided: tfidf_model1.pkl
scene_finder = se.Scene_Extractor()
#Load the script of All the President's Men
scripts = sm.load_scripts('scripts_clean/',count=1,name='All the President\'s Men.txt')
for name,script in scripts:
    print name
    reader.show_all_and_main_char(script,F=1,centrality_type='betweenness')
    reader.centrality_trace(script,F=1,centrality_type='betweenness')
    scene_finder.main_scenes(script,5)
