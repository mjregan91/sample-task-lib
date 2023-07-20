import requests


def test_example_ground_task(endpoint, ground_task):
    ground_task["X-Quindar-Task"] = "example.py"
    parameters = {"required_parameter": "foo", "required_int": 3}

    response = requests.request("POST", endpoint, headers=ground_task, json=parameters)

    # test expectations
    print(response.text)
