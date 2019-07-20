# -*- coding: utf-8 -*-

import pandas as pd
import random

if __name__ == "__main__":
    items_csv = pd.read_csv("./input/items.csv")
    items = {}
    items_check = []
    items_index = []
    for item_csv in items_csv:
        item_copies = [
          item = Item(
            item_csv.id,
            copy,
            item_csv.shape,
            item_csv.material,
            item_csv.surface,
            item_csv.constitution
          ) for copy in range(25)
        ]
        items[item_csv.id] = item_copies
        items_index.extend([item_csv.id for i in range(25)])
    items_check = items.copy()
    disputes = []
    for dispute_id in range(400):
        first = random.randint(0, 65)
        second = random.randint(0, 65)
        while second == first:
            second = random.randint(0, 65)
            if not second in items_index:
                second = first
        items_index.remove(second)
        third = random.randint(0, 65)
        while third == first or third == second:
            third = random.randint(0, 65)
            if not third in items_index:
                third = first
        items_index.remove(third)
        forth = random.randint(0, 65)
        while forth == first or forth == second or forth == third:
            forth = random.randint(0, 65)
            if not forth in items_index:
                forth = first
        items_index.remove(forth)
        dispute = Dispute(
          dispute_id,
          items_check[first][0],
          items_check[second][0],
          items_check[third][0],
          items_check[forth][0]
        )
        items_check[first][0].set_dispute(dispute_id)
        items_check[second][0].set_dispute(dispute_id)
        items_check[third][0].set_dispute(dispute_id)
        items_check[forth][0].set_dispute(dispute_id)
        del items_check[first][0]
        del items_check[second][0]
        del items_check[third][0]
        del items_check[forth][0]
        disputes.append(dispute)


    disputes_check = disputes.copy()
    result = {
      'form' : [],
      'form_position' : [],
      'dispute' : [],
      'first' : [],
      'second' : [],
      'third' : [],
      'forth' : []
    }
    forms = []
    for form_id in range(20):
        form = Form(form_id)
        result['form'].append(form_id)

        for dispute_position in range(20):
            dispute = disputes_check[random.randint(0, Len(disputes_check))]
            while not form.audict_dispute(dispute,dispute_position):#check if it are able to add this dispute in this position based on some criteria
                dispute = disputes_check[random.randint(0, Len(disputes_check))]
            result['dispute'].append(dispute.id)
            result['form_position'].append(dispute.id)
            result['first'].append(dispute.first)
            result['second'].append(dispute.second)
            result['third'].append(dispute.third)
            result['forth'].append(dispute.forth)
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
      'forth'
    ])


    export_csv = df.to_csv (r'./output/disputes.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path
