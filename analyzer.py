import scipy.stats as stats
import json
import os

class NotebookAnalyzer(object):
    '''
    Analyze the standardized data. The methods in these functions
    will be injected in an Iodide page in the future.
    '''

    def __init__(self, data):
        '''
        Initialize the Analyzer.

        :param dict data: Standardized data, post-transformation.
        '''
        self.data = data

    def split_subtests(self):
        '''
        If the subtest field exists, split the data based
        on it, grouping data into subtest groupings.
        '''
        if 'subtest' not in self.data[0]:
            return {'': self.data}

        split_data = {}
        for entry in self.data:                 # for every array element in data
            subtest = entry['subtest']          # subtest = subtest's name
            if subtest not in split_data:       # if subtest name does not exist
                split_data[subtest] = []        # create a new array for it
            split_data[subtest].append(entry)   # add corresponding JSON data to this array

        return split_data                       # returns an array of 
                                                # key: subtest name
                                                # value: subtest JSON object from self.data

    def ttest(self):
        '''
        Take the data and perform a cross-ttest on the rows.
        Data returned looks like the following:
        ```
            [
                {
                    'ttest': 7.2,
                    'pval': 0.01,
                    'name1': macosx-raptor,
                    'name2': macosx-browsertime
                }, ...
            ]
        ```

        :return dict: List of results.
        '''
        results = []

        split_data = self.split_subtests()

        for subtest in split_data:
            done = {}
            for entry1 in split_data[subtest]:
                name = entry1['name']

                for entry2 in split_data[subtest]:
                    if entry2['name'] == name:
                        continue
                    if '%s-%s' % (name, entry2['name']) in done or \
                       '%s-%s' % (entry2['name'], name) in done:
                       continue
                    done['%s-%s' % (name, entry2['name'])] = True

                    tval, pval = stats.ttest_ind(entry1['data'], entry2['data'])

                    results.append({
                        'ttest': tval,
                        'pval': pval,
                        'name1': name + '-%s' % subtest,
                        'name2': entry2['name'] + '-%s' % subtest,
                        'ts1': entry1['data'],
                        'ts2': entry2['data']
                    })

        return results

    # Write to Iodide Template File.
    # For now, it writes to the the folder "analysisOutput", 
    # with file name "new_notebook_content.iomd"
    # the actually server file locates at:
    # iodide\server\notebooks\templates
    # with the same name.

   
    def writeToIodideServer(self):
        # get result from analysis 
        results = self.ttest()

        # create file then write result to it.
        filename = "analysisOutput/new_notebook_content.iomd"
        os.makedirs(os.path.dirname(filename),exist_ok=True)

        with open(filename,"w") as f:
            f.write(str(results))

        return
    
    # if on local client only (without server), 
    # template file is located at:
    # src/editor/static.html
    # it is an html file. We should write to the <script> tag
    # for now, we output a html page. then copy this page 
    # to overwrite the static.html
    def writeToIodideClient(self):
        # get result from analysis 
        results = self.ttest()
        filename = "analysisOutput/static.html"

        with open(filename,"a+") as f:
            f.write(str(results))
        return


# Under development. For testing, a main will be runned here.

def main():
    # the test file is "transformedData/toIodide.json"
    # sample file contains:
    # [ 
    #   {
    #       data:[int]
    #       name:string
    #       subtest:string
    #       x-axis:[int]
    #   }
    # ]

    with open('transformedData/toIodide.json') as inputFile:
        inputData = json.load(inputFile)
        
    analyzer = NotebookAnalyzer(inputData) # create a new analyzer.
    results = analyzer.ttest()

    #analyzer.writeToIodideClient()

    # testing of write to file.
    filename = "static_copy.html"
    outputname = "static.html"
    with open(filename,"r+") as f:
            contents = f.readlines()
            
    start = 0
    # find index of <scrip> and </script> for template
    for index,line in enumerate(contents):
        if "script id=\"iomd\"" in line:
            start = index
            break
        
    if(start!=0):
        while("/script" not in contents[start+1]):
            del contents[start+1]
    
        contents_lowerHalf = contents[start+1:]
        contents = contents[:start+1]
    
        contents.append("<h2> T-Test Results</h2>\n\
<table>\n\
    <tr>\n\
        <th>name1</th>\n\
        <th>name2</th>\n\
        <th>t-value</th>\n\
        <th>p-value</th>\n\
    </tr>\n\
            ")
        '''
            'ttest': tval,
            'pval': pval,
            'name1': name + '-%s' % subtest,
            'name2': entry2['name'] + '-%s' % subtest,
            'ts1': entry1['data'],
            'ts2': entry2['data']
        '''
        for result in results:
            contents.append("\
                <tr>\n"+
                "<td>"+result['name1']+"</td>\n"+
                "<td>"+result['name2']+"</td>\n"+
                "<td>"+str(result['ttest'])+"</td>\n"+
                "<td>"+str(result['pval'])+"</td>\n"+
                "</tr>\n")
    
        contents.append("</table>\n")
        contents.extend(contents_lowerHalf)
    
        with open(outputname,"w") as f:
            f.writelines(contents)
    else:
        print ("error, no script found")


if __name__ == "__main__":
    main()
