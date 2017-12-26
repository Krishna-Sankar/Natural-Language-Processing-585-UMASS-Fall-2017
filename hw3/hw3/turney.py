from collections import defaultdict

def mutual_info(word,polarity):
    pmi = 0.0
    if polarity == 'positive':
        pmi = math.log(pos_seed_mentions[word] / (mentions[word] * mentions['positive'] * 1. / num))
    elif polarity == 'negative':
        pmi = math.log(neg_seed_mentions[word] / (mentions[word] * mentions['negative'] * 1. /num))


    return pmi

def symbol_avoid(token):
    return token in seed_pos or \
        token in seed_neg or \
        token.startswith("https://") or \
        token.startswith("#") or \
        token.startswith("@") 


seed_pos = ["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]
seed_neg = ["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]
num = 0
mentions = defaultdict(float) 
counts = defaultdict(float) 
polarity_dict =  defaultdict(float)



import math
pos_seed_mentions = defaultdict(lambda:0.01) 
neg_seed_mentions = defaultdict(lambda:0.01) 


with open("tweets.txt") as data:
    for line in data.readlines():
        tweets = [x.lower() for x in line.split()]
        forms = [x.lower() for x in list(set(tweets))] 
        POS_FOUND = any(x in seed_pos for x in forms)
        NEG_FOUND = any(x in seed_neg for x in forms)

        if POS_FOUND:
            mentions['positive'] += 1 
        if NEG_FOUND:
            mentions['negative'] += 1 

        for index in tweets:
            counts[index] += 1

        for template in forms:
            mentions[template]+=1
            if POS_FOUND:
                pos_seed_mentions[template] += 1
            if NEG_FOUND:
                neg_seed_mentions[template] += 1
        num += 1

        
        
for token,count in mentions.iteritems():
    if not symbol_avoid(token):
        polarity_dict[token] = mutual_info(token,'positive') - mutual_info(token,'negative')

def print_top50():
    print "Top - 50 Positive Words: \n\n"
    p=0
    for word in sorted(polarity_dict, key=polarity_dict.get, reverse=True)[:50]:
        p+=1
        print p,".",word,"=>", polarity_dict[word]

    print "Top - 50 Negative Words: \n\n"
    n=0
    for word in sorted(polarity_dict, key=polarity_dict.get)[:50]:
        n+=1
        print n,".",word,"=>", polarity_dict[word]

def print_top50withfilter():
    num_pos = 0
    p=0
    print "Top - 50 POSITIVIE WORDS:\n" 
    for word in sorted(polarity_dict, key=polarity_dict.get, reverse=True):
        if num_pos < 50:
            if counts[word] >= 500:
                num_pos += 1
                p+=1
                print p,".",word,"=>", polarity_dict[word]

    num_neg = 0
    n=0
    print "Top 50 Negative Words: \n\n"
    for word in sorted(polarity_dict, key=polarity_dict.get):
        if num_neg < 50:
            if counts[word] >= 500:
                n+=1
                print n,".",word,"=>", polarity_dict[word]
                num_neg += 1

    
   
    
        




