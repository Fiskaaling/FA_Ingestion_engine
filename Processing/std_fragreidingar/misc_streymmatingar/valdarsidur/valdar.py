
def fjerna(event, siduval_dict):
    item = siduval_dict['valdar_tree'].identify('item', event.x, event.y)
    print(siduval_dict['valdar_tree'].index(item))
    siduval_dict['valdar_tree'].delete(item)

def upp(siduval_dict):
    item = siduval_dict['valdar_tree'].focus()
    hvar = siduval_dict['valdar_tree'].index(item)
    siduval_dict['valdar_tree'].move(item, '', max(hvar - 1, 0))

def nidur(siduval_dict):
    item = siduval_dict['valdar_tree'].focus()
    hvar = siduval_dict['valdar_tree'].index(item)
    count = len(siduval_dict['valdar_tree'].get_children('')) - 1
    siduval_dict['valdar_tree'].move(item, '', min(hvar + 1, count))

def setup(tree):
    pass
