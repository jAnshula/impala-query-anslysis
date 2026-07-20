# intelligence/recommendation_library.py

RECOMMENDATIONS = {

    "compute_stats": {
        "title": "Refresh Table Statistics",
        "description": "Run COMPUTE STATS on tables used by the query."
    },

    "refresh_metadata": {
        "title": "Refresh Metadata",
        "description": "Investigate catalogd and metadata synchronization."
    },

    "catalog_health": {
        "title": "Investigate Catalog Health",
        "description": "Review catalogd CPU, GC pauses and topic size."
    },

    "review_partitions": {
        "title": "Review Partition Counts",
        "description": "Large partition counts can significantly slow planning."
    },

    # Execution-related
    "data_distribution": {
        "title": "Optimize Data Distribution",
        "description": "Rebalance data across nodes to reduce skew and improve parallelism."
    },

    "join_strategy": {
        "title": "Review Join Strategy",
        "description": "Consider broadcast joins or repartitioning to optimize query performance."
    },

    # Scan-related
    "partition_pruning": {
        "title": "Enable Partition Pruning",
        "description": "Ensure queries filter partitions effectively to reduce scan size."
    },

    "predicate_pushdown": {
        "title": "Apply Predicate Pushdown",
        "description": "Push filters closer to the data source to minimize scanned rows."
    },

    "file_compaction": {
        "title": "Perform File Compaction",
        "description": "Compact small files into larger ones to improve scan efficiency."
    },

    # Resource-related (from root_cause_catalog)
    "increase_pool_capacity": {
        "title": "Increase Pool Capacity",
        "description": "Adjust admission control pool limits to reduce queuing delays."
    },

    "increase_mem_limit": {
        "title": "Increase Memory Limit",
        "description": "Raise query memory limits to avoid spilling and improve performance."
    },

    "rebalance_data": {
        "title": "Rebalance Data",
        "description": "Redistribute data across partitions or nodes to reduce skew."
    },

    "compute_table_stats": {
    "title": "Compute Table Statistics",
    "description":
        "Run COMPUTE STATS on missing tables."
    }
}

