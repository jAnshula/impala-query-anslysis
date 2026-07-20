ROOT_CAUSES = {

    "missing_statistics": {

        "title":
            "Missing Statistics",

        "severity":
            "HIGH",

        "recommendations":
            [
                "compute_stats"
            ]
    },

    "metadata_delay": {

        "title":
            "Metadata Loading Delay",

        "severity":
            "CRITICAL",

        "recommendations":
            [
                "refresh_metadata"
            ]
    },

    "admission_delay": {

        "title":
            "Admission Control Delay",

        "severity":
            "HIGH",

        "recommendations":
            [
                "increase_pool_capacity"
            ]
    },

    "memory_spill": {

        "title":
            "Memory Spill",

        "severity":
            "HIGH",

        "recommendations":
            [
                "increase_mem_limit"
            ]
    },

    "data_skew": {

        "title":
            "Data Skew",

        "severity":
            "CRITICAL",

        "recommendations":
            [
                "rebalance_data"
            ]
    }
}

