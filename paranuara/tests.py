from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, APITestCase
from .models import Company, People
from food.models import Fruit, Vegetable
import datetime
from django.db import connections, DEFAULT_DB_ALIAS


# Create your tests here.
class SnippetTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        v1 = Vegetable.objects.create(name='BASIL')
        f1 = Fruit.objects.create(name='Apple')
        c1 = Company.objects.create(name='Test Company 1', index=0)
        c2 = Company.objects.create(name='Test Company 2', index=1)

        p1 = People.objects.create(
            index=0,
            company=c1,
            id='595eeb9c3b22f1556b4bda48',
            name="People 1",
            guid='fd047f66-fee7-41c1-953a-ba5836bfc66e',
            has_died=False,
            balance='$3,962.14',
            picture='http://placehold.it/32x32',
            age=52,
            eyeColor='brown',
            gender='Female',
            email='gomezbutler@earthmark.com',
            phone='+1 (961) 504-2654',
            address="631 Throop Avenue, Dunbar, Guam, 7469",
            about='Minim non anim irure esse ut adipisicing non anim laboris exercitation cupidatat duis veniam pariatur. Duis tempor ipsum in',
            registered=datetime.datetime.strptime(
                '2015-06-23T11:44:00 -10:00', "%Y-%m-%dT%H:%M:%S %z"),
            greeting="Hello, Gomez Butler! You have 5 unread messages.",
            tags=[
                "pariatur",
                "proident",
                "mollit",
                "proident",
                "ad",
                "commodo",
                "mollit"
            ],
        )
        p1.fruit.add(f1)
        p1.vegetable.add(v1)

        p2 = People.objects.create(
            id="595eeb9cf3bff1fca3b938a3",
            index=1,
            guid="e9f5a3ea-7765-4751-a059-2abd2c0201d6",
            has_died=False,
            balance="$1,823.99",
            picture="http://placehold.it/32x32",
            age=51,
            eyeColor="brown",
            name="Ana Wilkins",
            gender="Female",
            company=c1,
            email="anawilkins@earthmark.com",
            phone="+1 (897) 496-2673",
            address="894 Tehama Street, Urbana, Virgin Islands, 3323",
            about="Voluptate anim elit qui aute dolor enim ea. Cillum officia sunt enim do in officia exercitation id. Velit dolore duis anim ut non non anim aliqua aute cupidatat. Sint do commodo ullamco minim.\r\n",
            registered=datetime.datetime.strptime(
                "2016-10-24T12:55:36 -11:00", "%Y-%m-%dT%H:%M:%S %z"),
            greeting="Hello, Ana Wilkins! You have 1 unread messages.",
            tags=[
                "in",
                "do",
                "aute",
                "veniam",
                "irure",
                "duis",
                "aliquip"
            ]
        )
        p2.fruit.add(f1)
        p2.vegetable.add(v1)
        p2.friend.add(p1)

        p3 = People.objects.create(
            id="595eeb9c5de1191bdddaed6a",
            index=2,
            guid="b04d840a-1a8b-4311-b53e-8397eef8ea83",
            has_died=False,
            balance="$2,486.04",
            picture="http://placehold.it/32x32",
            age=49,
            eyeColor="brown",
            name="Elena Cummings",
            gender="Female",
            company=None,
            email="elenacummings@earthmark.com",
            phone="+1 (969) 424-3805",
            address="966 Newport Street, Coral, Kansas, 1233",
            about="Irure consequat exercitation sit ea culpa eu. Tempor occaecat dolor elit consequat deserunt. Non qui exercitation sint aliqua non esse ullamco.\r\n",
            registered=datetime.datetime.strptime(
                "2016-12-16T05:30:58 -11:00", "%Y-%m-%dT%H:%M:%S %z"),
            tags=[
                "eu",
                "eiusmod",
                "sunt",
                "sit",
                "labore",
                "consectetur",
                "nulla"
            ],
        )
        p3.fruit.add(f1)
        p3.vegetable.add(v1)
        p3.friend.add(p1, p2)

    def test_get_all_people_in_company(self):
        '''Test case to get all people in a company'''
        response = self.client.get('/company/0/peoples')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_no_people_in_company(self):
        '''Test case for no people in a company'''
        response = self.client.get('/company/1/peoples')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_people_detail(self):
        '''Test case for people detail API'''
        response = self.client.get('/people/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'People 1')

    def test_people_not_found(self):
        '''Test case for invalid index people detail API'''
        response = self.client.get('/people/10')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'].split('='), ['Not found.'])

    def test_common_friend(self):
        '''Test case to get common friend'''
        response = self.client.get('/common_friends/1/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['common_friends']), 1)

    def test_no_common_friend(self):
        '''Test case for no common friend'''
        response = self.client.get('/common_friends/0/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['common_friends']), 0)

    def test_common_friend_invalid_indexes(self):
        '''Test case for common friend invalid parameters'''
        response = self.client.get('/common_friends/1/1')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data['detail'].split('='), [
            'Index for people 1 and people 2 should be different!'])
