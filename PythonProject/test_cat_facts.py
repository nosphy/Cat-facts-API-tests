import json
import pytest
import requests

ENDPOINT = "https://meowfacts.herokuapp.com/"
#test to see if the endpoint can be accessed
def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

#test to see if the fact retrieved is different every time you access the API (risk of retrieving the same fact twice is low enough)
def test_random_fact_retrieved():
    response1 = requests.get(ENDPOINT)
    response2 = requests.get(ENDPOINT)
    data1 = response1.json()
    data2 = response2.json()
    assert data1 != data2
    print(data1)
    print(data2)

#test to see if you can retrieve a specific fact if you know the id of that fact
@pytest.mark.parametrize("id , fact",[
    ("?id=3",'{"data":["Mother cats teach their kittens to use the litter box."]}'),
    ("?id=4",'{"data":["The way you treat kittens in the early stages of it'"'s life will render it'"'s personality traits later in life."]}'),
    ("?id=5",'{"data":["Contrary to popular belief, the cat is a social animal. A pet cat will respond and answer to speech , and seems to enjoy human companionship."]}'),
])
def test_can_retrieve_specific_fact_by_id(id , fact):
    response_specific = requests.get(ENDPOINT + id)
    assert response_specific.text == fact

#test to see if you can retrieve multiple facts at once
@pytest.mark.parametrize("number_of_facts , array_length",[
    ("?count=3", 3),
    ("?count=4", 4),
    ("?count=5", 5),
])
def test_can_retrieve_multiple_facts(number_of_facts , array_length):
    response_multiple = requests.get(ENDPOINT + number_of_facts)
    data_multiple = response_multiple.json()
    data_array = json.loads(response_multiple.text)
    print(data_multiple)
    assert len(data_array['data']) == array_length

#test to see if you can retrieve a specific fact localised in the supported languages
@pytest.mark.parametrize("language , translated_fact",[
    ("?lang=esp&id=3", '{"data":["Las gatas madre enseñan a sus gatitos a usar la caja de arena."]}'),
    ("?lang=ger&id=3", '{"data":["Die Katzenmutter bringt ihren Kitten bei das Katzenklo zu verwenden"]}'),
    ("?lang=fil&id=3", '{"data":["Tinuturuan ng mga ina ang kanilang mga alagang kuting na gumamit ng litter box."]}'),
    ("?lang=zho&id=3", '{"data":["貓媽媽會教小貓如何使用貓砂盤。"]}')
])
def test_can_retrieve_facts_by_language(language , translated_fact):
    response_language = requests.get(ENDPOINT + language)
    assert response_language.text == translated_fact