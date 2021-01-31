#!/usr/bin/env python
# coding: utf-8

# ## Python Libraries

# In[1]:


import sys
import time
import re
import pandas as pd
from itertools import compress


# ## Reading CSV and Text Files

# In[2]:


words_data = pd.read_csv("G:/Programs/Exeter/french_dictionary.csv", header=None)
words_data.index = words_data[0]
words_data.drop(labels=[0], axis=1, inplace=True)
words_data.index.name = "english"
words_data.columns = ["french"]


# In[3]:


find_words = []
file = open("G:/Programs/Exeter/find_words.txt")
find_words = ["".join(lines.split()) for lines in file.readlines()]
file.close()


# In[4]:


replace = []
file = open("G:/Programs/Exeter/t8.shakespeare.txt")
replace = ["".join(lines.replace("\n", "")) for lines in file.readlines()]
file.close()


# ## Counting Find Words Before Translating

# In[5]:


words_count_before = {word:0 for word in find_words}
freq_replace = {word:0 for word in find_words}


# In[6]:


for i in range(len(replace)):
    splitted_words = replace[i].split()
    status = [True if (i.lower() in find_words) else False for i in splitted_words]
    idx = list(compress(range(len(status)), status))
    if len(idx) > 0:
        for j in idx:
            words_count_before[splitted_words[j].lower()] = words_count_before.get(splitted_words[j].lower()) + 1
    else:
        pass


# ## Translating from English to French

# In[7]:


start_time = time.time()

for i in range(len(replace)):
    splitted_words = replace[i].split()
    status = [True if (i.lower() in find_words) else False for i in splitted_words]
    idx = list(compress(range(len(status)), status))
    if len(idx) > 0:
        for j in idx:
            freq_replace[splitted_words[j].lower()] = freq_replace.get(splitted_words[j].lower()) + 1
            splitted_words[j] = words_data.loc[splitted_words[j].lower()].values[0]
        replace[i] = " ".join(splitted_words)
    else:
        pass

end_time = time.time()
print("Time Taken to Translate : ", round((end_time - start_time),0), "seconds.")


# ## Objects Memory Size

# In[8]:


print("Size of Find Words : ", sys.getsizeof(find_words), "bytes.", "(", sys.getsizeof(find_words) / 1e+6, "in MB)")
print("Size of English to French Dictionary : ", sys.getsizeof(words_data), "bytes.", "(", sys.getsizeof(words_data) / 1e+6, "in MB)")
print("Size of Replacement Text : ", sys.getsizeof(replace), "bytes.", "(", sys.getsizeof(replace) / 1e+6, "in MB)")
total_size = (sys.getsizeof(find_words) / 1e+6) + (sys.getsizeof(words_data) / 1e+6) + (sys.getsizeof(replace) / 1e+6)
print("Total Memory Size Required : ", total_size, "MB")


# ## Writing the Translated Script

# In[9]:


final = [replace[i] + "\n" for i in range(len(replace))]


# In[10]:


file = open("G:/Programs/Exeter/translated_output.txt", 'w')
file.writelines(final)
file.close()


# ## Checking Whether All Words are Replaced

# In[11]:


status = []
for i, j in zip(words_count_before.items(), freq_replace.items()):
    if (i[1] - j[1]) != 0:
        print(i[0], "wasn't replaced completely.")
    else:
        status.append(True)


# ## Writing the Frequency of Words Replaced in CSV File

# In[12]:


final_res = pd.DataFrame(data=[freq_replace.keys()]).T
final_res.columns = ["English"]


# In[13]:


final_df = pd.concat([final_res, words_data["french"]], axis=1)


# In[14]:


french_words = words_data["french"]
french_words.index = range(1000)


# In[15]:


final_df = pd.concat([final_res, words_data["french"]], axis=1)


# In[16]:


final_df = pd.concat([final_df, pd.Series(freq_replace.values(), index=range(1000))], axis=1)
final_df.columns = ["English", "French", "Frequency Replaced"]


# In[17]:


final_df.to_csv("G:/Programs/Exeter/replaced_frequency.csv", index=None)

