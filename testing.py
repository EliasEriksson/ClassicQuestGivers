class_pick = input().lower()

class_list = ['druid-c', 'druid-f', 'hunter', 'mage',
              'daladin', 'priest', 'shaman', 'warlock']

spirit_values = [[4.5, 15], [5, 15], [5, 15], [4, 12.5],
                 [5, 15], [4, 12.5], [5, 17], [5, 15]]

if class_pick in class_list:
    position = class_list.index(class_pick)

    # defining spirit_c and spirit_plus via indexing
    spirit_c = spirit_values[position][0]
    spirit_plus = spirit_values[position][1]

    # defining spirit_c and spirit_plus via unpacking
    spirit_c, spirit_plus = spirit_values[position]
