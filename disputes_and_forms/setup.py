# -*- coding: utf-8 -*-

import pandas as pd
import random
import os.path
from item import Item
from dispute import Dispute
from form import Form

def my_random(all_items,first_items):
    result = random.randint(0, len(all_items)-1)
    while items_index[result] in first_items:# or not (second in items_index):
        result = random.randint(0, len(all_items)-1)
    return all_items.pop(result)

if __name__ == "__main__":
    items = {}
    items_check = []
    items_index = []
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input", "items.csv")
    items_csv = pd.read_csv(filename)
    items_csv.info()
    for data in items_csv.itertuples():
        item_copies = [
          Item(
            data.id,
            copy,
            data.shape,
            data.material,
            data.surface,
            data.color,
            data.constitution
          ) for copy in range(25)
        ]
        items[data.id] = item_copies
        items_index.extend([data.id for i in range(25)])
    items_check = items.copy()
    disputes = []
    for dispute_id in range(400):#20 forms X each one with 20 disputes = 400
        first = my_random(items_index, [])
        
        ##first = random.randint(0, len(items_index)-1)#64 (0..63) combinations of attributes (shape, material, etc)
        #while not (first in items_index):
        #    first = random.randint(0, 63)
        ##first = items_index.pop(first)

        second = my_random(items_index, [first])

        #second = random.randint(0, len(items_index)-1)
        #while items_index[second] == first:# or not (second in items_index):
        #    second = random.randint(0, len(items_index)-1)
        #second = items_index.pop(second)

        third = my_random(items_index, [first,second])

        #third = random.randint(0, 63)
        #while third == first or third == second or not (third in items_index):
        #    third = random.randint(0, 63)
        #items_index.remove(third)

        fourth = my_random(items_index, [first,second,third])

        #fourth = random.randint(0, 63)
        #while fourth == first or fourth == second or fourth == third or not (fourth in items_index):
        #    fourth = random.randint(0, 63)
        #items_index.remove(fourth)
        dispute = Dispute(
          dispute_id,
          items_check[first][0],
          items_check[second][0],
          items_check[third][0],
          items_check[fourth][0]
        )
        items_check[first][0].dispute = dispute_id
        items_check[second][0].dispute = dispute_id
        items_check[third][0].dispute = dispute_id
        items_check[fourth][0].dispute = dispute_id
        del items_check[first][0]
        del items_check[second][0]
        del items_check[third][0]
        del items_check[fourth][0]
        disputes.append(dispute)


    disputes_check = disputes.copy()
    result = {
      'form' : [],
      'form_position' : [],
      'dispute' : [],
      'first' : [],
      'second' : [],
      'third' : [],
      'fourth' : []
    }
    forms = []
    for form_id in range(20):
        form = Form(form_id)
        for dispute_position in range(20):
            dispute = disputes_check[random.randint(0, len(disputes_check)-1)]
            check = 0
            while form.audict_dispute(dispute,dispute_position):#check if it are able to add this dispute in this position based on some criteria
                dispute = disputes_check[random.randint(0, len(disputes_check)-1)]
                check = check + 1
                if check >= 10:
                  break
            result['form'].append(form_id)
            result['dispute'].append(dispute.id)
            result['form_position'].append(dispute_position)
            result['first'].append(dispute.first)
            result['second'].append(dispute.second)
            result['third'].append(dispute.third)
            result['fourth'].append(dispute.fourth)
            form.append_dispute(dispute)
            disputes_check.remove(dispute)
        forms.append(form)

    df = pd.DataFrame(result, columns= [
      'form',
      'form_position',
      'dispute',
      'first',
      'second',
      'third',
      'fourth'
    ])

    filename = os.path.join(dirname, "output", "disputes.csv")
    export_csv = df.to_csv(filename, index = None, header=True, encoding='utf-8') 
