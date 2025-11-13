# AWS Setup Guide for Q3

## 🎯 **Goal**
Run your Q3 PySpark notebook on AWS EMR and generate the output CSV from the large dataset.

---

## 🛠️ **Required AWS Services**

1. **S3 (Simple Storage Service)** - For storing output files
2. **EMR (Elastic MapReduce)** - Managed Spark cluster for running notebook

---

## 📋 **Step-by-Step Setup**

---

## **STEP 1: Create S3 Bucket** ⭐ DO THIS FIRST

### 1.1 Go to S3 Console
- URL: https://s3.console.aws.amazon.com/s3/
- Or search "S3" in AWS Console search bar

### 1.2 Create Bucket
1. Click **"Create bucket"** (orange button, top right)
2. **Bucket name:** `cse6242-wlin99` ← Use this EXACT name!
3. **AWS Region:** `US East (N. Virginia) us-east-1` ← IMPORTANT: Match EMR region
4. **Object Ownership:** ACLs disabled (default)
5. **Block Public Access:** Keep all 4 checkboxes CHECKED (recommended)
6. **Bucket Versioning:** Disabled (default)
7. **Encryption:** Server-side encryption with Amazon S3 managed keys (default)
8. Click **"Create bucket"** at bottom

### 1.3 Verify
- You should see `cse6242-wlin99` in your bucket list ✅

**Cost:** ~$0.01 for this entire assignment (pennies!)

---

## **STEP 2: Create EMR Cluster** ⭐ THIS TAKES ~10-15 MIN

### 2.1 Go to EMR Console
- URL: https://console.aws.amazon.com/emr/
- Or search "EMR" in AWS Console

### 2.2 Create Cluster
1. Click **"Create cluster"** (orange button)

### 2.3 Cluster Configuration

#### **Software Configuration:**
- **Release:** `emr-7.0.0` (or latest 7.x version)
- **Applications:** 
  - Check **Spark** ✅
  - Check **JupyterEnterpriseGateway** ✅
  - Uncheck everything else

#### **Hardware Configuration:**
- **Instance type:** `m5.xlarge` (4 vCPU, 16 GB memory)
  - Alternative if unavailable: `m4.xlarge` or `m5.large`
- **Number of instances:** `3`
  - 1 Primary (master)
  - 2 Core (workers)

#### **Cluster Scaling:**
- Leave as default (no auto-scaling needed for this assignment)

#### **Networking:**
- **VPC:** Default VPC (should be auto-selected)
- **Subnet:** Any available subnet
- **EC2 Security Groups:** Default EMR groups (auto-created)

#### **Cluster Logs:**
- **S3 folder for logs:** `s3://cse6242-wlin99/logs/`
- This helps with debugging if something fails

#### **Security and Access:**
- **EC2 key pair:** 
  - If you have one: Select it
  - If you DON'T: Click "Create new key pair"
    - Name: `hw3-emr-key`
    - Download and save the .pem file
    - You might not need it, but AWS requires it

#### **Identity and Access Management (IAM) Roles:**
- **Service role:** `EMR_DefaultRole` (auto-created)
- **Instance profile:** `EMR_EC2_DefaultRole` (auto-created)
- If these don't exist, AWS will offer to create them - click "Create"

### 2.4 Launch Cluster
1. Scroll down and click **"Create cluster"**
2. **Wait 10-15 minutes** for cluster state to change from "Starting" → **"Waiting"**
3. **"Waiting" = Ready to use** ✅

### 2.5 Verify
- Cluster status shows **"Waiting"** (green)
- You can click on cluster name to see details

**Cost:** ~$0.50-0.75 per hour for 3 x m5.xlarge instances

---

## **STEP 3: Upload Notebook to EMR**

### 3.1 Navigate to Notebooks
1. In EMR Console, click **"Notebooks"** in left sidebar
2. Or click on your cluster → **"Notebooks"** tab

### 3.2 Create Notebook in EMR
1. Click **"Create notebook"**
2. **Notebook name:** `q3`
3. **Notebook location:** `s3://cse6242-wlin99/notebooks/`
4. **Choose "Attach to an EMR cluster"**
5. **Select your cluster** from dropdown
6. Click **"Create notebook"**
7. Wait 1-2 minutes for notebook to be "Ready"

### 3.3 Upload Your Notebook
1. Click on notebook name (`q3`)
2. Click **"Open in JupyterLab"** (or "Open")
3. In JupyterLab interface:
   - Click **Upload** button (top left)
   - Select `/Users/mxy1998/Documents/rileygit/6242_hw1/hw3/Q3/q3.ipynb`
   - Upload and replace if asked

### 3.4 Alternative: Copy-Paste Code
If upload doesn't work:
1. Open the blank notebook in JupyterLab
2. Create cells manually
3. Copy-paste code from your local `q3.ipynb`

---

## **STEP 4: Test with Small Dataset**

### 4.1 Run Setup Cells
In the notebook, run these cells in order:
1. Cell 3: Imports
2. Cell 4: Helper functions (`load_data`, `main`)
3. Cells 7, 9, 11, 13, 15, 17: Your function implementations

### 4.2 Load Small Data
Run Cell 21:
```python
trips, zones = load_data('small')
```
Should complete in ~30 seconds

### 4.3 Test Functions Individually
Add a new cell and test:
```python
# Test each function
print("User:", user())
trip_statistics(trips).show()
busiest_hour(trips).show()
most_freq_pickup_locations(trips).show()
avg_trip_distance_and_duration(trips).show(24)
most_freq_peak_hour_fares(trips, zones).show()
```

### 4.4 Fix Any Errors
If you see errors:
- Check cell output for error messages
- Verify column names in error messages
- Run `trips.printSchema()` to see available columns

---

## **STEP 5: Run on Large Dataset** 🚀

### 5.1 Run Main Function
Cell 23 (already configured):
```python
main('large', 's3://cse6242-wlin99')
```

### 5.2 Wait for Completion
- Small dataset: ~1-2 minutes
- **Large dataset: ~10-30 minutes** ⏰
- Watch the progress bar
- Don't close your browser (or it's fine if you do - job continues)

### 5.3 Check for Completion
You'll see:
```
User: wlin99

Trip Statistics:
+-------+------------------+
|summary|     trip_distance|
+-------+------------------+
...

Most Frequent Peak Hour Fares:
+------------+------+------------+------+----------+--------------+
|PULocationID|PUZone|DOLocationID|DOZone|trip_count|avg_total_fare|
+------------+------+------------+------+----------+--------------+
...
```

---

## **STEP 6: Download Output CSV from S3**

### 6.1 Go to S3 Console
- Navigate to your bucket: `cse6242-wlin99`

### 6.2 Find Output
- Folder: `output_large/`
- File: `part-00000-<random-id>.csv` (with a long random ID)
- There might be other files like `_SUCCESS` - ignore those

### 6.3 Download
1. Click on the CSV file (not the folder)
2. Click **"Download"** button
3. Save to your computer

### 6.4 Rename
Rename the downloaded file to:
```
q3_output_large.csv
```

### 6.5 Verify Contents
Open in Excel or text editor:
- Should have **11 rows total** (1 header + 10 data rows)
- Columns: PULocationID, PUZone, DOLocationID, DOZone, trip_count, avg_total_fare
- Example:
```csv
PULocationID,PUZone,DOLocationID,DOZone,trip_count,avg_total_fare
237,Upper East Side South,236,Upper East Side North,1234,45.67
...
```

---

## **STEP 7: Download Notebook from EMR**

### 7.1 Export from JupyterLab
In EMR JupyterLab interface:
1. Right-click on your notebook (`q3.ipynb`)
2. Select **"Download"**
3. Save to `/Users/mxy1998/Documents/rileygit/6242_hw1/hw3/Q3/`

### 7.2 Alternative: Download from S3
The notebook is also saved in S3:
- Path: `s3://cse6242-wlin99/notebooks/q3.ipynb`
- Download from S3 Console

---

## **STEP 8: TERMINATE CLUSTER** ⚠️ CRITICAL!

### 8.1 Why Terminate?
- EMR charges ~$0.50-0.75 **PER HOUR**
- If you leave it running overnight: $12-18 wasted!
- Always terminate when done

### 8.2 How to Terminate
1. Go to EMR Console
2. Click **"Clusters"** in left sidebar
3. **Select your cluster** (checkbox)
4. Click **"Terminate"** (top right)
5. Click **"Terminate"** again to confirm
6. Wait 2-3 minutes for status to change to "Terminated"

### 8.3 Verify
- Cluster status: **"Terminated"** ✅
- You can still see it in the list (for records)
- But it's NO LONGER CHARGING YOU 💰

### 8.4 Keep S3 Bucket
- Don't delete your S3 bucket yet
- S3 costs pennies (unlike EMR)
- Good to keep for records/verification

---

## **STEP 9: Submit to Gradescope**

Submit these 2 files:
1. ✅ `q3.ipynb` - Your completed notebook
2. ✅ `q3_output_large.csv` - Output from large dataset

---

## 🔧 **Troubleshooting Common Issues**

### **Issue 1: Cluster won't start**
**Error:** "Cannot create cluster: insufficient capacity"
**Fix:** 
- Try different instance type: m4.xlarge or m5.large
- Try different region: us-west-2
- Try different availability zone

### **Issue 2: "Access Denied" when writing to S3**
**Error:** "Access Denied" or "403 Forbidden"
**Fix:**
- Check EMR IAM roles have S3 write permissions
- Verify bucket name is correct: `cse6242-wlin99`
- Ensure bucket and EMR are in same region

### **Issue 3: Notebook won't open**
**Error:** "Cannot connect to notebook"
**Fix:**
- Wait 2-3 minutes after creation
- Check security groups allow access
- Try different browser (Chrome/Firefox/Safari)
- Clear browser cache

### **Issue 4: Code runs forever**
**Symptom:** Cell shows [*] for >1 hour
**Fix:**
- Check cluster is still running (not terminated)
- Look at Spark UI for job progress
- Check EMR logs in S3
- Restart kernel and try again

### **Issue 5: Out of memory**
**Error:** "OutOfMemoryError" or "Java heap space"
**Fix:**
- Increase instance size to m5.2xlarge
- Increase number of core instances to 4
- Add `.coalesce(1)` before operations

---

## 💰 **Cost Breakdown**

### **S3 Storage:**
- Storage: $0.023 per GB/month
- Your data: <1 GB
- **Cost: <$0.10 total**

### **EMR Cluster (3 x m5.xlarge):**
- EC2 cost: $0.192/hr × 3 = $0.576/hr
- EMR cost: $0.070/hr × 3 = $0.210/hr
- **Total: ~$0.79/hour**

### **Estimated Total:**
- Setup + testing: 1 hour = $0.79
- Large dataset run: 0.5 hour = $0.40
- Buffer time: 1 hour = $0.79
- **Total: ~$2-3 if you work efficiently**

### **If you forget to terminate:**
- 24 hours = $19 💸
- **Always terminate when done!**

---

## ⏱️ **Time Estimates**

| Task | Time |
|------|------|
| Create S3 bucket | 2 minutes |
| Create EMR cluster | 10-15 minutes (waiting) |
| Upload notebook | 2 minutes |
| Test with small data | 5-10 minutes |
| Run large dataset | 10-30 minutes |
| Download outputs | 5 minutes |
| Terminate cluster | 2 minutes |
| **Total** | **~45-75 minutes** |

---

## ✅ **Pre-Flight Checklist**

Before you start:
- [ ] Have AWS account with credits or payment method
- [ ] Know your GT username: `wlin99`
- [ ] Have `q3.ipynb` ready in local folder
- [ ] Know your AWS region (recommend: us-east-1)
- [ ] Have 1-2 hours of uninterrupted time

---

## 🎯 **Quick Reference**

**Your S3 Bucket:** `cse6242-wlin99`

**Data Source:** `s3://cse6242-hw3-q3` (pre-provided, don't change)

**EMR Settings:**
- Release: emr-7.x
- Apps: Spark + JupyterEnterpriseGateway  
- Instances: 3 × m5.xlarge

**Output Location:** `s3://cse6242-wlin99/output_large/`

**When Done:** TERMINATE CLUSTER! ⚠️

---

**Good luck! You've got this! 🚀**

