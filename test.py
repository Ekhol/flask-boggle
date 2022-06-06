from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Seconds Left:', res.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numPlays'))

    def test_invalid_words(self):
        self.client.get('/')
        res = self.client.get('/check-word?word=test')
        self.assertEqual(res.json['result'], 'not-on-board')

    def test_non_english(self):
        self.client.get('/')
        res = self.client.get('/check-word?word=bonjour')
        self.assertEqual(res.json['result'], 'not-word')

    def test_valid_word(self):
        with self.client as client:
            # need extra assistance here - do I need to build an entire table to test with?
