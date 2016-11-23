import matplotlib.pyplot as plt
import numpy as np
import os

def total(array): #Function to calculate total of an array
    total=0
    for i in range(len(array)):
        total=total+array[i]
    return total
    
def char_freq(file_name, filt): #Function which reads a file based on characters in filter
    data=[]
    counter_array=np.zeros(len(filt))
    cwd=os.getcwd()
    path=cwd+"\\"+file_name
    file=open(path,'r',encoding='utf-8')
    for line in file:
        data.append(line)
    words=str(data)
    for character in words:
        for i in range(len(filt)):
            if character==filt[i]:
                counter_array[i]+=1
    tot=total(counter_array)            
    for i in range(len(counter_array)):
        counter_array[i]=counter_array[i]/tot
    return counter_array

def plot_histogram(array):
    plt.figure()
    for char_count in array:
        plt.subplot(411)
        plt.hist(char_count)
        plt.show()
        plt.savefig('histograms_of_books.png')
        
def euc_distance(x,y): #Calculating Eucledian Distance between two Multidimentional Vectors of Same Length
        return  np.sqrt(np.sum((x-y)**2))
    

def cldist(c1,c2):  #Minimum Cluster_distance
    d=np.infty
    for x in c1:
        for y in c2:
            if euc_distance(x,y)<d:
                d=euc_distance(x,y)
    return d


def closest(L): #Find the closest cluster out of list of clusters
    d=np.infty
    a,b=-1,-1
    for i in range(len(L)-1):
        for j in range(i+1,len(L)):
            if cldist(L[i],L[j])<d:
                d=cldist(L[i],L[j])
                a,b=i,j
    return (a,b)
    

def initialize_clusters(L):
    clusters=[]
    for i in range(len(L)):
        clusters.append(i)
    return clusters


def pairs(points,clusters):
    pairs=[]
    dist=[]
    for i in range(len(clusters)):
        for j in range(i+1,len(clusters)):
            pairs.append([i,j])
            dist.append(euc_distance(points[i],points[j]))
    return (pairs,dist)
                    
              
def ranking(points,clusters):
    list1,list2=pairs(points,clusters)
    list3=[]
    for i in range(len(list2)):
        (m,index)=min((v,i) for i,v in enumerate(list2))
        list3.append(list1[index])
        del list1[index]
        del list2[index]
    return list3


def search_in_list(L,key):
    index=-1
    for i in range(len(L)):
        if type(L[i])==list:
            if key in L[i]:
                index=i
    return index          

def add_lists(L1,L2):
    L3=[]
    for element in L1:
        L3.append(element)
    for element in L2:
        L3.append(element)
    return L3

def delete_in_list(clusters,key):
    for cluster in clusters:
        if type(cluster)==list:
            if key in cluster:
                clusters.remove(cluster)
    return clusters

def make_new_cluster(clusters,c1,c2):
    clusters.remove(c1)
    clusters.remove(c2)
    clusters.append([c1,c2])
    return clusters

def merge_two_clusters(clusters,key_1,key_2):
    index1=search_in_list(clusters,key_1)
    index2=search_in_list(clusters,key_2)
    new_elements=add_lists(clusters[index1],clusters[index2])
    clusters=delete_in_list(clusters,key_1)
    clusters=delete_in_list(clusters,key_2)
    clusters.append(new_elements)
    return clusters

def add_key_in_cluster(clusters,key_1,key_2):
    index=search_in_list(clusters,key_1)
    clusters[index].append(key_2)
    clusters.remove(key_2)
    return clusters
    
def already_same_cluster(clusters,c1,c2):
    flag=0
    for cluster in clusters:
        if type(cluster)==list:
            if c1 in cluster:
                if c2 in cluster:
                    flag=1
    return flag

def single(L,k=2):
    clusters=initialize_clusters(L)
    rank=ranking(L,clusters)
    for closest_pair in rank:
        c1,c2=closest_pair[0],closest_pair[1]
        if search_in_list(clusters,c1)!=-1:
            if search_in_list(clusters,c2)!=-1: #Merge Two Clusters
                print (" Step "+str(closest_pair)+" Merging Two Clusters")
                if already_same_cluster(clusters,c1,c2)!=1:
                    clusters=merge_two_clusters(clusters,c1,c2)
            else: #Add C2 to the Cluster where c1 is Present
                print (" Step "+str(closest_pair)+" Adding c2 in Cluster where c1 is")
                clusters=add_key_in_cluster(clusters,c1,c2)
        else:
            if search_in_list(clusters,c2)!=-1: #Add C1 to the Cluster where C2 is Present
                print (" Step "+str(closest_pair)+" Adding c1 in Cluster where c2 is")
                clusters=add_key_in_cluster(clusters,c2,c1)
            else: #Make a New Cluster
                print (" Step "+str(closest_pair)+" Making New Cluster")
                clusters=make_new_cluster(clusters,c1,c2)
        if len(clusters)==k:
            break
        
    return clusters
