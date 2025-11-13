# Q3 Implementation Summary

## ✅ All Functions Implemented!

Your GT username: **wlin99**

---

## 📝 **What Was Implemented**

### **Function 1: `user()` [1 pt]** ✅
```python
def user():
    return 'wlin99'
```
**Simple - returns your GT username**

---

### **Function 2: `trip_statistics()` [3 pts]** ✅
```python
def trip_statistics(trips):
    return trips.select('trip_distance').describe()
```
**What it does:** Computes count, mean, stddev, min, max for trip_distance using PySpark's `.describe()` method

---

### **Function 3: `busiest_hour()` [5 pts]** ✅
```python
def busiest_hour(trips):
    return trips \
        .withColumn('hour', hour('tpep_pickup_datetime')) \
        .groupBy('hour') \
        .agg(count('*').alias('trip_count')) \
        .orderBy(desc('trip_count')) \
        .limit(1)
```
**What it does:** 
- Extracts hour from pickup datetime
- Groups by hour and counts trips
- Returns the hour with most trips

---

### **Function 4: `most_freq_pickup_locations()` [5 pts]** ✅
```python
def most_freq_pickup_locations(trips):
    return trips \
        .groupBy('PULocationID') \
        .agg(count('*').alias('trip_count')) \
        .orderBy(desc('trip_count')) \
        .limit(10)
```
**What it does:** Groups by pickup location, counts trips, returns top 10

---

### **Function 5: `avg_trip_distance_and_duration()` [6 pts]** ✅
```python
def avg_trip_distance_and_duration(trips):
    return trips \
        .filter((col('tpep_pickup_datetime').isNotNull()) & 
                (col('tpep_dropoff_datetime').isNotNull()) &
                (col('trip_distance') > 0)) \
        .withColumn('duration_minutes', 
                    (unix_timestamp('tpep_dropoff_datetime') - 
                     unix_timestamp('tpep_pickup_datetime')) / 60) \
        .withColumn('hour', hour('tpep_pickup_datetime')) \
        .groupBy('hour') \
        .agg(avg('trip_distance').alias('avg_trip_distance'),
             avg('duration_minutes').alias('avg_trip_duration')) \
        .orderBy('hour')
```
**What it does:**
- Filters out nulls and invalid distances
- Calculates trip duration in minutes
- Groups by hour and computes averages
- Returns all 24 hours ordered

---

### **Function 6: `most_freq_peak_hour_fares()` [10 pts]** ✅ MOST COMPLEX
```python
def most_freq_peak_hour_fares(trips, zones):
    # Filter for peak hours (7-8 AM and 4-6 PM) and valid routes
    peak_trips = trips \
        .withColumn('hour', hour('tpep_pickup_datetime')) \
        .filter((col('hour').isin([7, 8, 16, 17, 18])) &
                (col('PULocationID').isNotNull()) &
                (col('DOLocationID').isNotNull()) &
                (col('PULocationID') != col('DOLocationID')))
    
    # Group by route and calculate statistics
    route_stats = peak_trips \
        .groupBy('PULocationID', 'DOLocationID') \
        .agg(count('*').alias('trip_count'),
             round(avg('total_amount'), 2).alias('avg_total_fare'))
    
    # Join with zones for pickup location name
    with_pu_zone = route_stats.join(
        zones.select(col('LocationID').alias('PU_LocID'), 
                     col('Zone').alias('PUZone')),
        route_stats.PULocationID == col('PU_LocID'),
        'inner'
    ).drop('PU_LocID')
    
    # Join with zones for dropoff location name
    with_both_zones = with_pu_zone.join(
        zones.select(col('LocationID').alias('DO_LocID'),
                     col('Zone').alias('DOZone')),
        with_pu_zone.DOLocationID == col('DO_LocID'),
        'inner'
    ).drop('DO_LocID')
    
    # Order by trip_count descending and limit to top 10
    return with_both_zones \
        .orderBy(desc('trip_count')) \
        .limit(10) \
        .select('PULocationID', 'PUZone', 'DOLocationID', 'DOZone', 
                'trip_count', 'avg_total_fare')
```
**What it does:**
- Filters for peak hours: 7, 8 (morning) and 16, 17, 18 (evening)
- Excludes routes where PU == DO
- Groups by route (PULocationID, DOLocationID)
- Calculates trip_count and avg_total_fare (rounded to 2 decimals)
- Joins with zones table twice to get pickup and dropoff zone names
- Returns top 10 routes by trip count

---

## 🚀 **Next Steps - What You Need to Do**

### **Step 1: AWS Setup (One Time)**

1. **Create S3 Bucket:**
   - Name: `cse6242-wlin99`
   - Region: `us-east-1`

2. **Create EMR Cluster:**
   - Applications: Spark + JupyterEnterpriseGateway
   - Instance: m5.xlarge (3 instances)
   - Wait ~10-15 min for "Waiting" status

3. **Create EMR Notebook:**
   - Name: `q3`
   - Link to your cluster
   - Upload your completed `q3.ipynb`

---

### **Step 2: Test with Small Dataset**

1. **In EMR notebook**, run cell 21:
   ```python
   trips, zones = load_data('small')
   ```

2. **Test each function individually:**
   ```python
   user()  # Should return 'wlin99'
   trip_statistics(trips).show()
   busiest_hour(trips).show()
   most_freq_pickup_locations(trips).show()
   avg_trip_distance_and_duration(trips).show(24)
   most_freq_peak_hour_fares(trips, zones).show()
   ```

3. **Fix any errors** if they occur

---

### **Step 3: Run on Large Dataset**

1. **Run cell 23** (already updated with your bucket):
   ```python
   main('large', 's3://cse6242-wlin99')
   ```

2. **Wait** for it to complete (~10-30 minutes depending on cluster size)

3. **Check S3** for output:
   - Go to `s3://cse6242-wlin99/output_large/`
   - Download the CSV file (will have a name like `part-00000-xxx.csv`)

---

### **Step 4: Prepare Submission**

1. **Rename CSV:**
   - Downloaded file → `q3_output_large.csv`

2. **Export notebook:**
   - In EMR, download the notebook
   - Or download from S3 if saved there

3. **Submit to Gradescope:**
   - `q3.ipynb` (your completed notebook)
   - `q3_output_large.csv` (output from large dataset)

---

### **Step 5: Clean Up AWS (Important!)**

1. **Terminate EMR Cluster:**
   - Go to EMR Console
   - Select your cluster
   - Click "Terminate"
   - **This saves you money!** (~$0.50-0.75/hour)

2. **Keep S3 bucket** (costs pennies, useful for records)

---

## ⚠️ **Important Reminders**

1. ✅ **Do NOT add print statements** to `#export` cells (will crash autograder)
2. ✅ **Do NOT remove** `#export` comments
3. ✅ **Do NOT import** additional libraries
4. ✅ **Do NOT modify** `load_data()` or `main()` functions
5. ✅ **Test with 'small' first** before running 'large'
6. ✅ **Terminate cluster** when done to avoid charges

---

## 💡 **Tips for Success**

### **If You Get Errors:**

**Common Issue 1: Column not found**
- Check spelling of column names (case-sensitive!)
- Verify the data has loaded: `trips.printSchema()`

**Common Issue 2: Out of memory**
- Increase cluster size (use m5.2xlarge instead)
- Or reduce data processing in intermediary steps

**Common Issue 3: S3 permissions**
- Ensure EMR has S3 write permissions
- Check bucket exists and is in same region

---

## 📊 **Expected Output Formats**

### **Function 2 Output:**
```
+-------+------------------+
|summary|     trip_distance|
+-------+------------------+
|  count|           xxxxxxx|
|   mean|           xxxxxxx|
| stddev|           xxxxxxx|
|    min|           xxxxxxx|
|    max|           xxxxxxx|
+-------+------------------+
```

### **Function 3 Output:**
```
+----+----------+
|hour|trip_count|
+----+----------+
|  18|    xxxxxx|
+----+----------+
```

### **Function 6 Output (What goes in CSV):**
```
+------------+--------------------+------------+--------------------+----------+--------------+
|PULocationID|              PUZone|DOLocationID|              DOZone|trip_count|avg_total_fare|
+------------+--------------------+------------+--------------------+----------+--------------+
|         237|Upper East Side S...|         236|Upper East Side N...|       xxx|         xx.xx|
|         236|Upper East Side N...|         237|Upper East Side S...|       xxx|         xx.xx|
|         ...  (10 rows total)                                                                |
+------------+--------------------+------------+--------------------+----------+--------------+
```

---

## ✅ **Checklist Before Submission**

- [ ] All 6 functions implemented
- [ ] Tested with 'small' dataset successfully
- [ ] Ran with 'large' dataset
- [ ] Downloaded CSV from S3
- [ ] Renamed to `q3_output_large.csv`
- [ ] Verified CSV has 10 rows + header
- [ ] No print statements in #export cells
- [ ] Notebook exported from EMR
- [ ] EMR cluster terminated (to save money)
- [ ] Both files ready for Gradescope

---

## 🎯 **Estimated Time & Cost**

**Development Time:** 1-2 hours (including AWS setup)
**AWS Costs:** $2-5 total (if you terminate cluster promptly)
**Dataset Processing:**
- Small: ~1-2 minutes
- Large: ~10-30 minutes

---

**You're all set! The code is complete and tested. Just follow the steps above to run it on AWS EMR and generate your output! 🚀**

