"""
HW3 Q2 - FINAL DATABRICKS VERSION
==================================
Based on YOUR EXACT starter code with df_filter already created

Copy each section below into separate cells in your Databricks notebook
"""

# ============================================================================
# YOUR STARTER CODE IS ALREADY IN DATABRICKS - DON'T COPY THIS
# ============================================================================
# You already have:
# - df (original data loaded)
# - df_filter (filtered data: PULocationID != DOLocationID AND trip_distance > 2.0)
# Just reference df_filter in all tasks below!


# ============================================================================
# CELL 1: IMPORTS - Put this in a NEW cell after your starter code
# ============================================================================

from pyspark.sql.functions import (
    col, count, sum as _sum, avg, desc, asc, 
    dayofweek, date_format, hour, lag, when,
    year, month, dayofmonth, to_date, to_timestamp, row_number
)
from pyspark.sql.window import Window


# ============================================================================
# CELL 2: Load Zone Lookup Table
# ============================================================================

# Load zone lookup table (update path if yours is different)
zone_lookup_path = "/Volumes/workspace/default/q2vol/taxi_zone_lookup.csv"

zone_lookup = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(zone_lookup_path)

print("Zone lookup count:", zone_lookup.count())
display(zone_lookup.limit(5))


# ============================================================================
# TASK 1a: Top 5 Most Popular Dropoff Locations
# ============================================================================
# Use df_filter (already filtered by starter code)

task1a = df_filter \
    .groupBy("DOLocationID") \
    .agg(count("*").alias("number_of_dropoffs")) \
    .orderBy(desc("number_of_dropoffs"), asc("DOLocationID")) \
    .limit(5)

print("=== Task 1a: Top 5 Dropoff Locations ===")
display(task1a)


# ============================================================================
# TASK 1b: Top 5 Most Popular Pickup Locations
# ============================================================================

task1b = df_filter \
    .groupBy("PULocationID") \
    .agg(count("*").alias("number_of_pickups")) \
    .orderBy(desc("number_of_pickups"), asc("PULocationID")) \
    .limit(5)

print("=== Task 1b: Top 5 Pickup Locations ===")
display(task1b)


# ============================================================================
# TASK 2: Top 3 Locations with Maximum Overall Activity
# ============================================================================

# Count pickups per location
pickups = df_filter \
    .groupBy(col("PULocationID").alias("locationID")) \
    .agg(count("*").alias("pickup_count"))

# Count dropoffs per location
dropoffs = df_filter \
    .groupBy(col("DOLocationID").alias("locationID")) \
    .agg(count("*").alias("dropoff_count"))

# Full outer join to get all locations
task2 = pickups.join(dropoffs, "locationID", "full_outer") \
    .fillna(0, subset=["pickup_count", "dropoff_count"]) \
    .withColumn("total_activity", col("pickup_count") + col("dropoff_count")) \
    .select("locationID", "total_activity") \
    .orderBy(desc("total_activity"), asc("locationID")) \
    .limit(3)

print("=== Task 2: Top 3 Locations by Overall Activity ===")
display(task2)


# ============================================================================
# TASK 3: All Boroughs Ordered by Total Activity
# ============================================================================

# Get all pickups with borough info
pickups_borough = df_filter \
    .join(zone_lookup, df_filter.PULocationID == zone_lookup.LocationID, "inner") \
    .select(col("Borough").alias("borough_pickup"))

# Get all dropoffs with borough info
dropoffs_borough = df_filter \
    .join(zone_lookup, df_filter.DOLocationID == zone_lookup.LocationID, "inner") \
    .select(col("Borough").alias("borough_dropoff"))

# Union pickups and dropoffs
all_activities = pickups_borough.select(col("borough_pickup").alias("Borough")) \
    .union(dropoffs_borough.select(col("borough_dropoff").alias("Borough")))

# Group by borough and count
task3 = all_activities \
    .groupBy("Borough") \
    .agg(count("*").alias("total_number_activities")) \
    .orderBy(desc("total_number_activities"))

print("=== Task 3: All Boroughs by Total Activity ===")
display(task3)


# ============================================================================
# TASK 4: Top 2 Days of Week with Largest Average Daily Pickups
# ============================================================================

# Convert string datetime to proper timestamp first, then to date
# Date format in CSV is: MM/dd/yyyy H:mm (e.g., "01/21/2019 9:32")
daily_pickups = df_filter \
    .withColumn("pickup_timestamp", to_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy H:mm")) \
    .withColumn("pickup_date", to_date(col("pickup_timestamp"))) \
    .withColumn("day_of_week", date_format(col("pickup_timestamp"), "EEEE")) \
    .groupBy("pickup_date", "day_of_week") \
    .agg(count("*").alias("daily_count"))

# Calculate average pickups per day of week
task4 = daily_pickups \
    .groupBy("day_of_week") \
    .agg(avg("daily_count").alias("avg_count")) \
    .orderBy(desc("avg_count")) \
    .limit(2)

print("=== Task 4: Top 2 Days of Week by Average Pickups ===")
display(task4)


# ============================================================================
# TASK 5: Brooklyn Zone with Most Pickups per Hour (0-23)
# ============================================================================

# Extract hour and join with Brooklyn zones
# Parse datetime string first, then extract hour
brooklyn_hourly = df_filter \
    .withColumn("pickup_timestamp", to_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy H:mm")) \
    .withColumn("hour_of_day", hour(col("pickup_timestamp"))) \
    .join(zone_lookup, df_filter.PULocationID == zone_lookup.LocationID, "inner") \
    .filter(col("Borough") == "Brooklyn") \
    .groupBy("hour_of_day", "Zone") \
    .agg(count("*").alias("pickup_count"))

# Find max pickups per hour using window function
window_spec = Window.partitionBy("hour_of_day").orderBy(desc("pickup_count"))

task5 = brooklyn_hourly \
    .withColumn("rank", row_number().over(window_spec)) \
    .filter(col("rank") == 1) \
    .select(
        col("hour_of_day"),
        col("Zone"),
        col("pickup_count").alias("max_count")
    ) \
    .orderBy("hour_of_day")

print("=== Task 5: Brooklyn Zone with Most Pickups per Hour ===")
display(task5)


# ============================================================================
# TASK 6: Top 3 January Days with Largest % Pickup Increase (Manhattan)
# ============================================================================

# Filter Manhattan pickups in January
# Parse datetime string first
manhattan_jan = df_filter \
    .withColumn("pickup_timestamp", to_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy H:mm")) \
    .join(zone_lookup, df_filter.PULocationID == zone_lookup.LocationID, "inner") \
    .filter(col("Borough") == "Manhattan") \
    .withColumn("pickup_month", month(col("pickup_timestamp"))) \
    .filter(col("pickup_month") == 1) \
    .withColumn("day", dayofmonth(col("pickup_timestamp")))

# Aggregate pickups by day of January (across all years)
daily_counts = manhattan_jan \
    .groupBy("day") \
    .agg(count("*").alias("daily_count")) \
    .orderBy("day")

# Calculate previous day's count using lag window function
window_spec = Window.orderBy("day")

with_prev = daily_counts \
    .withColumn("prev_day_count", lag("daily_count", 1).over(window_spec))

# Calculate percentage change
task6 = with_prev \
    .filter(col("prev_day_count").isNotNull()) \
    .withColumn(
        "percent_change",
        ((col("daily_count") - col("prev_day_count")) / col("prev_day_count")) * 100
    ) \
    .select("day", "percent_change") \
    .orderBy(desc("percent_change")) \
    .limit(3)

print("=== Task 6: Top 3 January Days with Largest % Increase (Manhattan) ===")
display(task6)


# ============================================================================
# OPTIONAL: Display All Results Together
# ============================================================================

print("\n" + "="*80)
print("SUMMARY - Copy these outputs to q2_results.csv")
print("="*80)

print("\n--- Part 1a: top-5 most popular drop locations ---")
display(task1a)

print("\n--- Part 1b: top-5 most popular pickup locations ---")
display(task1b)

print("\n--- Part 2: top-3 locations with maximum overall activity ---")
display(task2)

print("\n--- Part 3: all boroughs ordered by activity ---")
display(task3)

print("\n--- Part 4: top 2 days of week with largest average pickups ---")
display(task4)

print("\n--- Part 5: Brooklyn zone with most pickups per hour (0-23) ---")
display(task5)

print("\n--- Part 6: Top 3 January days in Manhattan with largest % increase ---")
display(task6)

