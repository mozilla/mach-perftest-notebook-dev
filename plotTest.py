import numpy as np
import matplotlib.pyplot as plt
import json


'''
For testing only.
Delete later.
But save it for now.

'''
def main():
    with open('testing/output/data.json') as f:
        data_JSON = json.load(f)

        print(len(data_JSON))

        print(data_JSON[0].keys())

        print(type(data_JSON))

        fig,ax = plt.subplots()

        for element in data_JSON:
            x = element['xaxis']
            y = element['data']
            label = element['name']+"\n"+element['subtest']
            ax.scatter(x,y,label=label)
        
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

if __name__=="__main__":
    main()
