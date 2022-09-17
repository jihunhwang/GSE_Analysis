import numpy as np
import sys
from Progress import printProgressBar

def find_substring_start_with(url, prefix = 'GSE'):
    return url[url.find(prefix):]

def crawler(content, regex = '<tr valign="top"><td nowrap>Summary</td>(.*?)</tr>', words = 'colon'):
    import re
    #Regex is the regular expression to extract the blocks in the given form. Here, we would like to choose the html block in which contains the Summary. 
    #Words which is regular expression contains all words in lower case that you want to identify if them are the substring of Summary
    a = re.findall(regex, content)[0].lower()

    # b = re.findall(words, a)
    #return True if given words are substring of summary o.w. False
    S = a.split()
    if words in S:
        return True
    else:
        return False
    # return True if len(b) != 0 else False

def run(Website = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE23034', regex = "", words = ""):
    try:
        #Check if the connection is working well
        import builtwith as bw
        try:
            # print("CP1")
            # import np
            # _ = "AAAA".lowercase()
            _ = bw.urllib2.urlopen(Website).read()
            test_result = bw.parse(Website)
            f = 'framework'
            try:
                #Find all keys contains substring framework
                keys = np.array(list(test_result.keys()))
                idx = np.flatnonzero(np.core.defchararray.find(keys,f)!=-1)
                frameworks = np.append([], [test_result[item] for item in keys[idx]])
                if np.flatnonzero(np.core.defchararray.find(frameworks,'AngularJS')!=-1).shape[0] == 0 and np.flatnonzero(np.core.defchararray.find(frameworks,'ASP.NET')!=-1).shape[0] == 0:
                    #Check if the Framework is using either AngularJS or ASP.NET since they are very hard to crawler
                    #If Not, we crawler the website
                    try:
                        import urllib3
                        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                        website = urllib3.PoolManager().request('GET', Website)
                        try:
                            return crawler(str(website.data),regex, words)
                        except:
                            # raise ErrorMessage('Crawler Error')
                            # print('Crawler Error')
                            return 'Crawler Error'
                        # print(website.data)
                    except:
                        # raise ErrorMessage('Install urllib3 Module')
                        return 'Install urllib3 Module'
                else:
                    # raise ErrorMessage('Cannot Crawler')
                    return 'Cannot Crawler'
            
            except:
                # raise ErrorMessage('No attribute is called {}'.format(f))
                return 'No attribute is called {}'.format(f)
        except: 
            # raise ErrorMessage('Unknown Error: {}'.format(sys.exc_info()))
            return 'Unknown Error: {}'.format(sys.exc_info())
                
            
    except:
        # raise ErrorMessage('Install Builtwith Module')
        return 'Install Builtwith Module  {}'.format(sys.exc_info())

def main(data, regex, words):
    import time
    # times = list(range(0,57))
    l = len(data)
    urls = np.array([])
    idxs = np.array([-1])
    BarLength = 50
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete, Found: 0 at iter: -1, Current: 0', length = BarLength)
    for i, item in enumerate(data):
        code = find_substring_start_with(item)
        res = run(item, regex, words)
        if res == True:
            urls = np.append(urls, code)
            idxs = np.append(idxs, i)
        elif res == False:
            pass
        else:
            print(res)
            break

        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete, Found: {} at iter: {}, Current: {}'.format(urls.shape[0], idxs[-1], i+1), length = BarLength)
    
    saved = np.vstack((idxs[1:], urls))
    with open('code.data', 'w') as f:
        for line in saved:
            for item in line:
                f.write("{},".format(item))
            f.write("\n")
    # print(saved)

    # np.savetxt('Colons.txt', saved, delimiter=',')

    # print(idxs, urls)
            
            

if __name__ == "__main__":
    import os
    import pandas as pd
    
    path = 'data/geo_expression/'#os.path.dirname('crawler.py')
    filename = sys.argv[1]
    print("Loading Data Set....")
    df = pd.read_excel(path + filename, index_col=0)
    gses = df['gse'].values
    prefix = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='
    # gses = np.array(['GSE15322','GSE18497','GSE29316','GSE30292','GSE39394','GSE53059','GSE64385','GSE77474','GSE78947'], dtype=np.str)
    urls = np.unique(prefix + gses)
    # gse = np.array(['GSE11886','GSE12583','GSE14405','GSE15322','GSE15791','GSE18497','GSE20484', 'GSE20504', 'GSE29253', 'GSE29316', 'GSE29770', 'GSE30292','GSE38156', 'GSE39394', 'GSE41469', 'GSE42140', 'GSE42807', 'GSE42947','GSE44444', 'GSE46824', 'GSE47621', 'GSE50738', 'GSE53059', 'GSE63662','GSE64385', 'GSE77474', 'GSE78947', 'GSE85180', 'GSE85260', 'GSE92354','GSE93984', 'GSE9709', 'GSE98237', 'GSE9832'])
    """
        This progeam will identity if a given string is in given websites
        Input: List of urls and words you are attemping to identify
            urls: List
            words: Regular Expression(lower case)
        Output:
            Find url that contains any of given words
    """
    print("Started")
    # urls = prefix + np.unique(gse)
    main(urls,'<tr valign="top"><td nowrap>Summary</td>(.*?)</tr>', 'colon')
    print('Done')