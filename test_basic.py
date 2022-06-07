from unittest import TestCase,mock
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        self.boggle=Boggle()
        self.boggle_board= [   
                ['H','B',"C","D","E"],
                ['A','I',"C","D","E"],
                ['A','B',"M","D","E"],
                ['A','B',"C","D","E"],
                ['A','B',"C","D","E"],
            ]

    # def test_home(self):
    #     with self.client:
    #         res = self.client.get('/')
    #         self.assertIn('board', session)
    #         self.assertIn(b'Score:', res.data)
    #         self.assertIn(b'Seconds Left:', res.data)
    #         self.assertIsNone(session.get('highscore'))
    #         self.assertIsNone(session.get('numPlays'))

    # def test_invalid_words(self):
    #     self.client.get('/')
    #     res = self.client.get('/check-word?word=test')
    #     self.assertEqual(res.json['result'], 'not-on-board')

    # def test_non_english(self):
    #     self.client.get('/')
    #     res = self.client.get('/check-word?word=bonjour')
    #     self.assertEqual(res.json['result'], 'not-word')

    # thru the app
    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = self.boggle_board
            res = client.get('/check-word?word=him')
            self.assertEqual(res.json['result'], 'ok')
    
    #thru the functions of board
    def test_random(self):
        self.assertEqual(self.boggle.check_valid_word(self.boggle_board,"him"),"ok")
