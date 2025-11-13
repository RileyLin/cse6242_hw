# Task 4 Fix - Date Format Issue

## The Problem
The `lpep_pickup_datetime` column is stored as STRING in format: `'01/21/2019 9:32'`
Not as a proper timestamp type.

## The Solution
Parse the string with the correct format first, then extract date and day name.

---

## REPLACE YOUR TASK 4 CODE WITH THIS:

```python
# Convert string datetime to proper timestamp first, then to date
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
```

---

## What Changed?

**Before (Wrong):**
```python
.withColumn("pickup_date", to_date(col("lpep_pickup_datetime")))  # Fails - wrong format
```

**After (Correct):**
```python
.withColumn("pickup_timestamp", to_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy H:mm"))  # Parse string first
.withColumn("pickup_date", to_date(col("pickup_timestamp")))  # Then extract date
```

---

## Key Fix:
Added the format string `"MM/dd/yyyy H:mm"` to tell Spark how to parse your datetime strings.

The format breakdown:
- `MM` = month (01-12)
- `dd` = day (01-31)
- `yyyy` = year (2019)
- `H` = hour (0-23, single digit allowed)
- `mm` = minute (00-59)

This matches your data format: `01/21/2019 9:32`

---

**Copy the corrected code above into your Task 4 cell and run again!**

