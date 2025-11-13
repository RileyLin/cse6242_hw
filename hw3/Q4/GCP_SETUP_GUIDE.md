# GCP Setup Guide for Q4

## 🎯 **Goal**
Run your Q4 PySpark notebook on Google Cloud Platform (GCP) using Dataproc (managed Spark).

---

## 📋 **Prerequisites**

Before you start:
- [ ] Have a Google account
- [ ] GCP free credits activated ($300 for new users)
- [ ] Chrome, Firefox, or Safari browser
- [ ] Downloaded `yellow_tripdata09-08-2021.csv` from DropBox

---

## 🚀 **Step-by-Step Setup**

---

## **STEP 1: Activate GCP Free Credits** 💳

### 1.1 Go to GCP Console
- URL: https://console.cloud.google.com/
- Sign in with your Google account

### 1.2 Activate Free Trial
1. Click **"Activate"** or **"Try for free"** in the top banner
2. **Country:** United States
3. **Terms of Service:** Check the box
4. Click **"Continue"**
5. **Enter billing information:**
   - Credit/debit card required (won't be charged without permission)
   - Address information
6. Click **"Start my free trial"**

### 1.3 Verify Credits
- Top navigation: Check for **"$300 credit"** indicator
- You have 90 days to use these credits
- This assignment costs <$5

---

## **STEP 2: Create a GCP Project** 📁

### 2.1 Create Project
1. Click project dropdown (top left, next to "Google Cloud")
2. Click **"NEW PROJECT"**
3. **Project name:** `hw3-q4-wlin99` (or any name you like)
4. **Organization:** Leave as "No organization"
5. Click **"CREATE"**
6. Wait ~30 seconds for project creation

### 2.2 Select Project
1. Click project dropdown again
2. Select your new project: `hw3-q4-wlin99`
3. **Verify:** Top bar shows your project name ✅

---

## **STEP 3: Enable Required APIs** 🔌

### 3.1 Enable Dataproc API
1. Search for **"Dataproc"** in the top search bar
2. Click **"Dataproc API"**
3. Click **"ENABLE"**
4. Wait ~1-2 minutes

### 3.2 Enable Compute Engine API (Auto-enabled)
- Should enable automatically when you create Dataproc cluster
- If asked, click "Enable"

### 3.3 Enable Cloud Storage API
1. Search for **"Cloud Storage"** in top search bar
2. Click **"Cloud Storage API"**
3. Click **"ENABLE"** (if not already enabled)

---

## **STEP 4: Create Cloud Storage Bucket** 🪣

### 4.1 Go to Cloud Storage
1. Click **☰** (hamburger menu, top left)
2. Navigate to **Storage → Cloud Storage → Buckets**
3. Or search "Cloud Storage" in top search bar

### 4.2 Create Bucket
1. Click **"CREATE"** (blue button, top)
2. **Name your bucket:** `cse6242-wlin99-hw3q4`
   - Must be globally unique
   - Use lowercase, numbers, hyphens only
   - If taken, try: `cse6242-wlin99-hw3q4-2024`
3. **Choose where to store your data:**
   - Location type: **Region**
   - Location: **us-central1** (Iowa) - cheapest!
4. **Choose a default storage class:**
   - **Standard** (default, keep it)
5. **Choose how to control access:**
   - **Uncheck** "Enforce public access prevention"
   - **Uniform** (default, keep it)
6. **Data protection:**
   - Leave all defaults (no versioning, no retention)
7. Click **"CREATE"**
8. Click **"CONFIRM"** if warned about public access

### 4.3 Verify Bucket
- You should see `cse6242-wlin99-hw3q4` in your bucket list ✅

---

## **STEP 5: Upload Data to Cloud Storage** ⬆️

### 5.1 Navigate to Your Bucket
1. Click on your bucket name: `cse6242-wlin99-hw3q4`
2. You should see an empty bucket

### 5.2 Upload CSV File
1. Click **"UPLOAD FILES"** (blue button)
2. Select `yellow_tripdata09-08-2021.csv` from your computer
3. Wait for upload to complete (~1-2 minutes for ~40MB file)
4. **Verify:** You see the file listed ✅

### 5.3 Note the GCS Path
Your file path is:
```
gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv
```
**Copy this path** - you'll need it later!

---

## **STEP 6: Create Dataproc Cluster** 🖥️

### 6.1 Go to Dataproc
1. Click **☰** (hamburger menu)
2. Navigate to **Dataproc → Clusters**
3. Or search "Dataproc" in top search bar

### 6.2 Create Cluster
1. Click **"CREATE CLUSTER"** (blue button)
2. Choose **"Cluster on Compute Engine"**

### 6.3 Configure Cluster

#### **Set up cluster - Basic:**
- **Cluster name:** `hw3-q4-cluster`
- **Region:** `us-central1` (must match your bucket!)
- **Zone:** `us-central1-a` (or any zone in us-central1)
- **Cluster type:** **Single Node** (cheapest for homework!)
  - ⚠️ Or **Standard** if Single Node not available (1 master + 2 workers)

#### **Configure nodes:**

**For Single Node cluster:**
- **Machine type:** `n1-standard-4` (4 vCPUs, 15 GB memory)
- **Primary disk size:** 50 GB

**For Standard cluster (if Single Node unavailable):**
- **Master node:**
  - Series: N1
  - Machine type: `n1-standard-2` (2 vCPUs, 7.5 GB)
  - Primary disk size: 50 GB
- **Worker nodes:**
  - Number of workers: **2**
  - Machine type: `n1-standard-2`
  - Primary disk size: 50 GB

#### **Customize cluster → Optional components:**
- **Check:** ✅ **Jupyter Notebook**
- **Check:** ✅ **Component gateway** (auto-checked)

#### **Manage security → Project access:**
- **Allow API access:** Checked (default)

### 6.4 Create Cluster
1. Click **"CREATE"** at the bottom
2. **Wait 2-5 minutes** for cluster to provision
3. Status will change from "Provisioning" → **"Running"** ✅

---

## **STEP 7: Upload Notebook to Dataproc** 📓

### 7.1 Access JupyterLab
1. In Dataproc Clusters page, find your cluster: `hw3-q4-cluster`
2. Click on the cluster name
3. In the cluster details page, click **"WEB INTERFACES"** tab
4. Click **"Jupyter"** link (opens in new tab)
5. JupyterLab interface loads

### 7.2 Upload Notebook
1. In JupyterLab, click **upload icon** (↑ arrow) in left sidebar
2. Or drag-and-drop `q4.ipynb` from your computer
3. File appears in file browser

### 7.3 Open Notebook
1. Double-click `q4.ipynb` to open
2. **Kernel:** Should automatically use **PySpark** kernel
3. If asked to select kernel, choose **PySpark**

---

## **STEP 8: Update Notebook with Your GCS Path** 📝

### 8.1 Find the Testing Cell
- Scroll to Cell 20 (the commented testing code)

### 8.2 Uncomment and Update
```python
# Original (commented):
#gcp_storage_path = "gs://<replace_with_your_storage_bucket>/yellow_tripdata09-08-2021.csv"

# Update to YOUR bucket:
gcp_storage_path = "gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv"
```

### 8.3 Uncomment Testing Cells (Cells 20-32)
Remove the `#` from the beginning of each line to test your functions:

```python
# Cell 20-22: Load and count
gcp_storage_path = "gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv"
df = load_data(gcp_storage_path)
df.printSchema()
df.count()

# Cell 24: Test exclude_no_pickup_locations
df_no_pickup_locations = exclude_no_pickup_locations(df)
df_no_pickup_locations.count()

# Cell 26: Test exclude_no_trip_distance
df_no_trip_distance = exclude_no_trip_distance(df_no_pickup_locations)
df_no_trip_distance.count()

# Cell 28: Test include_fare_range
df_include_fare_range = include_fare_range(df_no_trip_distance)
df_include_fare_range.count()

# Cell 30: Test get_highest_tip
max_tip = get_highest_tip(df_include_fare_range)
print(max_tip)

# Cell 32: Test get_total_toll
total_toll = get_total_toll(df_include_fare_range)
print(total_toll)
```

---

## **STEP 9: Test Your Implementation** 🧪

### 9.1 Run Cells One by One
1. Click on Cell 5 (`user()` function)
2. Press **Shift+Enter** to run
3. Continue through all function cells (5, 7, 9, 11, 13, 15, 17)
4. **Verify:** No errors ✅

### 9.2 Run Testing Cells
1. Run Cell 20 (load data)
   - Should see schema printed
   - Count: ~45,000-50,000 rows
2. Run Cell 24 (exclude no pickup)
   - Count should decrease slightly
3. Run Cell 26 (exclude no distance)
   - Count should decrease more
4. Run Cell 28 (fare range)
   - Count should decrease significantly (~10,000-15,000 rows)
5. Run Cell 30 (highest tip)
   - Should print a decimal number (e.g., `73.45`)
6. Run Cell 32 (total toll)
   - Should print a decimal number (e.g., `12345.67`)

### 9.3 Verify Results
- All cells run without errors ✅
- Counts decrease at each filtering step ✅
- Final values are decimal.Decimal type ✅

---

## **STEP 10: Prepare for Submission** 📤

### 10.1 Comment Out All Testing Code
**CRITICAL:** Before submission, comment out ALL testing code (Cells 20-32):

```python
# Cell 20-22
#gcp_storage_path = "gs://cse6242-wlin99-hw3q4/yellow_tripdata09-08-2021.csv"
#df = load_data(gcp_storage_path)
#df.printSchema()
#df.count()

# Cell 24
#df_no_pickup_locations = exclude_no_pickup_locations(df)
#df_no_pickup_locations.count()

# ... etc for all testing cells
```

**Why?** The autograder will crash if you have print/show statements!

### 10.2 Download Notebook
1. In JupyterLab, right-click on `q4.ipynb` in file browser
2. Select **"Download"**
3. Save to `/Users/mxy1998/Documents/rileygit/6242_hw1/hw3/Q4/`

### 10.3 Verify Downloaded File
- Open `q4.ipynb` in your local editor
- Check that all testing code is commented out
- Check that all 7 functions are implemented

---

## **STEP 11: Delete Cluster to Save Costs** 💰

### 11.1 Stop Cluster
1. Go back to **Dataproc → Clusters**
2. **Select** your cluster (checkbox)
3. Click **"DELETE"** (top toolbar)
4. Confirm deletion
5. Wait ~1 minute for deletion

### 11.2 Keep Bucket (Optional)
- You can keep the bucket (costs pennies)
- Or delete it: Go to **Cloud Storage → Buckets** → Select → Delete

---

## 💰 **Cost Breakdown**

### **Single Node Cluster (n1-standard-4):**
- Compute: ~$0.19/hour
- Dataproc: ~$0.01/hour
- **Total: ~$0.20/hour**

### **Standard Cluster (1 master + 2 workers, n1-standard-2):**
- Compute: 3 × $0.095/hour = $0.285/hour
- Dataproc: 3 × $0.01/hour = $0.03/hour
- **Total: ~$0.32/hour**

### **Estimated Total Cost:**
- Setup + testing: 1 hour = $0.20-0.32
- Buffer: 0.5 hour = $0.10-0.16
- **Total: <$0.50** if you delete cluster promptly! ✅

### **Cloud Storage:**
- 40 MB file = $0.001/month (pennies!)

---

## ⚠️ **Common Mistakes to Avoid**

❌ **Wrong region for bucket vs cluster**
- Bucket: us-central1
- Cluster: us-central1
- Must match or you pay data transfer fees!

❌ **Forgetting to delete cluster**
- Cost: $0.20-0.32 per hour
- 24 hours = $5-8 wasted! 💸

❌ **Not selecting PySpark kernel**
- Notebook won't work with Python3 kernel
- Always use PySpark!

❌ **Leaving testing code uncommented**
- Autograder will crash
- Always comment out before submission!

❌ **Using float instead of decimal**
- Requirements specify decimal.Decimal
- Will fail autograder!

---

## ✅ **Pre-Flight Checklist**

Before starting:
- [ ] GCP account with free credits activated
- [ ] Chrome/Firefox/Safari browser
- [ ] `yellow_tripdata09-08-2021.csv` downloaded
- [ ] `q4.ipynb` with all functions implemented
- [ ] 1-2 hours of uninterrupted time

Before submitting:
- [ ] All 7 functions implemented
- [ ] Tested on full dataset
- [ ] All testing code commented out
- [ ] No print/show/display statements in function cells
- [ ] Notebook downloaded from GCP
- [ ] Cluster deleted

---

## 🆘 **Troubleshooting**

### **Issue 1: "GCP services disabled"**
**Error:** Services are disabled for your account
**Fix:** Follow this link: https://support.google.com/cloud/answer/6293596

### **Issue 2: Cluster creation fails**
**Error:** Quota exceeded or no capacity
**Fix:**
- Try different zone: us-central1-b or us-central1-c
- Try different region: us-east1 (remember to move bucket too!)

### **Issue 3: Can't access Jupyter**
**Error:** Jupyter link doesn't open
**Fix:**
- Wait 1-2 minutes after cluster is "Running"
- Check browser allows popups
- Try different browser (Chrome recommended)
- Click refresh on cluster details page

### **Issue 4: "spark" is not defined**
**Error:** NameError: name 'spark' is not defined
**Fix:**
- Make sure you selected **PySpark** kernel
- Restart kernel and try again
- Go to Kernel → Change Kernel → PySpark

### **Issue 5: File not found**
**Error:** Path does not exist: gs://...
**Fix:**
- Check bucket name spelling
- Check file name spelling (case-sensitive!)
- Verify file uploaded successfully in Cloud Storage UI

---

## 📞 **Support Resources**

- **GCP Free Trial:** https://cloud.google.com/free
- **Dataproc Docs:** https://cloud.google.com/dataproc/docs
- **GCP Console:** https://console.cloud.google.com/
- **Ed Discussion:** Post in GCP Setup thread

---

**Good luck! Remember to delete your cluster when done! 🚀**

