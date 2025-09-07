
RUN_NAME = 'alpha'
BATCH_SIZE = 500
DATA_PATH = 'data_pipeline/data'

EXPORT_FOLDER = f'{DATA_PATH}/{RUN_NAME}'

BASE_PRODUCT_PRICES = {
    'swim shorts': '14.99',
    'jacket': '49.99',
    'shorts': '19.99',
    'trousers': '24.99',
    'shoes': '34.99',
    't-shirt': '9.99',
    'jeans': '24.99',
    'belt': '9.99',
    'jumper': '19.99',
    'necklace': '6.99',
    'gilet': '29.99',
    'sweatshirt': '17.99',
    'bag': '14.99',
    'socks': '4.99',
    'gloves': '5.99',
    'briefs': '7.99',
    'cardigan': '19.99',
    'top': '12.99',
    'blazer': '34.99',
    'sunglasses': '9.99',
    'coat': '59.99',
    'scarf': '6.99',
    'pyjamas': '14.99',
    'cap': '7.99',
    'shirt': '19.99',
    'ring': '4.99',
    'pyjama bottoms': '9.99',
    'beanie': '6.99',
    'hat': '7.99',
    'hydration vest': '9.99',
    'slippers': '9.99',
    'leggings': '12.99',
    'handkerchief': '2.99',
    'sunglasses, glasses': '14.99',
    'beanie, scarf': '11.99',
    'hairband': '3.99',
    'bracelet, necklace': '8.99',
    'swim top': '12.99',
    'shorts, t-shirt': '17.99',
    'waistcoat': '24.99',
    'cycling bib shorts': '22.99',
    'bracelet': '4.99',
    'bow tie': '6.99',
    'earrings': '5.99',
    'scarf, beanie': '11.99',
    'pyjama shorts': '8.99',
    
    # Newly added items (still allowed)
    'ski goggles': '19.99',
    'pyjama top': '8.99',
    'gloves, beanie, scarf': '14.99',
    'sun visor': '6.99',
    'swimming cap': '4.99',
    'mittens': '5.99',
    'headband': '3.99'
}

# BASE_PRODUCT_PRICES = {
#     'swim shorts': '14.99',
#     'jacket': '49.99',
#     'shorts': '19.99',
#     'trousers': '24.99',
#     'shoes': '34.99',
#     't-shirt': '9.99',
#     'jeans': '24.99',
#     'belt': '9.99',
#     'jumper': '19.99',
#     'necklace': '6.99',
#     'gilet': '29.99',
#     'sweatshirt': '17.99',
#     'bag': '14.99',
#     'socks': '4.99',
#     'gloves': '5.99',
#     'briefs': '7.99',
#     'cardigan': '19.99',
#     'top': '12.99',
#     'blazer': '34.99',
#     'sunglasses': '9.99',
#     'coat': '59.99',
#     'scarf': '6.99',
#     'pyjamas': '14.99',
#     'cap': '7.99',
#     'shirt': '19.99',
#     'ring': '4.99',
#     'pyjama bottoms': '9.99',
#     'beanie': '6.99',
#     'hat': '7.99',
#     'keyring': '2.99',
#     'hydration vest': '9.99',
#     'fashion scarf': '7.99',
#     'slippers': '9.99',
#     'dressing gown': '14.99',
#     'leggings': '12.99',
#     'handkerchief': '2.99',
#     'jacket, cardigan': '39.99',
#     'sunglasses, glasses': '14.99',
#     'beanie, scarf': '11.99',
#     'hairband': '3.99',
#     'bracelet, necklace': '8.99',
#     'swim top': '12.99',
#     'card holder': '6.99',
#     'passport cover': '4.99',
#     'shorts, t-shirt': '17.99',
#     'laptop case': '14.99',
#     'waistcoat': '24.99',
#     'cycling bib shorts': '22.99',
#     'bib style neck warmer': '6.99',
#     'water bottle': '5.99',
#     'bracelet': '4.99',
#     'bow tie': '6.99',
#     'earrings': '5.99',
#     'sweatshirt, trousers': '29.99',
#     'scarf, beanie': '11.99',
#     'laundry bag': '6.99',
#     'tie': '7.99',
#     'necklace, bracelet': '8.99',
#     'pyjama shorts': '8.99',
#     'blazer, trousers': '39.99',
#     'wallet': '9.99'
# }

# t-shirt
# jacket
# trousers
# slippers
# top
# shorts
# shoes
# jumper
# sweatshirt
# belt
# hat
# tie
# coat
# gilet
# blazer
# scarf
# cap
# swim shorts
# cardigan
# shirt
# leggings
# beanie
# sunglasses
# socks
# briefs
# pyjamas
# pyjama bottoms
# bag
# necklace
# ring
# jeans
# gloves
# sunglasses, glasses
# earrings
# ski goggles
# scarf, beanie
# bracelet, necklace
# pyjama top
# waistcoat
# bow tie
# gloves, beanie, scarf
# bracelet
# shorts, t-shirt
# beanie, scarf
# swim top
# sun visor
# swimming cap
# mittens
# hydration vest
# cycling bib shorts
# headband
# pyjama shorts
# hairband
# handkerchief

# t-shirt  :  2018
# jacket  :  1091
# trousers  :  1484
# slippers  :  35
# top  :  355
# shorts  :  1078
# shoes  :  566
# jumper  :  541
# sweatshirt  :  894
# belt  :  90
# hat  :  94
# tie  :  9
# coat  :  104
# gilet  :  94
# blazer  :  181
# scarf  :  86
# cap  :  212
# swim shorts  :  226
# cardigan  :  128
# shirt  :  408
# leggings  :  33
# beanie  :  186
# sunglasses  :  208
# socks  :  233
# briefs  :  172
# pyjamas  :  124
# pyjama bottoms  :  77
# bag  :  91
# necklace  :  143
# ring  :  65
# jeans  :  115
# gloves  :  34
# sunglasses, glasses  :  11
# earrings  :  6
# ski goggles  :  3
# scarf, beanie  :  3
# bracelet, necklace  :  4
# pyjama top  :  2
# waistcoat  :  9
# bow tie  :  8
# gloves, beanie, scarf  :  2
# bracelet  :  10
# shorts, t-shirt  :  3
# beanie, scarf  :  11
# swim top  :  3
# sun visor  :  3
# swimming cap  :  1
# mittens  :  3
# hydration vest  :  5
# cycling bib shorts  :  7
# headband  :  3
# pyjama shorts  :  4
# hairband  :  2
# handkerchief  :  4


TYPE_BLACKLIST = [
    'lapel pin',
    'scarf, gloves, beanie',
    'water bottle',
    'dogwear',
    'sweatshirt, trousers',
    'bib style neck warmer',
    'laundry bag',
    'keyring',
    'glasses',
    'fashion scarf',
    'tie',
    'necklace, bracelet',
    'dressing gown',
    'card holder',
    'shaker bottle',
    'towel',
    'wallet',
    'brooch',
    'laptop case',
    'personal alarm',
    'wallet chain',
    'passport cover',
    'hood',
    'jacket, cardigan',
    'smartphone case',
    'blazer, trousers'
]