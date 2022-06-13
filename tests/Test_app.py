import pytest
import requests

class TestQuestions:
    @classmethod
    def setup_class(cls):
        print('\nSetup Class')

    @classmethod
    def teardown_class(cls):
        print("\nTearing Down Class")

    def test_get_question_1(self):
        response = requests.get('http://localhost:5008/Q1')
        assert response.status_code == 200
    def test_get_question_2(self):
        response = requests.get('http://localhost:5008/Q2')
        assert response.status_code == 200
    def test_get_question_3(self):
        response = requests.get('http://localhost:5008/Q3')
        assert response.status_code == 200
    def test_get_question_4(self):
        response = requests.get('http://localhost:5008/Q4')
        assert response.status_code == 200
    def test_get_question_5(self):
        response = requests.get('http://localhost:5008/Q5')
        assert response.status_code == 200
    def test_get_question_6(self):
        response = requests.get('http://localhost:5008/Q6')
        assert response.status_code == 200
    def test_get_question_7(self):
        response = requests.get('http://localhost:5008/Q7')
        assert response.status_code == 200
    def test_get_question_8(self):
        response = requests.get('http://localhost:5008/Q8')
        assert response.status_code == 200
    def test_get_question_10(self):
        response = requests.get('http://localhost:5008/Q10')
        assert response.status_code == 200




