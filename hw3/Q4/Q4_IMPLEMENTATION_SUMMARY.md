# Q4 Implementation Summary

## ✅ **All Functions Implemented!**

Your GT username: **wlin99**

---

## 📝 **What Was Implemented**

### **Function 1: `user()` [Required]** ✅
```python
def user() -> str:
    return 'wlin99'
```
**Returns:** Your GT username as a string

---

### **Function 2: `load_data(gcp_storage_path)` [0 pts - Required]** ✅
```python
def load_data(gcp_storage_path: str) -> pyspark.sql.DataFrame:
    # Load CSV from GCS with header and infer schema
    df = spark.read.csv(gcp_storage_path, header=True, inferSchema=True)
    return df
```

**What it does:**
- Reads CSV file from Google Cloud Storage
- Path format: `gs://bucket-name/filename.csv`
- Infers schema automatically
- Returns Spark DataFrame

**Example usage:**
```python
df = load_data("gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv")
```

---

### **Function 3: `exclude_no_pickup_locations(df)` [2 pts]** ✅
```python
def exclude_no_pickup_locations(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    from pyspark.sql.functions import col
    
    # Exclude rows where pulocationid is null or zero
    df = df.filter((col('pulocationid').isNotNull()) & (col('pulocationid') != 0))
    
    return df
```

**What it does:**
- Filters out trips with no pickup location
- Excludes rows where `pulocationid` is:
  - NULL
  - 0 (zero)
- Returns filtered DataFrame

**Why it matters:**
- Invalid trips without pickup locations are meaningless
- Ensures data quality for downstream analysis

---

### **Function 4: `exclude_no_trip_distance(df)` [2 pts]** ✅
```python
def exclude_no_trip_distance(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    from pyspark.sql.functions import col
    from pyspark.sql.types import DecimalType
    
    # Cast trip_distance to decimal(38,10) and filter nulls and zeros
    df = df.withColumn('trip_distance', col('trip_distance').cast(DecimalType(38, 10)))
    df = df.filter((col('trip_distance').isNotNull()) & (col('trip_distance') != 0))
    
    return df
```

**What it does:**
- **Casts** `trip_distance` to `DecimalType(38, 10)`
  - Precision: 38 total digits
  - Scale: 10 digits after decimal
- Filters out trips where `trip_distance` is:
  - NULL
  - 0 (zero)
- Returns filtered DataFrame

**Why decimal(38,10)?**
- High precision for accurate calculations
- Avoids floating-point rounding errors
- Required by assignment specifications

---

### **Function 5: `include_fare_range(df)` [2 pts]** ✅
```python
def include_fare_range(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    from pyspark.sql.functions import col
    from pyspark.sql.types import DecimalType
    
    # Cast fare_amount to decimal(38,10) and filter range [20, 60] inclusive
    df = df.withColumn('fare_amount', col('fare_amount').cast(DecimalType(38, 10)))
    df = df.filter((col('fare_amount') >= 20) & (col('fare_amount') <= 60))
    
    return df
```

**What it does:**
- **Casts** `fare_amount` to `DecimalType(38, 10)`
- Filters to include ONLY trips where fare is:
  - >= $20 (inclusive)
  - <= $60 (inclusive)
- Returns filtered DataFrame

**Why this range?**
- Focus on "typical" taxi fares
- Excludes very short trips (<$20)
- Excludes very long trips or outliers (>$60)

---

### **Function 6: `get_highest_tip(df)` [2 pts]** ✅
```python
def get_highest_tip(df: pyspark.sql.DataFrame) -> decimal.Decimal:
    from pyspark.sql.functions import col, max as spark_max, round as spark_round
    from pyspark.sql.types import DecimalType
    
    # Cast tip_amount to decimal(38,10)
    df = df.withColumn('tip_amount', col('tip_amount').cast(DecimalType(38, 10)))
    
    # Find max tip and round to 2 decimal places
    max_tip = df.agg(spark_round(spark_max('tip_amount'), 2).alias('max_tip')).collect()[0]['max_tip']
    
    # Return as decimal.Decimal
    return decimal.Decimal(str(max_tip))
```

**What it does:**
- **Casts** `tip_amount` to `DecimalType(38, 10)`
- Finds the **maximum** tip amount
- **Rounds** to 2 decimal places
- Returns as `decimal.Decimal` (NOT float!)

**Example result:**
```python
max_tip = get_highest_tip(df_filtered)
# Result: Decimal('73.45')
```

**Key points:**
- Uses `spark_max()` for aggregation
- Uses `spark_round(..., 2)` for rounding
- Converts to `decimal.Decimal` for return type

---

### **Function 7: `get_total_toll(df)` [2 pts]** ✅
```python
def get_total_toll(df: pyspark.sql.DataFrame) -> decimal.Decimal:
    from pyspark.sql.functions import col, sum as spark_sum, round as spark_round
    from pyspark.sql.types import DecimalType
    
    # Cast tolls_amount to decimal(38,10)
    df = df.withColumn('tolls_amount', col('tolls_amount').cast(DecimalType(38, 10)))
    
    # Calculate total toll and round to 2 decimal places
    total_toll = df.agg(spark_round(spark_sum('tolls_amount'), 2).alias('total_toll')).collect()[0]['total_toll']
    
    # Return as decimal.Decimal
    return decimal.Decimal(str(total_toll))
```

**What it does:**
- **Casts** `tolls_amount` to `DecimalType(38, 10)`
- **Sums** all toll amounts
- **Rounds** to 2 decimal places
- Returns as `decimal.Decimal` (NOT float!)

**Example result:**
```python
total_toll = get_total_toll(df_filtered)
# Result: Decimal('12345.67')
```

**Key points:**
- Uses `spark_sum()` for aggregation
- Uses `spark_round(..., 2)` for rounding
- Converts to `decimal.Decimal` for return type

---

## 🔄 **Data Flow (How Functions Chain)**

```
1. load_data()
   ↓ Original DataFrame (~45K rows)
   
2. exclude_no_pickup_locations()
   ↓ Filtered DataFrame (~44K rows, removed nulls/zeros in pickup)
   
3. exclude_no_trip_distance()
   ↓ Filtered DataFrame (~43K rows, removed nulls/zeros in distance)
   
4. include_fare_range()
   ↓ Filtered DataFrame (~12K rows, only $20-60 fares)
   
5a. get_highest_tip()  → Single Decimal value
5b. get_total_toll()   → Single Decimal value
```

**Each function depends on the previous one's output!**

---

## 🎓 **Key Technical Concepts**

### **1. DecimalType vs Float**

❌ **Don't use float:**
```python
# WRONG - causes precision errors
df = df.withColumn('fare', col('fare').cast('float'))
```

✅ **Use DecimalType(38, 10):**
```python
# CORRECT - precise calculations
from pyspark.sql.types import DecimalType
df = df.withColumn('fare', col('fare').cast(DecimalType(38, 10)))
```

**Why?**
- Float: Binary representation, rounding errors
  - `0.1 + 0.2 = 0.30000000000000004` (float)
- Decimal: Exact representation
  - `0.1 + 0.2 = 0.3` (decimal) ✅

---

### **2. Filtering Nulls and Zeros**

**Pattern used in functions 3-4:**
```python
df = df.filter(
    (col('column_name').isNotNull()) &  # Not null
    (col('column_name') != 0)            # Not zero
)
```

**Why both?**
- NULL: Missing data
- Zero: Invalid value for location IDs and distances
- Both should be excluded for data quality

---

### **3. Aggregation Functions**

**Max (Function 6):**
```python
from pyspark.sql.functions import max as spark_max
df.agg(spark_max('column_name'))
```

**Sum (Function 7):**
```python
from pyspark.sql.functions import sum as spark_sum
df.agg(spark_sum('column_name'))
```

**Why alias imports?**
- `max` and `sum` are Python built-ins
- Use `spark_max` and `spark_sum` to avoid conflicts

---

### **4. Rounding and Collecting Results**

**Pattern used in functions 6-7:**
```python
result = df.agg(
    spark_round(spark_max('column'), 2).alias('result_name')
).collect()[0]['result_name']

return decimal.Decimal(str(result))
```

**Breakdown:**
1. `spark_round(..., 2)` - Round to 2 decimals in Spark
2. `.alias('result_name')` - Name the result column
3. `.collect()[0]` - Get first row as Python dict
4. `['result_name']` - Extract the value
5. `decimal.Decimal(str(...))` - Convert to decimal.Decimal

---

## ⚠️ **Common Pitfalls Avoided**

### **1. Don't modify input DataFrame**
❌ **Wrong:**
```python
def my_function(df):
    df = df.filter(...)  # Modifies original!
```

✅ **Correct:**
```python
def my_function(df):
    df = df.filter(...)  # Creates new DataFrame
    return df            # Explicit return
```

---

### **2. Don't use RDD API**
❌ **Wrong:**
```python
df.rdd.map(lambda x: x['fare'] * 2)  # Uses RDD!
```

✅ **Correct:**
```python
from pyspark.sql.functions import col
df.withColumn('doubled_fare', col('fare') * 2)  # DataFrame API
```

---

### **3. Don't leave debug statements**
❌ **Wrong:**
```python
def my_function(df):
    df = df.filter(...)
    df.show()  # DEBUG - will crash autograder!
    print(df.count())  # DEBUG - will crash autograder!
    return df
```

✅ **Correct:**
```python
def my_function(df):
    df = df.filter(...)
    return df  # Clean, no debug output
```

---

### **4. Return correct types**
❌ **Wrong:**
```python
def get_highest_tip(df) -> decimal.Decimal:
    return 123.45  # Returns float!
```

✅ **Correct:**
```python
def get_highest_tip(df) -> decimal.Decimal:
    return decimal.Decimal('123.45')  # Returns decimal.Decimal!
```

---

## 🧪 **Testing Your Implementation**

### **Expected Row Counts (Approximate):**

```python
# Original data
df = load_data(path)
df.count()  # ~45,000 rows

# After filtering pickup locations
df_no_pickup = exclude_no_pickup_locations(df)
df_no_pickup.count()  # ~44,000 rows (-2%)

# After filtering trip distance
df_no_distance = exclude_no_trip_distance(df_no_pickup)
df_no_distance.count()  # ~43,000 rows (-4%)

# After filtering fare range $20-60
df_fare_range = include_fare_range(df_no_distance)
df_fare_range.count()  # ~12,000 rows (-73%)

# Highest tip
max_tip = get_highest_tip(df_fare_range)
# ~$50-100 (varies by dataset)

# Total toll
total_toll = get_total_toll(df_fare_range)
# ~$10,000-20,000 (varies by dataset)
```

**Your numbers will vary slightly** depending on the exact dataset!

---

## 📤 **Before Submission Checklist**

- [ ] All 7 functions implemented
- [ ] Username is 'wlin99'
- [ ] All testing code commented out (Cells 20-32)
- [ ] No print() statements in function bodies
- [ ] No show() statements in function bodies
- [ ] No display() statements in function bodies
- [ ] All functions return correct types
- [ ] Tested on full dataset in GCP
- [ ] Notebook downloaded from GCP Dataproc
- [ ] Cluster deleted to save costs

---

## 💡 **Industry Perspective**

**What You're Learning:**
- **Managed Spark on GCP:** Dataproc = Google's managed Spark service
- **Data Quality:** Filtering nulls, zeros, outliers
- **Precision:** Using Decimal for financial calculations
- **Cloud Storage:** GCS = Google's S3 equivalent
- **Serverless Notebooks:** No local setup, run anywhere

**In a Real Company:**
- Same code patterns for ETL pipelines
- Same decimal precision for financial data
- Same filtering logic for data quality
- Scale to billions of rows (not just 45K!)
- Schedule to run daily/hourly

---

## 🆚 **Comparison: AWS vs GCP (What You've Learned)**

| Aspect | **AWS (Q3)** | **GCP (Q4)** |
|--------|--------------|--------------|
| Service | Athena (serverless) | Dataproc (managed) |
| Storage | S3 | Google Cloud Storage (GCS) |
| Path Format | `s3://bucket/file` | `gs://bucket/file` |
| Setup | Simpler | More steps |
| Notebook | Athena notebooks | JupyterLab |
| Cost Model | Per query | Per hour |
| Cluster | Auto (serverless) | Manual creation |

**Both run PySpark!** Your code is portable between them. 🚀

---

**You're all set! The code is complete and ready to run on GCP Dataproc!** ✅

