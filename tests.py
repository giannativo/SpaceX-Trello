from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)

BOARD_LABELS = [{'id': '1', 'name': 'label_1'}, {'id': '2', 'name': 'label_2'}]


def test_wrong_task_type_should_return_bad_request():
    response = client.post('/', json={'type': 'deploy'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'The task type is not valid or is missing'}


def test_issue_without_title_and_description_should_return_bad_request():
    response = client.post('/', json={'type': 'issue'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'The issue should have a title and a description'}


def test_issue_with_title_and_description_is_created_correctly(mocker):
    expected_issue = {'id': '1',
                      'name': 'Send Message',
                      'desc': 'Let pilots send messages to Central'}
    mocker.patch('main.add_card_to_list', return_value=expected_issue)
    response = client.post('/', json={
        'type': 'issue',
        'title': 'Send Message',
        'description': 'Let pilots send messages to Central'
    })
    assert response.status_code == 200
    assert response.json() == expected_issue


def test_bug_without_description_should_return_bad_request():
    response = client.post('/', json={'type': 'bug'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'The bug should have a description'}


def test_bug_with_description_is_created_correctly(mocker):
    expected_bug_title = 'bug-hellothere-1234'
    expected_board_members = [{'id': '1', 'name': 'kenobi'}]
    expected_bug_label = {'id': '1', 'name': 'bug'}
    expected_bug = {'id': '1',
                    'name': expected_bug_title,
                    'desc': 'Cockpit is not depressurizing correctly',
                    'labels': [expected_bug_label],
                    'idMembers': ['1']}
    mocker.patch('main.get_bug_title', return_value=expected_bug_title)
    mocker.patch('main.get_or_create_label', return_value=expected_bug_label)
    mocker.patch('main.get_board_members', return_value=expected_board_members)
    mocker.patch('main.add_card_to_list', return_value=expected_bug)
    response = client.post('/', json={
        'type': 'bug',
        'description': 'Cockpit is not depressurizing correctly'
    })
    assert response.status_code == 200
    assert response.json() == expected_bug


def test_task_without_title_and_category_should_return_bad_request():
    response = client.post('/', json={'type': 'task'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'The task should have a title and a category'}


def test_task_with_title_and_category_is_created_correctly(mocker):
    expected_task_label = {'id': '1', 'name': 'Maintenance'}
    expected_task = {'id': '1', 'name': 'Clean the Rocket', 'labels': [expected_task_label]}
    mocker.patch('main.get_or_create_label', return_value=expected_task_label)
    mocker.patch('main.add_card_to_list', return_value=expected_task)
    response = client.post('/', json={
        'type': 'task',
        'title': 'Clean the Rocket',
        'category': 'Maintenance'
    })
    assert response.status_code == 200
    assert response.json() == expected_task


def test_an_existent_board_label_is_returned_if_an_existent_label_name_is_passed(mocker):
    mocker.patch('main.get_board_labels', return_value=BOARD_LABELS)
    expected_label = {'id': '1', 'name': 'label_1'}
    label = main.get_or_create_label('label_1')
    assert label == expected_label


def test_a_new_board_label_is_returned_if_a_non_existent_label_name_is_passed(mocker):
    mocker.patch('main.get_board_labels', return_value=BOARD_LABELS)
    expected_label = {'id': '3', 'name': 'label_3'}
    mocker.patch('main.create_board_label', return_value=expected_label)
    label = main.get_or_create_label('label_3')
    assert label == expected_label
