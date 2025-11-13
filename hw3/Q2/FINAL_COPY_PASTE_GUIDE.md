# ✅ FINAL Copy-Paste Guide for Databricks
## Using YOUR Exact Starter Code with df_filter

---

## 🎯 **Your Databricks Notebook Already Has:**

1. ✅ Data loaded into `df`
2. ✅ Filter applied and saved to `df_filter`
3. ✅ All subsequent tasks use `df_filter` (already filtered!)

**You're starting from here:**
```python
# Your starter code (already in Databricks):
df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(file_path)
df_filter = df.filter((df.PULocationID != df.DOLocationID) & (df.trip_distance > 2.0))
df_filter.show(5)
```

---

## 📋 **Step-by-Step: Copy These Into NEW Cells**

### **CELL 1: Imports**
After your starter code, create a NEW cell and paste:

```python
from pyspark.sql.functions import (
    col, count, sum as _sum, avg, desc, asc, 
    dayofweek, date_format, hour, lag, when,
    year, month, dayofmonth, to_date, row_number
)
from pyspark.sql.window import Window
```

**Run this cell** ✅

---

### **CELL 2: Load Zone Lookup Table**
Create a NEW cell and paste:

```python
# Load zone lookup table (update path if yours is different)
zone_lookup_path = "/Volumes/workspace/default/q2vol/taxi_zone_lookup.csv"

zone_lookup = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(zone_lookup_path)

print("Zone lookup count:", zone_lookup.count())
display(zone_lookup.limit(5))
```

**Update path if needed, then run** ✅

---

### **CELL 3: Task 1a - Top 5 Dropoff Locations**
Create a NEW cell and paste:

```python
task1a = df_filter \
    .groupBy("DOLocationID") \
    .agg(count("*").alias("number_of_dropoffs")) \
    .orderBy(desc("number_of_dropoffs"), asc("DOLocationID")) \
    .limit(5)

print("=== Task 1a: Top 5 Dropoff Locations ===")
display(task1a)
```

**Run → Copy output to q2_results.csv Part 1a** ✅

---

### **CELL 4: Task 1b - Top 5 Pickup Locations**
Create a NEW cell and paste:

```python
task1b = df_filter \
    .groupBy("PULocationID") \
    .agg(count("*").alias("number_of_pickups")) \
    .orderBy(desc("number_of_pickups"), asc("PULocationID")) \
    .limit(5)

print("=== Task 1b: Top 5 Pickup Locations ===")
display(task1b)
```

**Run → Copy output to q2_results.csv Part 1b** ✅

---

### **CELL 5: Task 2 - Top 3 by Overall Activity**
Create a NEW cell and paste:

```python
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
```

**Run → Copy output to q2_results.csv Part 2** ✅

---

### **CELL 6: Task 3 - All Boroughs**
Create a NEW cell and paste:

```python
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
```

**Run → Copy output to q2_results.csv Part 3** ✅

---

### **CELL 7: Task 4 - Top 2 Weekdays**
Create a NEW cell and paste:

```python
# Convert pickup datetime to date and get day name
daily_pickups = df_filter \
    .withColumn("pickup_date", to_date(col("lpep_pickup_datetime"))) \
    .withColumn("day_of_week", date_format(col("lpep_pickup_datetime"), "EEEE")) \
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

**Run → Copy output to q2_results.csv Part 4** ✅

---

### **CELL 8: Task 5 - Brooklyn Hourly**
Create a NEW cell and paste:

```python
# Extract hour and join with Brooklyn zones
brooklyn_hourly = df_filter \
    .withColumn("hour_of_day", hour(col("lpep_pickup_datetime"))) \
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

**Run → Copy output to q2_results.csv Part 5 (should show 24 rows)** ✅

---

### **CELL 9: Task 6 - January % Increase**
Create a NEW cell and paste:

```python
# Filter Manhattan pickups in January
manhattan_jan = df_filter \
    .join(zone_lookup, df_filter.PULocationID == zone_lookup.LocationID, "inner") \
    .filter(col("Borough") == "Manhattan") \
    .withColumn("pickup_month", month(col("lpep_pickup_datetime"))) \
    .filter(col("pickup_month") == 1) \
    .withColumn("day", dayofmonth(col("lpep_pickup_datetime")))

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

**Run → Copy output to q2_results.csv Part 6** ✅

---

## 🎉 **That's It! All Tasks Complete**

### **Next Steps:**

1. **Verify all outputs look correct:**
   - Task 1a: 5 rows
   - Task 1b: 5 rows
   - Task 2: 3 rows
   - Task 3: 7 rows (all boroughs)
   - Task 4: 2 rows
   - Task 5: 24 rows
   - Task 6: 3 rows

2. **Copy all outputs to `q2_results.csv`**

3. **Export your notebook:**
   - File → Export → DBC Archive → Save as `q2.dbc`
   - File → Export → IPython Notebook → Save as `q2.ipynb`

4. **Submit to Gradescope:**
   - `q2.dbc`
   - `q2.ipynb`
   - `q2_results.csv`

---

## ✅ **Key Differences from Previous Version**

✅ Uses `df_filter` (your starter code variable)  
✅ No need to create filter yourself (already done!)  
✅ All tasks reference `df_filter` directly  
✅ Matches your exact Databricks setup  

---

## 📊 **Quick Verification**

Run this in a cell to verify everything is working:

```python
print("Original data count:", df.count())
print("Filtered data count:", df_filter.count())
print("Zone lookup count:", zone_lookup.count())
print("\nAll variables loaded successfully! ✅")
```

Expected output:
- Original: ~630,000 rows
- Filtered: Less than original (should be majority of data)
- Zone lookup: 266 rows

---

**You're all set! Just copy-paste each cell and run in order. Total time: ~30 minutes 🚀**

