import pickle
import re

# example_dict = [{1:"6",2:"2",3:"f"},{5:"hello"}]
#
# pickle_out = open("dict.pickle","wb")
# pickle.dump(example_dict, pickle_out)
# pickle_out.close()

# a = {1:[2,3,4],2:[3,4,5],3:[4,5,6]}
# s = ""
# for key,val in a.items():
#     s += "\n" +str(key) + ":" + str(a[key])
# print (s)
#
# s = "<em>hello</em> so i want to say <em>there</em>"
# for i in re.findall("<em>(.*?)</em>",s):
#     print(i)
s = "hello there bitch"
s = s.replace("hello","")
print(s)

results = {'a':["My name is lola bitch what <mark>are</mark> <mark>you</mark> talking about","never love you <mark>like,</mark> i loved ya","never cheat never lied","never put no one above ya","i gave you space and time","do you stay up late","just <mark>so</mark> <mark>you</mark> can dream"],'b':["hello <mark>there</mark>"]}
# term = "lola bitch"
# results.replace(new RegExp(term, "gi"), (match) => `<mark>${match}</mark>`);
for key,val in results.items():
    temp = []
    for i in results[key]:
        print(i)
        try:
            # word = re.search(r'<mark>(.*?)</mark>', i).group(1)
            words = re.findall(r'<mark>(.*?)</mark>', i)
            for word in words:
                if word in i:
                    i = i.replace(word,word.upper())
            temp.append(i)
        except:
            temp.append(i)
    results[key] = temp
# print(results)

user_query = "hello there"
words = user_query.split()