DUNE_API_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "execution_id": {"type": ["string", "null"]},
        "query_id": {"type": ["integer", "null"]},
        "state": {
            "type": "string",
            "enum": ["QUERY_STATE_COMPLETED"]
        },
        "submitted_at": {"type": ["string", "null"], "format": "date-time"},
        "expires_at": {"type": ["string", "null"], "format": "date-time"},
        "execution_started_at": {"type": ["string", "null"], "format": "date-time"},
        "execution_ended_at": {"type": ["string", "null"], "format": "date-time"},
        "result": {
            "type": "object",
            "properties": {
                "rows": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "Current": {"type": ["number"]},
                            "High_180d": {"type": ["number", "null"]},
                            "High_30d": {"type": ["number", "null"]},
                            "High_7d": {"type": ["number", "null"]},
                            "Low_180d": {"type": ["number", "null"]},
                            "Low_30d": {"type": ["number", "null"]},
                            "Low_7d": {"type": ["number", "null"]},
                            "MA_10d": {"type": ["number", "null"]},
                            "MA_200d": {"type": ["number", "null"]},
                            "MA_50d": {"type": ["number", "null"]},
                            "Performance_180d": {"type": ["number", "null"]},
                            "Performance_30d": {"type": ["number", "null"]},
                            "Performance_7d": {"type": ["number", "null"]},
                            "Value_180d": {"type": ["number", "null"]},
                            "Value_30d": {"type": ["number", "null"]},
                            "Value_7d": {"type": ["number", "null"]},
                            "day": {"type": ["string"], "format": "date-time"}
                        },
                        "required": [
                            "Current",
                            "High_180d",
                            "High_30d",
                            "High_7d",
                            "Low_180d",
                            "Low_30d",
                            "Low_7d",
                            "MA_10d",
                            "MA_200d",
                            "MA_50d",
                            "Performance_180d",
                            "Performance_30d",
                            "Performance_7d",
                            "Value_180d",
                            "Value_30d",
                            "Value_7d",
                            "day"
                        ]
                    }
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "column_names": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "result_set_bytes": {"type": "integer"},
                        "total_row_count": {"type": "integer"},
                        "datapoint_count": {"type": "integer"},
                        "pending_time_millis": {"type": "integer"},
                        "execution_time_millis": {"type": "integer"}
                    },
                    "required": [
                        "column_names",
                        "result_set_bytes",
                        "total_row_count",
                        "datapoint_count",
                        "pending_time_millis",
                        "execution_time_millis"
                    ]
                }
            },
            "required": ["rows", "metadata"]
        }
    },
    "required": [
        "execution_id",
        "query_id",
        "state",
        "submitted_at",
        "expires_at",
        "execution_started_at",
        "execution_ended_at",
        "result"
    ]
}


