import numpy as np


from keras.models import load_model
import pickle

from keras.preprocessing.sequence import pad_sequences 

from text_cleaner import TextCleaner# it's a class that I made so I can make it easier to clean text

#model1

# recall the model
model1 = load_model(r'C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL1\MODEL1_S&NS.h5')


file_path = r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL1/tokenizer1.pickle"
with open(file_path, 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)
    
    
model2 = load_model(r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL2\MODEL2_E&F.h5")
file_path = r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL2\tokenizer2.pickle"
with open(file_path, 'rb') as handle:
    loaded_tokenizer2 = pickle.load(handle)
        
    
model3 = load_model(r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL3\MODEL3_EA&EF.h5")


file_path = r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL3\tokenizer3.pickle"
with open(file_path, 'rb') as handle:
    loaded_tokenizer3 = pickle.load(handle)
        

model4 = load_model(r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL4\MODEL4_FA&FF.h5")


file_path = r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL4\tokenizer4.pickle"
with open(file_path, 'rb') as handle:
    loaded_tokenizer4 = pickle.load(handle)
    
pickle.dump(model1 ,open(r'C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL1\MODEL1_S&NS.pkl',"wb"))
pickle.dump(model2 ,open(r"C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL2\MODEL2_E&F.pkl","wb"))
pickle.dump(model3 ,open(r'C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL3\MODEL3_EA&EF.pkl',"wb"))
pickle.dump(model4 ,open(r'C:\Users\User\Desktop\NASA apps\A Marketplace for Open Science Projects\Model\codes\MODELS\MODEL4\MODEL4_FA&FF.pkl',"wb"))




#starting prediction

txt=input("text : ")
print("\n")



mytext = txt
cleaner = TextCleaner(mytext)
cleaned_text = cleaner.clean_text()
pos_tagged_text = cleaner.lemmatize_text(cleaned_text)
lemmatized_text = cleaner.lemmatize_with_wordnet(pos_tagged_text)
print("\n","clean text:",lemmatized_text,"\n")



sequences = loaded_tokenizer.texts_to_sequences([lemmatized_text])
max_sequence_length = 20  
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

predictions = model1.predict(padded_sequences)



#keywords = ["space", "model", "system","quantum","learn","satellite","function"]
#if any(keyword in txt for keyword in keywords):
#    predictions[:, 1]=predictions[:, 1]+0.07



predictedind1= np.argmax(predictions[0])# index of the highest probability

if predictedind1==0:
    predictedind1="not science"
elif predictedind1==1:
    predictedind1="science"


print("\n text topic :", predictedind1)



if predictedind1=="science":

    
#Model2
    
    sequences = loaded_tokenizer2.texts_to_sequences([lemmatized_text])
    max_sequence_length = 20  
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)
    
    predictions = model2.predict(padded_sequences)
    predictedind2= np.argmax(predictions[0])# index of the highest probability
    
    if predictedind2==0:
        predictedind2="Emprical"
    elif predictedind2==1:
        predictedind2="Formal"
    
    
    print("\n text topic :", predictedind2)

#model3

    if predictedind2=="Emprical":
 

        sequences = loaded_tokenizer3.texts_to_sequences([lemmatized_text])
        max_sequence_length = 20  
        padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)
        
        predictions = model3.predict(padded_sequences)
        predictedind3= np.argmax(predictions[0])# index of the highest probability
        
        if predictedind3==0:
            predictedind3="Application"
        elif predictedind3==1:
            predictedind3="Foundation"
        
        
        print("text topic :", predictedind3)


#model4

    elif predictedind2=="Formal":
    

        sequences = loaded_tokenizer4.texts_to_sequences([lemmatized_text])
        max_sequence_length = 20  
        padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)
        
        predictions = model4.predict(padded_sequences)
        predictedind4= np.argmax(predictions[0])# index of the highest probability
        
        if predictedind4==0:
            predictedind4="Application"
        elif predictedind4==1:
            predictedind4="Foundation"
        
        
        print("text topic :", predictedind4)






