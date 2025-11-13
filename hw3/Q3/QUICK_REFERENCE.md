# Q3 Quick Reference Card

## 📋 **Essential Info**

**Your GT Username:** `wlin99`  
**Your S3 Bucket:** `cse6242-wlin99`  
**Data Source:** `s3://cse6242-hw3-q3` (pre-provided)  
**AWS Region:** `us-east-1` (recommended)

---

## 🚀 **Quick Start (5 Steps)**

### 1️⃣ Create S3 Bucket
```
Name: cse6242-wlin99
Region: us-east-1
Settings: Default (block public access)
```

### 2️⃣ Create EMR Cluster
```
Release: emr-7.x
Apps: Spark + JupyterEnterpriseGateway
Instances: 3 × m5.xlarge
Wait: ~10-15 min until "Waiting" status
```

### 3️⃣ Upload Notebook
```
EMR Console → Notebooks → Create notebook
Name: q3
Upload: q3.ipynb from local folder
```

### 4️⃣ Run Large Dataset
```python
main('large', 's3://cse6242-wlin99')
```
Wait ~10-30 minutes

### 5️⃣ Download & Submit
```
S3 → cse6242-wlin99 → output_large/ → download CSV
Rename to: q3_output_large.csv
Submit: q3.ipynb + q3_output_large.csv
```

---

## ⚠️ **CRITICAL: Terminate Cluster When Done!**
```
EMR Console → Select cluster → Terminate
Cost: ~$0.79/hour if running!
```

---

## 📁 **Files Created**

| File | Description |
|------|-------------|
| `q3.ipynb` | ✅ All 6 functions implemented |
| `Q3_IMPLEMENTATION_SUMMARY.md` | Detailed code explanations |
| `AWS_SETUP_GUIDE.md` | Step-by-step AWS instructions |
| `QUICK_REFERENCE.md` | This cheat sheet |

---

## ✅ **What's Implemented**

1. ✅ `user()` → Returns 'wlin99'
2. ✅ `trip_statistics()` → Describes trip_distance
3. ✅ `busiest_hour()` → Hour with most trips
4. ✅ `most_freq_pickup_locations()` → Top 10 pickup locations
5. ✅ `avg_trip_distance_and_duration()` → Averages by hour (24 rows)
6. ✅ `most_freq_peak_hour_fares()` → Top 10 peak hour routes with zone names

---

## 🧪 **Testing Commands**

```python
# Load small data
trips, zones = load_data('small')

# Test each function
user()  # Returns 'wlin99'
trip_statistics(trips).show()
busiest_hour(trips).show()
most_freq_pickup_locations(trips).show()
avg_trip_distance_and_duration(trips).show(24)
most_freq_peak_hour_fares(trips, zones).show()

# Run full pipeline on large
main('large', 's3://cse6242-wlin99')
```

---

## 💰 **Cost Estimate**

- **S3:** <$0.10 (pennies)
- **EMR:** ~$0.79/hour
- **Total:** $2-3 (if efficient)
- **If left running overnight:** $19+ 💸

---

## 📤 **Submission Checklist**

- [ ] `q3.ipynb` (notebook with all functions)
- [ ] `q3_output_large.csv` (10 rows + header)
- [ ] Verified CSV has correct columns
- [ ] EMR cluster terminated

---

## 🆘 **Quick Troubleshooting**

| Problem | Solution |
|---------|----------|
| Cluster won't start | Try m4.xlarge or different region |
| Access Denied to S3 | Check IAM roles, bucket name |
| Code runs forever | Check cluster status, look at Spark UI |
| Out of memory | Increase to m5.2xlarge |
| Can't download CSV | Check S3 → output_large/ folder |

---

## 📞 **Support**

- **AWS Setup:** Read `AWS_SETUP_GUIDE.md`
- **Code Details:** Read `Q3_IMPLEMENTATION_SUMMARY.md`
- **AWS Console:** https://console.aws.amazon.com/
- **S3 Console:** https://s3.console.aws.amazon.com/
- **EMR Console:** https://console.aws.amazon.com/emr/

---

**Remember: TERMINATE YOUR CLUSTER when done! ⚠️**

