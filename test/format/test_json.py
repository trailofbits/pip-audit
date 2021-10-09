import json

import pip_audit.format as format


def test_json(vuln_data):
    json_format = format.JsonFormat(True)
    expected_json = [
        {
            "package": "foo",
            "version": "1.0",
            "vulns": [
                {
                    "id": "VULN-0",
                    "fix_versions": [
                        "1.1",
                        "1.4",
                    ],
                    "description": "The first vulnerability",
                },
                {
                    "id": "VULN-1",
                    "fix_versions": ["1.0"],
                    "description": "The second vulnerability",
                },
            ],
        },
        {
            "package": "bar",
            "version": "0.1",
            "vulns": [
                {"id": "VULN-2", "fix_versions": [], "description": "The third vulnerability"}
            ],
        },
    ]
    assert json_format.format(vuln_data) == json.dumps(expected_json)
