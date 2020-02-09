import sys; sys.path.append("..") #compatibility github-pycharm
from tabulate import tabulate
from src import templates


def find_label(width_min = 0, width_max = 300, height_min = 0, height_max = 300, sortkey=(1,2)):

    tempKeys = templates.__dict__.keys()
    tempKeys = list(filter(lambda x: x[:5] == "Herma" or x[:5] == "Avery", tempKeys))

    labels = []
    for i in tempKeys:
        manufactuerer = i
        size = templates.__dict__[i]["size"]
        cnt = templates.__dict__[i]["cnt"]
        if size[0] >= width_min and size[0] <= width_max and size[1] >= height_min and size[1] <= height_max:
            labels.append((i,size[0],size[1],cnt[0]*cnt[1], cnt))

    from operator import itemgetter
    if type(sortkey) is tuple:
        labels = sorted(labels, key=itemgetter(*sortkey))
    elif type(sortkey) is int:
        labels = sorted(labels, key=itemgetter(sortkey))
    print(tabulate(labels, headers=["Manufactuerer", "Width", "Height", "Quantity", "Layout" ]))

if __name__ == "__main__":
    i = None
    while i is None:
        try:
            i = input("Sorting by\n 0 - manufacturer\n 1 - width-height\n 2 - height-width\n 3 - quantity\n?")
            i = int(i)
            if i <0 or i>3:
                i = None
                raise 'Invalid Input'
        except:
            print("Invalid Input\n")
            i = None
    if i == 1: i = 1, 2
    if i == 2: i = 2, 1
    print()
    find_label(sortkey=i)

