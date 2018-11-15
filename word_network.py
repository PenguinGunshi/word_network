from requests_oauthlib import OAuth1Session
import json
import config
import sys
import MeCab
import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from networkx.algorithms.centrality import degree_centrality
from networkx.algorithms.centrality import closeness_centrality
from networkx.algorithms.centrality import betweenness_centrality
#plt.rcParams['font.family'] = 'AppleGothic'
#from kadai2_2 import scan_communities
#from kadai2_2 import scan
#from kadai2_2 import search_clusters

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/search/tweets.json"


#Taggerの引数に-dオプションとmecab-ipadic-neologdの場所を指定する
#　↓場所の確認
# echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
m = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
m.parse('')  #最初にこの空文字のparseをしないとparseToNodeがなぜかできない

def tweet_search(keyword,f):
    sentence_list = []
    params = {'q' : keyword, 'count' : 1200}

    req = twitter.get(url, params = params)

    if req.status_code == 200:
        search_timeline = json.loads(req.text)
        for tweet in search_timeline['statuses']:
            bun = tweet['text']
            bun = bun.split('http')[0] #画像URLなどの削除
            bun = bun.replace("\n","")
            sentence_list.append(bun)
            #print(tweet['user']['name'] + '::' + tweet['text'])
            #print(type(tweet['text']))
            #print(tweet['created_at'])

            #print('----------------------------------------------------')
    else:
        print("ERROR: %d" % req.status_code)
    #print(sentence_list)
#print(sentence_list)

#ツイートごとに名詞を抽出する関数
#def meishi_search(keyword):
    #sentence_list = []
#tweet_search(keyword)
#print(sentence_list)
    for x in range(len(sentence_list)):
        meishi_list = []
        node = m.parseToNode(sentence_list[x])
        while (node):
        #if node.surface != "":
            if node.feature.split(",")[1] =="固有名詞" or node.feature.split(",")[0] =="形容詞":
                meishi_list.append(node.surface)
                #print(node.surface + '\t' + node.feature.split(",")[1])
            node = node.next
            if node is None:
                break
                
        for x in range(0,len(meishi_list)-1):
            f.write(meishi_list[x] + " " + meishi_list[x+1])
            f.write('\n')




#実行部分
#sentence_list = []
print("何を調べますか?")
keyword = input('>> ')
path_w = '単語リスト.txt'
#G = nx.read_edgelist('単語リスト.txt', nodetype = str)
with open(path_w, mode='w') as f:
    tweet_search(keyword,f)
    #print(sentence_list)
    #for x in range(len(sentence_list)):
        #print(sentence_list[x])
        #meishi_search(sentence_list[x])
#filewrite(f,meishi_list)
#with open(path_w) as f:
#print(f.read())
G = nx.read_edgelist('単語リスト.txt', nodetype = str)
#print(G.nodes)



def search_cluster(cluster_list, u):
    for i in range(len(cluster_list)):  #rangeで回したほうがいいらしい、setでは回せない
        if u in cluster_list[i]:
            return i
    print('error')

def scan(cluster_list, eps, mu, u, check):
    #計算済みだったらreturn
    if check[u] is True:
        return
    #σ(u,v)を計算する。
    #u = node_list[0]
    check[u] = True
    u_set = set(G.neighbors(u)) #uと繋がってるnodeをsetに入れておく
    u_set.add(u)  #u自身も入れておく
    u_list = list(u_set)  #list化
    sigma=[] #sigma_uvを入れておくリスト
    v_list =[] #coreだった時にσ(u,v)>=eのvを入れておくリスト
    for x in range(len(u_list)): #σ(u,v)の計算
        v = u_list[x]
        v_set = set(G.neighbors(v))
        v_set.add(v)
        sigma_uv = len(u_set & v_set) / math.sqrt((len(u_set)*len(v_set)))
        if sigma_uv >= eps:  #密度がeより高い
            sigma.append(sigma_uv)
            v_list.append(v)
    if len(sigma) < mu:
        return    #uはcoreではないと判定
    else:  #uはcoreだった！マージする
        #uとvが何番目(のクラスタ)か探して記憶する。vは複数あるかもしれない。uと同じクラスタだったらしない。マージ先vがすでに同じクラスタだった場合に一緒にやるという処理を書いておく。
        u_num = search_cluster(cluster_list, u)  #uがcluster_listの何番目か探す。(何番目のクラスタなのか)
        #print(u_num)
        #print(u_num)
        #v_num_list = []  #vが何番目のクラスタか記録しておくlist
        v_num_list = set()
        tmp = set() #仮のv
        for y in range(len(v_list)):  #v_listにはuのクラスタになるvが入ってる
            v_num = search_cluster(cluster_list, v_list[y])
            #if v_num not in v_num_list and v_num is not u_num:
            if v_num != u_num:
                #v_num_list.append(v_num)
                v_num_list.add(v_num)
                tmp.add(v_num)
        #print(tmp)
        #print(v_num_list)
        #↑すでに同じクラスタのvがいるor uと一緒の時、何番目のクラスタのvがいるのかが記憶されているので新たに書かない。一個あればマージできる
#merge.merge u-cluster and v-cluster
#v_num_list.sort()
#v_num_list.reverse()
#print(v_num_list)
#reversed(sorted(v_num_list))
#print(v_num_list)
#print(v_num_list)
    tmp_set = set()
    for z in tmp:
        tmp_set = tmp_set | cluster_list[z]
        #print(str(z)+" "+str(u_num)+" "+str(v_num_list[z]))
        #print(str(cluster_list[u_num])+" "+str(cluster_list[v_num_list[z]]))
        #print(u_num)
        #print(tmp[z])
        
    cluster_list[u_num] = cluster_list[u_num] | tmp_set
        #print(cluster_list[u_num])
    for z in reversed(sorted(tmp)):
            #cluster_list.pop(v_num_list[z])
        cluster_list.pop(z)
    #delete v-cluster. 後ろから消せば番号が早まることを考えなくて良い
#sorted(v_num_list)
#v_num_list.reverse()
#for a in range(len(v_num_list)):
#cluster_list.pop(a)
#print(cluster_list)
#再帰で次のvでscanを行う
#print(v_list)
#print(v_list[0])
    for v in v_list:
        scan(cluster_list, eps, mu, v, check)

def scan_communities(G, eps, mu):
    node_list = list(G.nodes)
    #各ノードをsetに入れる。それをマージしていってクラスタを作る。
    cluster_list =[]
    check = {}
    for i in range(len(node_list)):
        cluster_list.append(set((node_list[i],)))   #cluster_list, check scan_communitieやらない外で単体動作確認済み
        check.setdefault(node_list[i],False)
    #check[node_list[i]] = False
    #print(cluster_list)

    for u in nx.nodes(G):
        scan(cluster_list, eps, mu, u, check)
    print(cluster_list)
    return cluster_list

#node_list = list(G.nodes)
#cluster_list =[]
#check = {}
#for i in range(len(node_list)):
#   cluster_list.append(set((node_list[i],)))   #cluster_list, check scan_communitieやらない外で単体動作確認済み
#   check.setdefault(node_list[i],False)
#check[node_list[i]] = False
#print(cluster_list)

#print(cluster_list)
#print(search_cluster(cluster_list, node_list[0]))

eps = 0.5
mu = 3
c = scan_communities(G, eps, mu)




#ノードの色の指定
d = list(G.nodes)
g_dict = {}
for i in range(len(c)):
    g_dict[i] = i

c_list = []
for j in range(len(d)):
    for n in range(len(c)):
        if d[j] in c[n]:
            c_list.append(g_dict[n])





#中心性解析
#次数中心性
cent_values = degree_centrality(G).values()
cent_central = degree_centrality(G)
cent_keys = degree_centrality(G).keys()

#近接中心性
d_values = closeness_centrality(G).values()
d_central = closeness_centrality(G)
d_keys = closeness_centrality(G).keys()

#媒介中心性
bet_values = betweenness_centrality(G).values()
bet_central = betweenness_centrality(G)
bet_keys = betweenness_centrality(G).keys()

#sorted(d_dict.values())
d_values_list = list(d_values)
#print(d_values)
#print(d_keys)
#print(d_values_list)
a = 0
b = 0
c = 0
#次数中心性
print("次数中心性")
for k, v in sorted(cent_central.items(), key=lambda x: -x[1]):
    a += 1
    #10個表示したらおしまい
    if a is 11:
        break
    print(str(k) + ": " + str(v))
#近接中心性
print("近接中心性")
for k, v in sorted(d_central.items(), key=lambda x: -x[1]):
    b += 1
    #10個表示したらおしまい
    if b is 11:
        break
    print(str(k) + ": " + str(v))
#媒介中心性
print("媒介中心性")
for k, v in sorted(bet_central.items(), key=lambda x: -x[1]):
    c += 1
    #10個表示したらおしまい
    if c is 11:
        break
    print(str(k) + ": " + str(v))

#print(len(bet_values_list))
print("PageRank")
pr = nx.pagerank(G)
d = 0
for k, v in sorted(pr.items(), key=lambda x: -x[1]):
    d += 1
    #10個表示したらおしまい
    if d is 11:
        break
    print(str(k) + ": " + str(v))

d_values_list = list(d_values)
bet_values_list = list(bet_values)
node_size = [0] * len(d_values_list)
for v in range(len(d_values_list)):
    #次数中心性
    node_size[v] =  bet_values_list[v] * 3000
#近接中心性
#node_size[v] = 300 * d_values_list[v]
#媒介中心性
#node_size[v] = 3000 * d_values_list[v]
print(len(d_values_list))
pos = nx.spring_layout(G)
plt.figure(figsize=(6, 6))

nx.draw_networkx_edges(G, pos, edge_color='black', width=0.4, alpha=0.3)
nx.draw_networkx_nodes(G, pos, node_color=c_list, cmap = plt.cm.rainbow_r, node_size=node_size)
nx.draw_networkx_labels(G, pos, font_size=8,font_family = 'IPAexGothic',font_color="b")

plt.show()
