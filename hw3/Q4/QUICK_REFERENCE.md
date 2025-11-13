# Q4 Quick Reference Card

## 📋 **Essential Info**

**Your GT Username:** `wlin99`  
**GCP Project:** `hw3-q4-wlin99` (or your chosen name)  
**GCS Bucket:** `cse6242-wlin99-hw3q4`  
**Region:** `us-central1` (Iowa) - Must match bucket & cluster!  
**Data File:** `yellow_tripdata09-08-2021.csv`

---

## 🚀 **Quick Start (7 Steps)**

### 1️⃣ Activate GCP Free Credits
```
Go to: https://console.cloud.google.com/
Click: "Try for free"
Enter: Billing info (won't be charged)
Get: $300 free credits ✅
```

### 2️⃣ Create GCS Bucket
```
Service: Cloud Storage → Buckets
Name: cse6242-wlin99-hw3q4
Region: us-central1
Click: CREATE
```

### 3️⃣ Upload Data
```
Click on bucket
Upload: yellow_tripdata09-08-2021.csv
Path: gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv
```

### 4️⃣ Create Dataproc Cluster
```
Service: Dataproc → Clusters
Name: hw3-q4-cluster
Region: us-central1
Type: Single Node (cheapest!)
Machine: n1-standard-4
Optional Components: ✅ Jupyter Notebook
Wait: 2-5 minutes
```

### 5️⃣ Access Jupyter
```
Click: hw3-q4-cluster
Tab: WEB INTERFACES
Click: Jupyter
Upload: q4.ipynb
```

### 6️⃣ Test Your Code
```
Update cell 20: gcp_storage_path = "gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv"
Run all cells
Verify: No errors ✅
```

### 7️⃣ Submit & Clean Up
```
Comment out: All testing code (cells 20-32)
Download: q4.ipynb
Delete: Dataproc cluster (to save money!)
Submit: q4.ipynb to Gradescope
```

---

## 📁 **Files Created**

| File | Description |
|------|-------------|
| `q4.ipynb` | ✅ All 7 functions implemented |
| `GCP_SETUP_GUIDE.md` | Step-by-step GCP instructions |
| `Q4_IMPLEMENTATION_SUMMARY.md` | Detailed code explanations |
| `QUICK_REFERENCE.md` | This cheat sheet |

---

## ✅ **What's Implemented**

1. ✅ `user()` → Returns 'wlin99'
2. ✅ `load_data()` → Loads CSV from GCS
3. ✅ `exclude_no_pickup_locations()` → Filters nulls/zeros in pickup
4. ✅ `exclude_no_trip_distance()` → Filters nulls/zeros in distance
5. ✅ `include_fare_range()` → Filters $20-60 fares
6. ✅ `get_highest_tip()` → Returns max tip as Decimal
7. ✅ `get_total_toll()` → Returns total toll as Decimal

---

## 🔄 **Data Pipeline**

```
load_data()                          → ~45K rows
   ↓
exclude_no_pickup_locations()        → ~44K rows
   ↓
exclude_no_trip_distance()           → ~43K rows
   ↓
include_fare_range()                 → ~12K rows
   ↓
get_highest_tip() / get_total_toll() → Single values
```

---

## 🎯 **Key GCS Path**

Your complete file path:
```
gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv
```

Update this in Cell 20:
```python
gcp_storage_path = "gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv"
```

---

## 💰 **Cost Estimate**

**Single Node Cluster (n1-standard-4):**
- $0.20/hour
- Total: <$0.50 for assignment ✅

**Cloud Storage:**
- 40 MB = $0.001/month (pennies!)

**Remember:** DELETE CLUSTER when done!

---

## ⚠️ **Critical Reminders**

### **Before Submission:**
- [ ] Comment out ALL testing code (cells 20-32)
- [ ] No print/show/display in function bodies
- [ ] All functions use DecimalType(38, 10)
- [ ] Return types are correct (decimal.Decimal for 6 & 7)
- [ ] Downloaded from GCP (not local copy)

### **Cost Savings:**
- [ ] Delete Dataproc cluster immediately
- [ ] Region matches: bucket = us-central1, cluster = us-central1

---

## 🔑 **Key Code Patterns**

### **Cast to Decimal:**
```python
from pyspark.sql.types import DecimalType
df = df.withColumn('column', col('column').cast(DecimalType(38, 10)))
```

### **Filter Nulls & Zeros:**
```python
df = df.filter((col('column').isNotNull()) & (col('column') != 0))
```

### **Aggregation:**
```python
from pyspark.sql.functions import max as spark_max, sum as spark_sum, round as spark_round

# Max
result = df.agg(spark_round(spark_max('column'), 2).alias('max_val')).collect()[0]['max_val']

# Sum
result = df.agg(spark_round(spark_sum('column'), 2).alias('sum_val')).collect()[0]['sum_val']
```

### **Return Decimal:**
```python
return decimal.Decimal(str(result))
```

---

## 🧪 **Testing Commands**

```python
# Load data
gcp_storage_path = "gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv"
df = load_data(gcp_storage_path)
print(f"Original: {df.count()} rows")

# Chain filters
df = exclude_no_pickup_locations(df)
print(f"No pickup nulls: {df.count()} rows")

df = exclude_no_trip_distance(df)
print(f"No distance nulls: {df.count()} rows")

df = include_fare_range(df)
print(f"Fare $20-60: {df.count()} rows")

# Get results
max_tip = get_highest_tip(df)
print(f"Max tip: ${max_tip}")

total_toll = get_total_toll(df)
print(f"Total toll: ${total_toll}")
```

---

## 🆘 **Quick Troubleshooting**

| Problem | Solution |
|---------|----------|
| Cluster won't create | Try us-central1-b or us-east1 |
| "spark" not defined | Select PySpark kernel |
| File not found | Check bucket/file name spelling |
| Can't access Jupyter | Wait 2 min, refresh page |
| High costs | DELETE CLUSTER NOW! |

---

## 📞 **Support**

- **GCP Console:** https://console.cloud.google.com/
- **Dataproc:** https://console.cloud.google.com/dataproc/
- **Cloud Storage:** https://console.cloud.google.com/storage/
- **Ed Discussion:** Post in GCP Setup thread
- **Setup Guide:** Read `GCP_SETUP_GUIDE.md`
- **Code Details:** Read `Q4_IMPLEMENTATION_SUMMARY.md`

---

## 🎓 **What You're Learning**

- **GCP Dataproc:** Google's managed Spark service
- **GCS:** Google Cloud Storage (like S3)
- **PySpark:** Distributed data processing
- **Decimal Precision:** Financial calculations
- **Data Quality:** Filtering nulls and outliers
- **Cloud Computing:** Infrastructure as a Service

---

## 📤 **Submission Checklist**

- [ ] All 7 functions implemented
- [ ] Username is 'wlin99'
- [ ] Tested on full dataset (45K rows)
- [ ] All testing code commented out
- [ ] No debug print/show statements
- [ ] Downloaded q4.ipynb from GCP
- [ ] Cluster deleted (saved money!)
- [ ] Ready to submit to Gradescope ✅

---

## 💡 **Pro Tips**

1. **Single Node is enough** - Cheaper than Standard cluster
2. **Use PySpark kernel** - Not Python3
3. **Comment liberally** - But remove before submission
4. **Test incrementally** - One function at a time
5. **Delete cluster ASAP** - Saves $0.20/hour

---

**Remember: The code is complete! Just follow GCP setup, test, and submit! 🚀**

