from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = str(Path(__file__).resolve().parent.parent.parent)

GENERATED_PRODUCT_PATH = ROOT + '/backend/generated'

EMBEDDING_MODEL = 'text-embedding-3-large' #text-embedding-ada-002
LARGE_LANGUAGE_MODEL = 'gpt-4o-mini'

load_dotenv(ROOT + '/backend/secrets.env')  # specify your custom env file name

DATABASE_URL = os.getenv('DATABASE_URL')
AZURE_KEY = os.getenv('AZURE_KEY')


if EMBEDDING_MODEL == 'text-embedding-3-large':
    AZURE_EMBEDDING_URL = os.getenv('AZURE_EMBEDDING_LARGE_URL')
elif EMBEDDING_MODEL == 'text-embedding-ada-002':
    AZURE_EMBEDDING_URL = os.getenv('AZURE_ADA_URL')

AZURE_LLM_URL = os.getenv('AZURE_GPT_4o_URL')

MAX_TOKENS = 8191
PRODUCT_GENERATION_TEMPERATURE = 0.3
PRODUCT_GENERATION_MAX_TOKENS = 600

PRODUCT_GENERATION_SYSTEM_PROMPT = 'Return structured mens clothing product data for an item in a clothing catalog. The field "json_description" must contain a JSON string with keys like sizes, fabrics, style, etc. For example: {"fabrics": ["felted fabric"], "style": "casual"}'

HEADERS = {
    'Content-Type' : 'application/json',
    'api-key': AZURE_KEY
}

CLOTHING_TYPE_LIST = [
  'swim shorts',
  'jacket',
  'shorts',
  'trousers',
  'shoes',
  't-shirt',
  'jeans',
  'belt',
  'jumper',
  'necklace',
  'gilet',
  'sweatshirt',
  'bag',
  'socks',
  'gloves',
  'briefs',
  'cardigan',
  'top',
  'blazer',
  'sunglasses',
  'glasses',
  'coat',
  'scarf',
  'pyjamas',
  'cap',
  'shirt',
  'ring',
  'pyjama bottoms',
  'beanie',
  'hat',
  'hydration vest',
  'slippers',
  'leggings',
  'handkerchief',
  'hairband',
  'bracelet',
  'swim top',
  'waistcoat',
  'cycling bib shorts',
  'bow tie',
  'earrings',
  'pyjama shorts',
  'ski goggles',
  'pyjama top',
  'sun visor',
  'swimming cap',
  'mittens',
  'headband',
  'multi-pack'
]

CHAT_SYSTEM_PROMPT = 't'

DUMMY_MESSAGES = [
    {
      'role': 'system',
      'content': 'You are a helpful AI assistant that extracts and formats structured product data for an e-commerce catalog.'
    },
    {
      'role': 'user',
      'content': 'Hi, I want to add a new product to the catalog.'
    },
    {
      'role': 'assistant',
      'content': 'Sure! Please provide details such as name, description, price, colors, sizes, and image URL.'
    },
    {
      'role': 'user',
      'content': 'Here is the info: Hat in felted fabric with grosgrain band, colors: black dark, sizes: S/56, M/58, L/60, price: $14.99'
    }
]


PRODUCT_GENERATION_SCHEMA = {
        'type': 'function',
        'function': {
        'name': 'get_product_info',
        'description': PRODUCT_GENERATION_SYSTEM_PROMPT,
        'parameters': {
          'type': 'object',
          'properties': {
            'name': {
              'type': 'string',
              'description': 'The product name.'
            },
            'price': {
              'type': 'string',
              'description': 'Price of the product in GBP.'
            },
            'product_type': {
              'type': 'string',
              'enum': CLOTHING_TYPE_LIST,
              'description': 'Type of fashion product.'
            },
            'product_description': {
              'type': 'string',
              'description': 'Short description of the mens clothing product, what it looks like, shapes, colours and materials.'
            },
            'json_description': {
              'type': 'string',
              'description': 'Additional product metadata. This may include context of use, fabric details, fashion style. Structured as a JSON string.'
            },
            'color': {
              'type': 'array',
              'items': {
                'type': 'string'
              },
              'description': 'List of color variants.'
            },
          },
          'required': [
            'name',
            'price',
            'product_type',
            'product_description',
            'json_description'
          ]
        }
      }
    }


DECOMPOSITION_SYSTEM_PROMPT = '''You are a helpful assistant that prepares queries that will be sent to a search component.
Your job is to simplify complex requests about clothing into multiple requests that can be answered
in isolation to eachother, very important is that each separate request contains one request for a piece of clothing and that yo dont miss any.

Each request should include all relevant context but only one product.

If the query is simple, then keep it as it is.

Example:
User: I am looking for X piece of clothing and also a Y for a party
Response: 
I am looking for X piece of clothing for a party
I am looking for Y piece of clothing for a party


Respond now:
'''

DECOMPOSITION_GENERATION_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'split_questions',
        'description': DECOMPOSITION_SYSTEM_PROMPT,
        'parameters': {
            'type': 'object',
            'properties': {
                'questions': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    },
                    'description': 'List of questions, one for each clothing piece with all relevant context.'
                },
            },
            'required': [
                'questions',
            ]
        }
    }
}

DECOMPOSITION_TEMPERATURE = 0.3
DECOMPOSITION_MAX_TOKENS = 150



# Name: Shirt / Regular Fit football shirt
# Price: 14.99 GPB
# Type: t-shirt
# Description: Football shirt in printed mesh. Regular fit with a round neckline and short raglan sleeves with flatlock seams.
# External Brand: Placeholder
# Colors: red, white
# Concept: Placeholder Man Trend
# Brand: Placeholder
# Key Fabrics: Mesh
# Sleeve Length: Short sleeve
# Descriptive Length: Regular length Short sleeve
# Sleeve Style: Raglan sleeve
# Fit: Regular fit
# Assortment Type: Clothing
# Neckline Style: Round neck
# Garment Length: Regular length
# Age Group: Adult
# Style: Raglan sleeve Round neck
# Division: Menswear Complements

#  off-white
#  orange medium dusty
#  pistachio green
#  pale denim blue
#  amethyst
#  mole dark
#  black checked
#  rust orange
#  washed purple
#  brown dark
#  blue
#  dark navy blue
#  dark cerise
#  dark denim blue
#  blue medium dusty
#  moss green
#  green
#  mole medium dusty
#  pink dusty light
#  sage green
#  yellow medium
#  dark turquoise
#  white light
#  red bright
#  green light
#  dusky green
#  vintage black
#  light grey marl
#  dark teal
#  light greige marl
#  fern green
#  plum
#  orange light
#  dark burgundy
#  dusty brown
#  lilac
#  dark plum purple
#  grey melange dusty light
#  beige dusty light
#  blue-grey
#  pale green
#  bondi blue
#  dark green marl
#  light beige marl
#  light dusty turquoise
#  pink medium
#  blue medium
#  denim grey
#  metal bright
#  dark sage green
#  transparent beige
#  forest green
#  washed denim blue
#  gold-coloured
#  brown marl
#  dark pink marl
#  pink
#  greige
#  crimson red
#  denim green-blue
#  apricot pink
#  dark greige marl
#  dark grey marl
#  light yellow
#  dark old rose
#  dark dusty green
#  dark plum
#  denim brown
#  turquoise
#  grey-blue
#  light denim blue
#  cream
#  aqua blue
#  petrol
#  light brown
#  bright red
#  khaki brown
#  dusty green
#  khaki green dark
#  denim blue-grey
#  rust brown
#  apricot
#  pale purple
#  blue bright
#  denim red
#  red-brown
#  khaki green
#  cactus green
#  light denim grey
#  dark beige

#  transparent grey
#  black marl
#  dark khaki green marl
#  denim blue
#  silver-coloured
#  deep lilac
#  light green-beige
#  beige medium dusty
#  light orange
#  rust red
#  bright orange
#  lime green
#  washed green
#  emerald green
#  red
#  pigeon blue
#  grey dusty light
#  olive green
#  coral
#  dark red marl
#  bright turquoise
#  green dusty light
#  grey-green
#  coral red
#  burgundy marl
#  powder pink
#  dark mole
#  light sage green
#  light green
#  light grey-blue
#  basic black
#  dark beige marl
#  navy blue
#  pale denim grey
#  brick red
#  turquoise dark
#  metal light
#  old rose
#  pale blue
#  white marl
#  steel black
#  aubergine purple
#  dark orange
#  plum purple
#  khaki beige
#  beige
#  brown medium dusty
#  yellow bright
#  light purple
#  lilac purple light
#  white-blue
#  beige dark
#  light blue
#  dark blue
#  dark pink
#  pulp fiction
#  dusty blue
#  light brown marl
#  ivory
#  bright purple
#  natural white
#  green dark
#  light apricot
#  white dusty light
#  steel blue
#  turquoise-grey
#  washed black
#  green medium dusty
#  blue marl
#  deep blue
#  black
#  pale denim pink
#  dark khaki green
#  black dark
#  mustard yellow
#  pale orange
#  dark greige
#  burgundy
#  khaki green medium dusty
#  light greige
#  purple
#  true navy
#  light grey
#  denim black dark
#  vintage grey
#  dark brown marl
#  dusty pink
#  dark olive green
#  pale green-blue
#  green marl
#  dark petrol
#  denim purple
#  holographic
#  green bright
#  light dusty green
#  steel grey
#  burnt orange
#  blue dark
#  light turquoise
#  light mole
#  light beige
#  dark grey
#  bright blue
#  grey marl
#  teal
#  dusty khaki green
#  light khaki green
#  peach pink
#  dark green
#  denim beige
#  red dark
#  grey medium dusty
#  dark blue marl
#  dark purple
#  pale yellow
#  mole
#  vintage beige
#  navy
#  light dusty blue
#  acid green
#  mint green
#  bright yellow
#  dark brown
#  orange dark
#  blue light
#  dark blue-grey
#  bright green
#  brown
#  yellow
#  charcoal grey
#  whitw
#  dark denim grey
#  grass green
#  orange bright
#  multicolour
#  denim black
#  dark grey-green
#  beige marl
#  greige marl
#  dark yellow
#  pink light
#  orange
#  bronze-coloured
#  dark red
#  sky blue
#  transparent
#  klein blue
#  blue dusty light
#  denim green
#  mole dusty light
#  light mint green
#  neon yellow
#  light pink
#  turquoise dusty light
#  undefined undefined
#  grey melange medium dusty
#  light grey-green
#  salmon pink
#  yale
#  grey
#  neon green
#  cerise
#  grey dark
#  white
#  blue-purple
#  anthracite grey
#  red marl
#  turquoise medium dusty
#  fed red