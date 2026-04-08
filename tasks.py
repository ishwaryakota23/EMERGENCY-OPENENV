tasks = [
    {
        "name": "easy_task",
        "input": {
            "request_text": "Person unconscious",
            "available_units": [
                {"id": "A1", "distance": 2},
                {"id": "A2", "distance": 5}
            ]
        },
        "expected": {
            "type": "medical",
            "severity": "critical",
            "assigned_unit": "A1"
        }
    },

    {
        "name": "medium_task",
        "input": {
            "request_text": "Fire in building",
            "available_units": [
                {"id": "F1", "distance": 3},
                {"id": "F2", "distance": 6}
            ]
        },
        "expected": {
            "type": "fire",
            "severity": "high",
            "assigned_unit": "F1"
        }
    },

    {
        "name": "hard_task",
        "input": {
            "request_text": "Accident with injuries",
            "available_units": [
                {"id": "A1", "distance": 5},
                {"id": "A2", "distance": 2}
            ]
        },
        "expected": {
            "type": "medical",
            "severity": "critical",
            "assigned_unit": "A2"
        }
    }
]
{
    "name": "extreme_task",
    "input": {
        "request_text": "Multiple accident victims, critical condition, limited ambulances",
        "available_units": [
            {"id": "A1", "distance": 10}
        ]
    },
    "expected": {
        "type": "medical",
        "severity": "critical",
        "assigned_unit": "A1"
    }
}