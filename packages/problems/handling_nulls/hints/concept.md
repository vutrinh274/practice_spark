NULL values in Spark need special handling — comparing `NULL = NULL` always returns NULL (not true). Use dedicated NULL-handling functions instead of regular comparisons.
