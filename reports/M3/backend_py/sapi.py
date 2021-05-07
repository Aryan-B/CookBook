from __future__ import print_function
import time
import spoonacular
from spoonacular.rest import ApiException
from pprint import pprint
import os
from flask import Flask,jsonify,Response,json, request
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
import cv2, torch
import numpy as np
import glob
from torch import nn
import torchvision.models as models
import pickle
import json

configuration = spoonacular.Configuration()
configuration.api_key['apiKey'] = 'de1b34dcfe874d82885c269c47708c22'

api_instance = spoonacular.DefaultApi(spoonacular.ApiClient(configuration))
# username = "dsky" # str | The username.
# hash = "4b5v4398573406" # str | The private hash for the username.
# inline_object11 = spoonacular.InlineObject11(username,hash) # InlineObject11 | 


sample_recipe= {'aggregateLikes': 37,
 'analyzedInstructions': [{'name': '',
                           'steps': [{'equipment': [{'id': 404645,
                                                     'image': 'pan.png',
                                                     'localizedName': 'frying '
                                                                      'pan',
                                                     'name': 'frying pan'},
                                                    {'id': 404794,
                                                     'image': 'oven.jpg',
                                                     'localizedName': 'stove',
                                                     'name': 'stove'}],
                                      'ingredients': [{'id': 4582,
                                                       'image': 'vegetable-oil.jpg',
                                                       'localizedName': 'cooking '
                                                                        'oil',
                                                       'name': 'cooking oil'}],
                                      'number': 1,
                                      'step': 'Brush the pan with oil and heat '
                                              'until hot. (350 on an electric '
                                              'skillet or medium high on the '
                                              'stove).'},
                                     {'equipment': [{'id': 404645,
                                                     'image': 'pan.png',
                                                     'localizedName': 'frying '
                                                                      'pan',
                                                     'name': 'frying pan'}],
                                      'ingredients': [{'id': 18364,
                                                       'image': 'flour-tortilla.jpg',
                                                       'localizedName': 'tortilla',
                                                       'name': 'tortilla'}],
                                      'number': 2,
                                      'step': 'Place tortillas on pan.'},
                                     {'equipment': [],
                                      'ingredients': [{'id': 18364,
                                                       'image': 'flour-tortilla.jpg',
                                                       'localizedName': 'tortilla',
                                                       'name': 'tortilla'},
                                                      {'id': 1041009,
                                                       'image': 'cheddar-cheese.png',
                                                       'localizedName': 'cheese',
                                                       'name': 'cheese'}],
                                      'number': 3,
                                      'step': 'Sprinkle 1 -2 tablespoons of '
                                              'cheese on each tortilla.'},
                                     {'equipment': [],
                                      'ingredients': [{'id': 5006,
                                                       'image': 'whole-chicken.jpg',
                                                       'localizedName': 'whole '
                                                                        'chicken',
                                                       'name': 'whole chicken'},
                                                      {'id': 1041009,
                                                       'image': 'cheddar-cheese.png',
                                                       'localizedName': 'cheese',
                                                       'name': 'cheese'}],
                                      'number': 4,
                                      'step': 'Place ~1/3 cup of barbecue '
                                              'chicken on top of the '
                                              'cheese.Top with 1 – 2 '
                                              'tablespoons of cheese.'},
                                     {'equipment': [],
                                      'ingredients': [{'id': 18364,
                                                       'image': 'flour-tortilla.jpg',
                                                       'localizedName': 'tortilla',
                                                       'name': 'tortilla'}],
                                      'length': {'number': 4,
                                                 'unit': 'minutes'},
                                      'number': 5,
                                      'step': 'Place another tortilla on top '
                                              'and press it down to evenly '
                                              'smush the ingredients between '
                                              'the tortillas.Cook until the '
                                              'bottom tortilla is brown. Flip '
                                              'and cook until the other '
                                              'tortilla is brown, '
                                              'approximately 3 -4 minutes each '
                                              'side.Repeat until all of your '
                                              'quesadillas have been made.'},
                                     {'equipment': [{'id': 404651,
                                                     'image': 'pizza-cutter.jpg',
                                                     'localizedName': 'pizza '
                                                                      'cutter',
                                                     'name': 'pizza cutter'}],
                                      'ingredients': [],
                                      'number': 6,
                                      'step': 'Cut in fourths with a pizza '
                                              'cutter and serve while hot.'}]}],
 'cheap': False,
 'cookingMinutes': 8,
 'creditsText': 'Premeditated Left Over',
 'cuisines': ['Mexican'],
 'dairyFree': False,
 'diets': ['gluten free'],
 'dishTypes': ['lunch', 'main course', 'main dish', 'dinner'],
 'extendedIngredients': [{'aisle': 'Cheese',
                          'amount': 1.5,
                          'consistency': 'solid',
                          'id': 1041009,
                          'image': 'cheddar-cheese.png',
                          'measures': {'metric': {'amount': 354.882,
                                                  'unitLong': 'milliliters',
                                                  'unitShort': 'ml'},
                                       'us': {'amount': 1.5,
                                              'unitLong': 'cups',
                                              'unitShort': 'cups'}},
                          'meta': [],
                          'metaInformation': [],
                          'name': 'cheese',
                          'nameClean': 'cheese',
                          'original': '1½ cups cheese',
                          'originalName': 'cheese',
                          'originalString': '1½ cups cheese',
                          'unit': 'cups'},
                         {'aisle': 'Meat',
                          'amount': 2.0,
                          'consistency': 'solid',
                          'id': 5006,
                          'image': 'whole-chicken.jpg',
                          'measures': {'metric': {'amount': 473.176,
                                                  'unitLong': 'milliliters',
                                                  'unitShort': 'ml'},
                                       'us': {'amount': 2.0,
                                              'unitLong': 'cups',
                                              'unitShort': 'cups'}},
                          'meta': ['shredded'],
                          'metaInformation': ['shredded'],
                          'name': 'chicken',
                          'nameClean': 'whole chicken',
                          'original': '2 cups shredded barbecue chicken',
                          'originalName': 'shredded barbecue chicken',
                          'originalString': '2 cups shredded barbecue chicken',
                          'unit': 'cups'},
                         {'aisle': 'Bakery/Bread;Pasta and Rice;Ethnic Foods',
                          'amount': 12.0,
                          'consistency': 'solid',
                          'id': 18364,
                          'image': 'flour-tortilla.jpg',
                          'measures': {'metric': {'amount': 12.0,
                                                  'unitLong': '',
                                                  'unitShort': ''},
                                       'us': {'amount': 12.0,
                                              'unitLong': '',
                                              'unitShort': ''}},
                          'meta': [],
                          'metaInformation': [],
                          'name': 'tortillas',
                          'nameClean': 'tortilla',
                          'original': '12 tortillas',
                          'originalName': 'tortillas',
                          'originalString': '12 tortillas',
                          'unit': ''}],
 'gaps': 'no',
 'glutenFree': True,
 'healthScore': 5.0,
 'id': 531683,
 'image': 'https://spoonacular.com/recipeImages/531683-556x370.jpg',
 'imageType': 'jpg',
 'instructions': 'Brush the pan with oil and heat until hot. (350 on an '
                 'electric skillet or medium high on the stove).Place '
                 'tortillas on pan.Sprinkle 1 -2 tablespoons of cheese on each '
                 'tortilla.Place ~1/3 cup of barbecue chicken on top of the '
                 'cheese.Top with 1 – 2 tablespoons of cheese.Place another '
                 'tortilla on top and press it down to evenly smush the '
                 'ingredients between the tortillas.Cook until the bottom '
                 'tortilla is brown. Flip and cook until the other tortilla is '
                 'brown, approximately 3 -4 minutes each side.Repeat until all '
                 'of your quesadillas have been made.Cut in fourths with a '
                 'pizza cutter and serve while hot.',
 'lowFodmap': False,
 'occasions': ["father's day"],
 'originalId': None,
 'preparationMinutes': 5,
 'pricePerServing': 68.0,
 'readyInMinutes': 13,
 'servings': 6,
 'sourceName': 'Premeditated Left Over',
 'sourceUrl': 'http://premeditatedleftovers.com/recipes-cooking-tips/barbecue-chicken-quesadillas/',
 'spoonacularScore': 49.0,
 'summary': 'Barbecue Chicken Quesadillas might be just the <b>Mexican</b> '
            'recipe you are searching for. This recipe makes 6 servings with '
            '<b>375 calories</b>, <b>19g of protein</b>, and <b>19g of fat</b> '
            'each. For <b>81 cents per serving</b>, this recipe <b>covers '
            '12%</b> of your daily requirements of vitamins and minerals. '
            "<b>Father's Day</b> will be even more special with this recipe. "
            'If you have cheese, barbecue chicken, tortillas, and a few other '
            'ingredients on hand, you can make it. To use up the cheese you '
            'could follow this main course with the <a '
            'href="https://spoonacular.com/recipes/the-bianca-dessert-grilled-cheese-586550">The '
            'Bianca Dessert Grilled Cheese</a> as a dessert. From preparation '
            'to the plate, this recipe takes around <b>13 minutes</b>. A few '
            'people made this recipe, and 37 would say it hit the spot. It is '
            "a good option if you're following a <b>gluten free and fodmap "
            "friendly</b> diet. It works well as a hor d'oeuvre. All things "
            'considered, we decided this recipe <b>deserves a spoonacular '
            'score of 52%</b>. This score is good. Try <a '
            'href="https://spoonacular.com/recipes/easy-barbecue-chicken-quesadillas-919303">Easy '
            'Barbecue Chicken Quesadillas</a>, <a '
            'href="https://spoonacular.com/recipes/barbecue-chicken-quesadillas-with-spinach-and-caramelized-onions-486618">Barbecue '
            'Chicken Quesadillas with Spinach and Caramelized Onions</a>, and '
            '<a '
            'href="https://spoonacular.com/recipes/barbecue-portobello-quesadillas-for-two-696527">Barbecue '
            'Portobello Quesadillas for Two</a> for similar recipes.',
 'sustainable': False,
 'title': 'Barbecue Chicken Quesadillas',
 'vegan': False,
 'vegetarian': False,
 'veryHealthy': False,
 'veryPopular': False,
 'weightWatcherSmartPoints': 11,
 'winePairing': {'pairedWines': ['pinot noir', 'riesling', 'sparkling rose'],
                 'pairingText': 'Pinot Noir, Riesling, and Sparkling rosé are '
                                'my top picks for Mexican. Acidic white wines '
                                'like riesling or low-tannin reds like pinot '
                                'noir can work well with Mexican dishes. '
                                'Sparkling rosé is a safe pairing too. The '
                                'White Oak Russian River Pinot Noir with a 4.5 '
                                'out of 5 star rating seems like a good match. '
                                'It costs about 20 dollars per bottle.',
                 'productMatches': [{'averageRating': 0.9,
                                     'description': 'A delicate Pinot Noir '
                                                    'with cranberry, '
                                                    'pomegranate and a slight '
                                                    'dusty, floral note on the '
                                                    'nose. Leads to a soft '
                                                    'entry on the palette, '
                                                    'followed by flavors of '
                                                    'boysenberry, plum and '
                                                    'leather, supported by '
                                                    'subtle and well '
                                                    'integrated oak. This wine '
                                                    'lingers at the finish '
                                                    'with velvety tannins.',
                                     'id': 448471,
                                     'imageUrl': 'https://spoonacular.com/productImages/448471-312x231.jpg',
                                     'link': 'https://click.linksynergy.com/deeplink?id=*QCiIS6t4gA&mid=2025&murl=https%3A%2F%2Fwww.wine.com%2Fproduct%2Fwhite-oak-russian-river-pinot-noir-2013%2F161568',
                                     'price': '$19.99',
                                     'ratingCount': 5.0,
                                     'score': 0.8375,
                                     'title': 'White Oak Russian River Pinot '
                                              'Noir'}]}}


sample_ingredient=[{'id': 1075071,
  'image': 'https://spoonacular.com/recipeImages/1075071-312x231.jpg',
  'imageType': 'jpg',
  'likes': 1,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Meat',
                         'amount': 1.0,
                         'extendedName': 'canned bacon',
                         'id': 10123,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/raw-bacon.png',
                         'meta': ["with mashed potatoes and corn and you're in "
                                  'business!'],
                         'metaInformation': ['with mashed potatoes and corn '
                                             "and you're in business!"],
                         'name': 'bacon',
                         'original': 'Bacon Wrapped Chicken – No one can '
                                     'resist this cheese stuffed, bacon '
                                     'wrapped chicken! Brush on some bbq sauce '
                                     'and serve with mashed potatoes and corn '
                                     "and you're in business!",
                         'originalName': 'Bacon Wrapped Chicken – No one '
                                         'resist this cheese stuffed, bacon '
                                         'wrapped chicken! Brush on some bbq '
                                         'sauce and serve with mashed potatoes '
                                         "and corn and you're in business",
                         'originalString': 'Bacon Wrapped Chicken – No one can '
                                           'resist this cheese stuffed, bacon '
                                           'wrapped chicken! Brush on some bbq '
                                           'sauce and serve with mashed '
                                           "potatoes and corn and you're in "
                                           'business!',
                         'unit': 'can',
                         'unitLong': 'can',
                         'unitShort': 'can'},
                        {'aisle': 'Pasta and Rice',
                         'amount': 1.0,
                         'extendedName': 'wild rice',
                         'id': 20444,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/uncooked-white-rice.png',
                         'meta': ['wild'],
                         'metaInformation': ['wild'],
                         'name': 'rice',
                         'original': 'Chicken & Wild Rice Casserole – Comfort '
                                     'food all the way! This recipe remind of '
                                     "of Sunday supper at my grandma's house.",
                         'originalName': 'Chicken & Wild Rice Casserole – '
                                         'Comfort food all the way! This '
                                         'recipe remind of of Sunday supper at '
                                         "my grandma's house",
                         'originalString': 'Chicken & Wild Rice Casserole – '
                                           'Comfort food all the way! This '
                                           'recipe remind of of Sunday supper '
                                           "at my grandma's house.",
                         'unit': 'serving',
                         'unitLong': 'serving',
                         'unitShort': 'serving'}],
  'title': '25 Chicken',
  'unusedIngredients': [],
  'usedIngredientCount': 2,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 1.0,
                       'extendedName': 'sweet chicken',
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['sweet',
                                'with rice or on a burger bun with lettuce!'],
                       'metaInformation': ['sweet',
                                           'with rice or on a burger bun with '
                                           'lettuce!'],
                       'name': 'chicken',
                       'original': 'Brown Sugar Pineapple Chicken – My '
                                   'favorite grilling recipe! I love the sweet '
                                   'glaze on this chicken and the pineapple is '
                                   'insanely good. Serve with rice or on a '
                                   'burger bun with lettuce!',
                       'originalName': 'Brown Sugar Pineapple Chicken – My '
                                       'favorite grilling recipe! I love the '
                                       'sweet glaze on this chicken and the '
                                       'pineapple is insanely good. Serve with '
                                       'rice or on a burger bun with lettuce',
                       'originalString': 'Brown Sugar Pineapple Chicken – My '
                                         'favorite grilling recipe! I love the '
                                         'sweet glaze on this chicken and the '
                                         'pineapple is insanely good. Serve '
                                         'with rice or on a burger bun with '
                                         'lettuce!',
                       'unit': 'serving',
                       'unitLong': 'serving',
                       'unitShort': 'serving'},
                      {'aisle': 'Meat',
                       'amount': 1.0,
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': [],
                       'metaInformation': [],
                       'name': 'chicken',
                       'original': 'Sheet Pan Chicken Fajitas – Easiest '
                                   'fajitas ever! Chop eveything up, toss in '
                                   'seasoning, and bake until done. Just add '
                                   'tortillas!',
                       'originalName': 'Pan Chicken Fajitas – Easiest fajitas '
                                       'ever! Chop eveything up, toss in '
                                       'seasoning, and bake until done. Just '
                                       'add tortillas',
                       'originalString': 'Sheet Pan Chicken Fajitas – Easiest '
                                         'fajitas ever! Chop eveything up, '
                                         'toss in seasoning, and bake until '
                                         'done. Just add tortillas!',
                       'unit': 'Sheet',
                       'unitLong': 'Sheet',
                       'unitShort': 'Sheet'}]},
 {'id': 559886,
  'image': 'https://spoonacular.com/recipeImages/559886-312x231.jpg',
  'imageType': 'jpg',
  'likes': 6042,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Bakery/Bread',
                         'amount': 8.0,
                         'id': 18064,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/white-bread.jpg',
                         'meta': ['your favorite'],
                         'metaInformation': ['your favorite'],
                         'name': 'bread',
                         'original': '8 slices of your favorite bread',
                         'originalName': 'your favorite bread',
                         'originalString': '8 slices of your favorite bread',
                         'unit': 'slices',
                         'unitLong': 'slices',
                         'unitShort': 'slice'},
                        {'aisle': 'Cheese',
                         'amount': 4.0,
                         'id': 93838,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/taleggio-cheese.jpg',
                         'meta': [],
                         'metaInformation': [],
                         'name': 'havarti cheese',
                         'original': '4 thicker slices of havarti cheese',
                         'originalName': 'thicker slices of havarti cheese',
                         'originalString': '4 thicker slices of havarti cheese',
                         'unit': '',
                         'unitLong': '',
                         'unitShort': ''}],
  'title': 'Chicken Fajita Sandwiches',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 4.0,
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['for recipe'],
                       'metaInformation': ['for recipe'],
                       'name': 'chicken',
                       'original': 'chicken fajitas, click for recipe',
                       'originalName': 'chicken fajitas, click for recipe',
                       'originalString': 'chicken fajitas, click for recipe',
                       'unit': 'servings',
                       'unitLong': 'servings',
                       'unitShort': 'servings'}]},
 {'id': 510869,
  'image': 'https://spoonacular.com/recipeImages/510869-312x231.jpg',
  'imageType': 'jpg',
  'likes': 3187,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Canned and Jarred',
                         'amount': 8.0,
                         'id': 6970,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/chicken-broth.png',
                         'meta': ['low sodium'],
                         'metaInformation': ['low sodium'],
                         'name': 'low sodium chicken broth',
                         'original': '8 cups chicken broth, low sodium',
                         'originalName': 'chicken broth, low sodium',
                         'originalString': '8 cups chicken broth, low sodium',
                         'unit': 'cups',
                         'unitLong': 'cups',
                         'unitShort': 'cup'},
                        {'aisle': 'Produce',
                         'amount': 0.25,
                         'id': 11291,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/spring-onions.jpg',
                         'meta': [],
                         'metaInformation': [],
                         'name': 'scallions',
                         'original': '1/4 cup scallions',
                         'originalName': 'scallions',
                         'originalString': '1/4 cup scallions',
                         'unit': 'cup',
                         'unitLong': 'cups',
                         'unitShort': 'cup'}],
  'title': 'Chicken Potsticker Soup',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 21.0,
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['(16 oz pkg.)'],
                       'metaInformation': ['(16 oz pkg.)'],
                       'name': 'chicken',
                       'original': '21 chicken potstickers (16 oz pkg.)',
                       'originalName': 'chicken potstickers (16 oz pkg.)',
                       'originalString': '21 chicken potstickers (16 oz pkg.)',
                       'unit': '',
                       'unitLong': '',
                       'unitShort': ''}]},
 {'id': 574737,
  'image': 'https://spoonacular.com/recipeImages/574737-312x231.jpg',
  'imageType': 'jpg',
  'likes': 1974,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Produce',
                         'amount': 3.0,
                         'id': 2063,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/rosemary.jpg',
                         'meta': ['fresh'],
                         'metaInformation': ['fresh'],
                         'name': 'fresh rosemary',
                         'original': '3 sprigs of fresh rosemary',
                         'originalName': 'fresh rosemary',
                         'originalString': '3 sprigs of fresh rosemary',
                         'unit': 'sprigs',
                         'unitLong': 'sprigs',
                         'unitShort': 'sprigs'},
                        {'aisle': 'Alcoholic Beverages',
                         'amount': 12.0,
                         'extendedName': 'white wine',
                         'id': 14084,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/red-wine.jpg',
                         'meta': ['white'],
                         'metaInformation': ['white'],
                         'name': 'wine',
                         'original': '12 oz. bottle of white wine and herb '
                                     'marinade',
                         'originalName': 'white wine and herb marinade',
                         'originalString': '12 oz. bottle of white wine and '
                                           'herb marinade',
                         'unit': 'oz',
                         'unitLong': 'ounces',
                         'unitShort': 'oz'}],
  'title': 'Garlic Herb Crock Pot Chicken',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 5.0,
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['whole'],
                       'metaInformation': ['whole'],
                       'name': 'whole chicken',
                       'original': '5-6lbs. of whole chicken',
                       'originalName': 'whole chicken',
                       'originalString': '5-6lbs. of whole chicken',
                       'unit': 'lbs',
                       'unitLong': 'pounds',
                       'unitShort': 'lb'}]},
 {'id': 74358,
  'image': 'https://spoonacular.com/recipeImages/74358-312x231.jpg',
  'imageType': 'jpg',
  'likes': 242,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Produce',
                         'amount': 1.0,
                         'extendedName': 'whole garlic cloves',
                         'id': 11215,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/garlic.png',
                         'meta': ['whole', 'peeled'],
                         'metaInformation': ['whole', 'peeled'],
                         'name': 'garlic cloves',
                         'original': 'OPTIONAL Whole garlic cloves, peeled',
                         'originalName': 'OPTIONAL Whole garlic , peeled',
                         'originalString': 'OPTIONAL Whole garlic cloves, '
                                           'peeled',
                         'unit': 'cloves',
                         'unitLong': 'clove',
                         'unitShort': 'cloves'},
                        {'aisle': 'Produce',
                         'amount': 1.0,
                         'extendedName': 'fresh herbs',
                         'id': 1002044,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/lemon-basil.jpg',
                         'meta': ['fresh'],
                         'metaInformation': ['fresh'],
                         'name': 'herbs',
                         'original': 'OPTIONAL Fresh herbs',
                         'originalName': 'OPTIONAL Fresh herbs',
                         'originalString': 'OPTIONAL Fresh herbs',
                         'unit': 'serving',
                         'unitLong': 'serving',
                         'unitShort': 'serving'}],
  'title': 'rotisserie” Chicken',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 1.0,
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['whole'],
                       'metaInformation': ['whole'],
                       'name': 'whole chicken',
                       'original': '1 whole chicken, small enough to fit in '
                                   'your slow cooker',
                       'originalName': 'whole chicken, small enough to fit in '
                                       'your slow cooker',
                       'originalString': '1 whole chicken, small enough to fit '
                                         'in your slow cooker',
                       'unit': 'small',
                       'unitLong': 'small',
                       'unitShort': 'small'}]},
 {'id': 1156204,
  'image': 'https://spoonacular.com/recipeImages/1156204-312x231.jpg',
  'imageType': 'jpg',
  'likes': 1,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Milk, Eggs, Other Dairy',
                         'amount': 2.0,
                         'id': 1001,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg',
                         'meta': ['softened'],
                         'metaInformation': ['softened'],
                         'name': 'butter',
                         'original': '2 tbsp butter softened',
                         'originalName': 'butter softened',
                         'originalString': '2 tbsp butter softened',
                         'unit': 'tbsp',
                         'unitLong': 'tablespoons',
                         'unitShort': 'Tbsp'},
                        {'aisle': 'Spices and Seasonings',
                         'amount': 2.0,
                         'id': 1012034,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/seasoning.png',
                         'meta': [],
                         'metaInformation': [],
                         'name': 'rub',
                         'original': "2 tbsp Trader Joe's BBQ Rub and "
                                     'Seasoning or bbq rub',
                         'originalName': "Trader Joe's BBQ Rub and Seasoning "
                                         'or bbq rub',
                         'originalString': "2 tbsp Trader Joe's BBQ Rub and "
                                           'Seasoning or bbq rub',
                         'unit': 'tbsp',
                         'unitLong': 'tablespoons',
                         'unitShort': 'Tbsp'}],
  'title': 'Air Fryer Whole Chicken',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 1.0,
                       'extendedName': 'whole chicken',
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['whole'],
                       'metaInformation': ['whole'],
                       'name': 'chicken',
                       'original': '1 whole chicken about 3-5 pounds',
                       'originalName': 'whole chicken about 3-5 pounds',
                       'originalString': '1 whole chicken about 3-5 pounds',
                       'unit': '',
                       'unitLong': '',
                       'unitShort': ''}]},
 {'id': 394088,
  'image': 'https://spoonacular.com/recipeImages/394088-312x231.jpg',
  'imageType': 'jpg',
  'likes': 0,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Produce',
                         'amount': 22.0,
                         'extendedName': 'whole green onion tops',
                         'id': 11291,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/spring-onions.jpg',
                         'meta': ['whole'],
                         'metaInformation': ['whole'],
                         'name': 'green onion tops',
                         'original': 'Whole chives or green onion tops',
                         'originalName': 'Whole chives or green onion tops',
                         'originalString': 'Whole chives or green onion tops',
                         'unit': 'servings',
                         'unitLong': 'servings',
                         'unitShort': 'servings'},
                        {'aisle': 'Gluten Free',
                         'amount': 16.0,
                         'id': 18069,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/white-bread.jpg',
                         'meta': ['white', 'thin'],
                         'metaInformation': ['white', 'thin'],
                         'name': 'white sandwich bread',
                         'original': '1 loaf (16 ounces) thin white sandwich '
                                     'bread, crusts removed',
                         'originalName': 'loaf thin white sandwich bread, '
                                         'crusts removed',
                         'originalString': '1 loaf (16 ounces) thin white '
                                           'sandwich bread, crusts removed',
                         'unit': 'ounces',
                         'unitLong': 'ounces',
                         'unitShort': 'oz'}],
  'title': 'Diploma Sandwiches',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 2.0,
                       'extendedName': 'cooked chicken',
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['prepared'],
                       'metaInformation': ['prepared'],
                       'name': 'chicken',
                       'original': '2 cups prepared ham, tuna or chicken salad',
                       'originalName': 'prepared ham, tuna or chicken salad',
                       'originalString': '2 cups prepared ham, tuna or chicken '
                                         'salad',
                       'unit': 'cups',
                       'unitLong': 'cups',
                       'unitShort': 'cup'}]},
 {'id': 386635,
  'image': 'https://spoonacular.com/recipeImages/386635-312x231.jpg',
  'imageType': 'jpg',
  'likes': 0,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Pasta and Rice',
                         'amount': 8.8,
                         'id': 20040,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/uncooked-brown-rice.png',
                         'meta': ['ready-to-serve'],
                         'metaInformation': ['ready-to-serve'],
                         'name': 'brown rice',
                         'original': '1 package (8.8 ounces) ready-to-serve '
                                     'brown rice',
                         'originalName': 'package ready-to-serve brown rice',
                         'originalString': '1 package (8.8 ounces) '
                                           'ready-to-serve brown rice',
                         'unit': 'ounces',
                         'unitLong': 'ounces',
                         'unitShort': 'oz'},
                        {'aisle': 'Nuts;Savory Snacks',
                         'amount': 3.0,
                         'id': 12585,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/cashews.jpg',
                         'meta': ['salted'],
                         'metaInformation': ['salted'],
                         'name': 'salted cashews',
                         'original': '3 tablespoons salted cashews',
                         'originalName': 'salted cashews',
                         'originalString': '3 tablespoons salted cashews',
                         'unit': 'tablespoons',
                         'unitLong': 'tablespoons',
                         'unitShort': 'Tbsp'}],
  'title': 'Quick Sweet-and-Sour Chicken',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 13.2,
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': [],
                       'metaInformation': [],
                       'name': 'chicken',
                       'original': '1 package (13.2 ounces) breaded chicken '
                                   'nuggets',
                       'originalName': 'package breaded chicken nuggets',
                       'originalString': '1 package (13.2 ounces) breaded '
                                         'chicken nuggets',
                       'unit': 'ounces',
                       'unitLong': 'ounces',
                       'unitShort': 'oz'}]},
 {'id': 133849,
  'image': 'https://spoonacular.com/recipeImages/133849-312x231.jpg',
  'imageType': 'jpg',
  'likes': 0,
  'missedIngredientCount': 2,
  'missedIngredients': [{'aisle': 'Spices and Seasonings;Baking',
                         'amount': 2.0,
                         'id': 2033,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/poppyseed.png',
                         'meta': [],
                         'metaInformation': [],
                         'name': 'poppy seeds',
                         'original': '2 tablespoons poppy seeds',
                         'originalName': 'poppy seeds',
                         'originalString': '2 tablespoons poppy seeds',
                         'unit': 'tablespoons',
                         'unitLong': 'tablespoons',
                         'unitShort': 'Tbsp'},
                        {'aisle': 'Refrigerated',
                         'amount': 8.0,
                         'extendedName': 'canned refrigerated crescent rolls',
                         'id': 93618,
                         'image': 'https://spoonacular.com/cdn/ingredients_100x100/crescent-roll-dough.png',
                         'meta': ['refrigerated', 'canned'],
                         'metaInformation': ['refrigerated', 'canned'],
                         'name': 'refrigerated crescent rolls',
                         'original': '1 (8-oz.) can refrigerated crescent '
                                     'rolls',
                         'originalName': 'refrigerated crescent rolls',
                         'originalString': '1 (8-oz.) can refrigerated '
                                           'crescent rolls',
                         'unit': 'oz',
                         'unitLong': 'ounces',
                         'unitShort': 'oz'}],
  'title': 'Chicken Salad Crescent Rolls',
  'unusedIngredients': [],
  'usedIngredientCount': 1,
  'usedIngredients': [{'aisle': 'Meat',
                       'amount': 1.0,
                       'id': 5006,
                       'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
                       'meta': ['your favorite'],
                       'metaInformation': ['your favorite'],
                       'name': 'chicken',
                       'original': '1 cup your favorite chicken salad',
                       'originalName': 'your favorite chicken salad',
                       'originalString': '1 cup your favorite chicken salad',
                       'unit': 'cup',
                       'unitLong': 'cup',
                       'unitShort': 'cup'}]}]


UPLOAD_FOLDER = './store/'

app = Flask(__name__,template_folder='template',static_url_path='/',static_folder='./')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


with open('classes.txt') as f:
        label = list(map(lambda x:x.strip(), f.readlines()))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(DEVICE)
model = torch.load('model.pht').to(DEVICE)
            
@app.route('/recognise', methods=['POST'])
def recognise():
    data=dict(request.files)
    dataresult=[]
    for key in data:
        path = os.path.join(app.config['UPLOAD_FOLDER'], data[key].filename)
        print(data[key])
        data[key].save(path)

        try:
            img = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img, (224, 224))
            img = np.transpose(img, axes=[2, 0, 1]) / 255.0
            img = np.expand_dims(img, axis=0)
            img = torch.from_numpy(img).to(DEVICE).float()
            pred = np.argmax(model(img).cpu().detach().numpy()[0])
            print('Image Path:{}, Pred Class:{}'.format(path, label[pred]))
            dataresult.append({'name':label[pred], 'type':'string'})
        except:
            print('Error, Try Again!')
    for f in os.listdir('./store'):
        os.remove(os.path.join('./store', f))
    return jsonify(dataresult)

@app.route('/ingredients',methods=['POST'])
def ingredients():
    datas = json.loads((request.data.decode("ascii")))
    query=[]
    for x in datas:
        query.append(x['name'])
    query_string=','.join(query)
    print(query_string)
    # try:
    #     api_response = api_instance.search_recipes_by_ingredients(query_string,number=9)
    #     pprint(api_response)
    # except ApiException as e:
    #     print("Exception when calling DefaultApi->add_to_meal_plan: %s\n" % e)
    return Response(json.dumps(sample_ingredient),mimetype='application/json')
    
@app.route('/recipe',methods=['POST'])
def recipe():
    pprint(request.data.decode("ascii"))
    datas = json.loads(request.data.decode("ascii"))
    # # # print(type(datas))
    # # print(request.data)
    # query=[]
    # for x in datas:
    #     # print(x)
    #     # print(type(x))
    #     query.append(x['id'])
    query_string=str(datas['id'])
    print(query_string)
    # return jsonify({'name':'Success','id':'12345'})
    # try:
    #     api_response = api_instance.get_recipe_information(query_string)
    #     pprint(api_response)
    # except ApiException as e:
    #     print("Exception when calling DefaultApi->add_to_meal_plan: %s\n" % e)
    return Response(json.dumps(sample_recipe),mimetype='application/json')




if __name__ == '__main__':
       app.run(host="0.0.0.0", port=8080)
       
