# ⚠️ IMPORTANT: DateTime Format Fix for All Tasks

## 🔴 The Problem You Encountered

Your datetime columns are stored as **STRINGS** in format: `"01/21/2019 9:32"`

When you tried to use `to_date()` directly, Spark couldn't parse it and threw:
```
[CAST_INVALID_INPUT] The value '01/21/2019 9:32' of the type "STRING" 
cannot be cast to "DATE" because it is malformed.
```

---

## ✅ The Solution

**Always parse the string to timestamp FIRST**, then extract date/hour/day:

```python
# WRONG (causes error):
.withColumn("pickup_date", to_date(col("lpep_pickup_datetime")))

# CORRECT:
.withColumn("pickup_timestamp", to_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy H:mm"))
.withColumn("pickup_date", to_date(col("pickup_timestamp")))
```

---

## 📋 UPDATED IMPORTS (Cell 1)

**REPLACE your imports cell with this:**

```python
from pyspark.sql.functions import (
    col, count, sum as _sum, avg, desc, asc, 
    dayofweek, date_format, hour, lag, when,
    year, month, dayofmonth, to_date, to_timestamp, row_number
)
from pyspark.sql.window import Window
```

**Key addition:** `to_timestamp` function

---

## 📝 Fixed Task Code (Copy-Paste Ready)

### **Task 4: Top 2 Weekdays (FIXED)**

```python
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
```

---

### **Task 5: Brooklyn Hourly (FIXED)**

```python
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
```

---

### **Task 6: January % Increase (FIXED)**

```python
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
```

---

## 🔑 Understanding the Fix

### **Date Format String Breakdown:**
`"MM/dd/yyyy H:mm"`

- `MM` = month with leading zero (01, 02, ..., 12)
- `dd` = day with leading zero (01, 02, ..., 31)
- `yyyy` = 4-digit year (2019)
- `H` = hour WITHOUT leading zero (0, 1, 2, ..., 23)
- `mm` = minute with leading zero (00, 01, ..., 59)

This matches your data: `"01/21/2019 9:32"` ← hour has NO leading zero!

---

## ✅ What Tasks Need This Fix?

- ✅ **Task 1a & 1b**: NO datetime operations - no fix needed
- ✅ **Task 2**: NO datetime operations - no fix needed
- ✅ **Task 3**: NO datetime operations - no fix needed
- 🔧 **Task 4**: FIXED - uses `to_date()` and `date_format()`
- 🔧 **Task 5**: FIXED - uses `hour()`
- 🔧 **Task 6**: FIXED - uses `month()` and `dayofmonth()`

---

## 📂 Updated Files

I've already updated:
- ✅ `q2_final_databricks.py` - All fixes applied
- ✅ Added `to_timestamp` to imports

---

## 🚀 Action Items for You

1. **Update your imports cell** (add `to_timestamp`)
2. **Replace Task 4 code** with the fixed version above
3. **Replace Task 5 code** with the fixed version above
4. **Replace Task 6 code** with the fixed version above
5. **Run all cells** - should work now!

---

## 💡 Why This Happened

Your starter code loaded the CSV with `inferSchema=true`, but:
- Spark couldn't automatically detect the datetime format
- So it treated the columns as STRINGS
- We need to explicitly tell Spark the format using `to_timestamp(col, "format")`

This is **very common in real-world data engineering** - CSV files with custom datetime formats!

---

**All code has been fixed in `q2_final_databricks.py`. Copy the updated code from there! ✅**

