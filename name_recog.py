import spacy


nlp=spacy.load("en_core_web_sm")
text="Graham Campbell,  Peter Campbell, Orlando Campbell, Freddie Iron"


doc=nlp(text)
names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
print(names)
 