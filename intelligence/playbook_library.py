PLAYBOOKS = {

    "metadata_delay": {

        "evidence": [

            "PARTITION_NOT_FOUND detected",

            "Planning retries observed",

            "Planning dominates runtime"
        ],

        "impact":

            "Planner repeatedly reloads metadata causing long frontend delays.",

        "actions": [

            "INVALIDATE METADATA <table>",

            "REFRESH <table>",

            "Verify catalogd topic propagation",

            "Check HMS partition consistency",

            "Review catalogd GC pauses",

            "Review catalogd CPU utilization"
        ],

        "verification": [

            "Planning retries disappear",

            "Planning time drops",

            "Query runtime improves"
        ]
    },

    "missing_statistics": {

        "evidence": [

            "Missing table statistics",

            "Missing column statistics"
        ],

        "impact":

            "Optimizer may choose inefficient join order and scan strategy.",

        "actions": [

            "COMPUTE STATS table",

            "COMPUTE INCREMENTAL STATS partition",

            "Validate table row counts",

            "Refresh planner metadata"
        ],

        "verification": [

            "Cardinality estimates improve",

            "Runtime decreases"
        ]
    },

    "admission_delay": {

        "evidence": [

            "Long admission queue wait"
        ],

        "impact":

            "Cluster resources unavailable causing query queuing.",

        "actions": [

            "Review admission pool limits",

            "Increase queue resources",

            "Review concurrent workload",

            "Check resource contention"
        ],

        "verification": [

            "Admission wait approaches zero"
        ]
    },

    "memory_spill": {

        "evidence": [

            "Scratch writes detected",

            "Scratch bytes written"
        ],

        "impact":

            "Query spills to disk causing severe slowdown.",

        "actions": [

            "Increase MEM_LIMIT",

            "Reduce data volume",

            "Review join strategy",

            "Review cardinality estimates",

            "Compute statistics"
        ],

        "verification": [

            "Scratch writes disappear",

            "Runtime improves"
        ]
    }
}

