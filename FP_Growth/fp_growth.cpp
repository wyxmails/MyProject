#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <tuple>
using namespace std;
class TreeNode;
bool cmp(const TreeNode*,const TreeNode*);
class TreeNode{
public:
    vector<TreeNode*> children;
    string name;
    int count;
    TreeNode *parent,*nodeLink;
public: 
    TreeNode(string name,int occur,TreeNode* parent)
        :name(name),count(occur),parent(parent),nodeLink(NULL){}
    void inc(int num){
        count += num;
    }
    void disp(int ind=1){
        string tmp = "";
        tmp.append(ind,' ');
        cout << tmp << name << " " << count << endl;
        //sort(children.begin(),children.end(),cmp);
        for(int i=0;i<children.size();++i){
            children[i]->disp(ind+1);
        }
    }
};
    bool cmp(const TreeNode*a,const TreeNode*b){
        return a->count>b->count;
    }
struct LinkHead{
    int count;
    TreeNode *next;
    LinkHead():count(0),next(NULL){}
    LinkHead(int c):count(c),next(NULL){}
};

void updateHeader(TreeNode *tNode,TreeNode* target){
    while(tNode->nodeLink!=NULL)
        tNode = tNode->nodeLink;
    tNode->nodeLink = target;
}

void updateTree(vector<char> items, TreeNode*root, 
    map<char,LinkHead > &headerTable,int count){
    if(items.size()==0) return;
    if(root==NULL) return;
    bool found = false;
    int f=0;
    string key = "";
    key.append(1,items[0]);
    for(int i=0;i<root->children.size();++i)
        if(root->children[i]->name==key){
            root->children[i]->inc(count);
            found = true;
            f = i;
            break;
        }
    if(!found){
        f = root->children.size();
        root->children.push_back(new TreeNode(key,count,root));
        if(headerTable[items[0]].next==NULL)
            headerTable[items[0]].next = *root->children.rbegin();
        else
            updateHeader(headerTable[items[0]].next,*root->children.rbegin());
    }
    if(items.size()>1){
        //vector<char> nitems = move(items.begin()+1,items.end());
        vector<char> nitems;
        for(int i=1;i<items.size();++i)
            nitems.push_back(items[i]);
        updateTree(nitems,root->children[f],headerTable,count);
    }
}
TreeNode* createTree(map<string,int> dataSet,
    map<char,LinkHead> &headerTable, int minSup=1){
    map<char,int> hT;
    for(map<string,int>::iterator it=dataSet.begin();it!=dataSet.end();++it)
        for(int i=0;i<it->first.size();++i){
            hT[it->first[i]] += it->second;
        }
    set<char> freqItemSet;
    for(map<char,int>::iterator it=hT.begin();it!=hT.end();++it){
        if(it->second<minSup) continue;
        freqItemSet.insert(it->first);
        headerTable[it->first] = LinkHead(it->second);
    }
    if(freqItemSet.size()==0) return NULL;
    TreeNode *root = new TreeNode("Null Set",1,NULL);
    for(map<string,int>::iterator it=dataSet.begin();it!=dataSet.end();++it){
        int count = it->second;
        vector<pair<int,char> > localD;
        for(int i=0;i<it->first.size();++i)
            if(freqItemSet.find(it->first[i])!=freqItemSet.end())
                localD.push_back(make_pair(headerTable[it->first[i]].count,it->first[i]));
        if(localD.size()>0){
            sort(localD.begin(),localD.end());
            reverse(localD.begin(),localD.end());
            vector<char> orderedItems(localD.size());
            for(int i=0;i<localD.size();++i)
                orderedItems[i] = localD[i].second;
            updateTree(orderedItems, root, headerTable, count);
        }
    }
    return root;
}

vector<string> loadSimpDat(){
    vector<string> simpDat(6);
    simpDat[0] = "rzhjp";
    simpDat[1] = "zyxwvuts";
    simpDat[2] = "z";
    simpDat[3] = "rxnos";
    simpDat[4] = "yrxzqtp";
    simpDat[5] = "yzxeqstm";
    return simpDat;
}

map<string,int> createInitSet(vector<string> dataSet){
    map<string,int> retDict;
    for(int i=0;i<dataSet.size();++i)
        retDict[dataSet[i]] = 1;
    return retDict;
}
int main(int argc,char*argv[]){
    TreeNode*rootNode = new TreeNode("pyramid",9,NULL);
    rootNode->children.push_back(new TreeNode("eye",13,NULL));
    rootNode->disp();
    rootNode->children.push_back(new TreeNode("phoenix",3,NULL));
    rootNode->disp();
    vector<string> simpDat = loadSimpDat();
    map<string,int> initSet = createInitSet(simpDat);
    map<char,LinkHead> headerTable;
    cout << "create Tree Start..." << endl;
    TreeNode *root = createTree(initSet,headerTable,3);
    cout << "display Tree Start..." << endl;
    root->disp();
    return 0;
}
