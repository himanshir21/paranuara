from django.core.management.base import BaseCommand
from paranuara.models import Company, People
from food.models import Vegetable, Fruit
import json
import logging
import os
import traceback
import datetime
from django.core.exceptions import ObjectDoesNotExist

fruits = ['APPLE', 'APRICOT', 'BANANA', 'BLUEBERRY', 'CHERRY', 'GRAPES',
          'GUAVA', 'LEMON', 'LIME', 'MANGO', 'MELON', 'ORANGE', 'PAPAYA',
          'PEAR', 'PERSIMMON', 'PINEAPPLE', 'RASPBERRY', 'STRAWBERRY',
          'TOMATO', 'WATERMELON']

vegetables = ['ACORN SQUASH', 'ALFALFA SPROUT', 'AMARANTH', 'ANISE',
              'ARTICHOKE', 'ARUGULA', 'ASPARAGUS', 'AUBERGINE', 'AZUKI BEAN',
              'BANANA SQUASH', 'BASIL', 'BEAN SPROUT', 'BEET', 'BEETROOT',
              'BLACK BEAN', 'BLACK-EYED PEA', 'BOK CHOY', 'BORLOTTI BEAN',
              'BROAD BEANS', 'BROCCOFLOWER', 'BROCCOLI', 'BRUSSELS SPROUT',
              'BUTTERNUT SQUASH', 'CABBAGE', 'CALABRESE', 'CARAWAY', 'CARROT',
              'CAULIFLOWER', 'CAYENNE PEPPER', 'CELERIAC', 'CELERY',
              'CHAMOMILE', 'CHARD', 'CHAYOTE', 'CHICKPEA', 'CHIVES',
              'CILANTRO', 'COLLARD GREEN', 'CORN', 'CORN SALAD', 'COURGETTE',
              'CUCUMBER', 'DAIKON', 'DELICATA', 'DILL', 'EGGPLANT', 'ENDIVE',
              'FENNEL', 'FIDDLEHEAD', 'FRISEE', 'GARLIC', 'GEM SQUASH',
              'GINGER', 'GREEN BEAN', 'GREEN PEPPER', 'HABANERO',
              'HERBS AND SPICE', 'HORSERADISH', 'HUBBARD SQUASH', 'JALAPENO',
              'JERUSALEM ARTICHOKE', 'JICAMA', 'KALE', 'KIDNEY BEAN',
              'KOHLRABI', 'LAVENDER', 'LEEK ', 'LEGUME', 'LEMON GRASS',
              'LENTILS', 'LETTUCE', 'LIMA BEAN', 'MAMEY', 'MANGETOUT',
              'MARJORAM', 'MUNG BEAN', 'MUSHROOM', 'MUSTARD GREEN',
              'NAVY BEAN', 'NEW ZEALAND SPINACH', 'NOPALE', 'OKRA', 'ONION',
              'OREGANO', 'PAPRIKA', 'PARSLEY', 'PARSNIP', 'PATTY PAN', 'PEA',
              'PINTO BEAN', 'POTATO', 'PUMPKIN', 'RADICCHIO', 'RADISH',
              'RHUBARB', 'ROSEMARY', 'RUNNER BEAN', 'RUTABAGA', 'SAGE',
              'SCALLION', 'SHALLOT', 'SKIRRET', 'SNAP PEA', 'SOY BEAN',
              'SPAGHETTI SQUASH', 'SPINACH', 'SQUASH', 'SWEET POTATO',
              'TABASCO PEPPER', 'TARO', 'TAT SOI', 'THYME', 'TOPINAMBUR',
              'TUBERS', 'TURNIP', 'WASABI', 'WATER CHESTNUT', 'WATERCRESS',
              'WHITE RADISH', 'YAM', 'ZUCCHINI']


class Command(BaseCommand):
    help = 'Sync companies and peoples from their respective JSON files'

    def handle(self, *args, **kwargs):
        """
        This functions process companies.json and people.json from resources dir.
        Massage the JSONs and store them in respective tables
        """
        # Processing companies.json ..
        try:
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir,
                                     '../../../resources/companies.json')
            with open(file_path, 'r') as f:
                cmp_json = json.load(f)
                for item in cmp_json:
                    obj, created = Company.objects.get_or_create(
                        index=item.get('index'), name=item.get('company'))
                    if created:
                        logging.info("New company added : {}".format(
                            item.get('company')))
        except Exception as err:
            logging.error("Failed to load companies : {}".format(err))

        # Processing people.json ..
        try:
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir,
                                     '../../../resources/people.json')
            with open(file_path, 'r') as f:
                people_json = json.load(f)
                for people in people_json:
                    try:
                        c = Company.objects.get(index=people.get('company_id'))
                    except ObjectDoesNotExist:
                        c = None
                    p = People(
                        index=people.get('index'),
                        company=c,
                        id=people.get('_id'),
                        name=people.get('name'),
                        guid=people.get('guid'),
                        has_died=people.get('has_died'),
                        balance=people.get('balance'),
                        picture=people.get('picture'),
                        age=people.get('age'),
                        eyeColor=people.get('eyeColor'),
                        gender=people.get('gender').capitalize(),
                        email=people.get('email'),
                        phone=people.get('phone'),
                        address=people.get('address'),
                        about=people.get('about'),
                        registered=datetime.datetime.strptime(
                            people.get('registered'), "%Y-%m-%dT%H:%M:%S %z"),
                        greeting=people.get('greeting'),
                        tags=people.get('tags')
                    )
                    p.save()
                    # Storing fruits and vegetables for the person
                    for item in people.get('favouriteFood', []):
                        item = item.upper()
                        if item in fruits:
                            fruit, created = Fruit.objects.get_or_create(
                                name=item)
                            p.fruit.add(fruit)
                        elif item in vegetables:
                            vegetable, created = Vegetable.objects.get_or_create(
                                name=item)
                            p.vegetable.add(vegetable)
                        else:
                            logging.error(
                                "No preset data found for food : {}".format(
                                    item))
                    p.save()

                # Processing and storing friends for the person
                for people in people_json:
                    p = People.objects.get(index=people.get('index'))
                    friends_list = []
                    for friend_index in people.get('friends'):
                        try:
                            friend = People.objects.get(
                                index=friend_index['index'])
                            friends_list.append(friend)
                        except ObjectDoesNotExist:
                            logging.error(
                                "No friend found with index {}".format(value))
                    p.friend.add(*friends_list)
        except Exception as err:
            logging.error("Failed to load people : {}".format(err))
