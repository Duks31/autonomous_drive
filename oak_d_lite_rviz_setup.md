## Configure RViz2 step by step

### Step 1 — Set the Fixed Frame
On the left panel, at the top you'll see **"Fixed Frame"** with a dropdown. Change it from `map` to:
```
camera_optical_link
```
or if that shows errors, use:
```
base_link
```

### Step 2 — Add the RGB Image display
1. Click **"Add"** button at the bottom left
2. Select **"By topic"** tab
3. Find `/camera/color/image_raw` → click **"Image"** under it → click **OK**
4. It will appear as a small image panel in the bottom left of the 3D view

---

### Step 3 — Add the Depth Image display
1. Click **"Add"** again
2. **"By topic"** tab
3. Find `/camera/depth/image_raw` → click **"Image"** under it → click **OK**

---

### Step 4 — Add the Point Cloud display
1. Click **"Add"** again
2. **"By topic"** tab
3. Find `/camera/points` → click **"PointCloud2"** under it → click **OK**
4. In the left panel, expand the **PointCloud2** display and change:
   - **Color Transformer** → `RGB8` (to see colors from the RGB channel)
   - **Size (m)** → `0.02` (makes points more visible)

---

### Step 5 — Add the Robot model
1. Click **"Add"**
2. **"By display type"** tab
3. Select **"RobotModel"** → OK
4. In its settings set **Description Topic** to `/robot_description`

---

### Step 6 — Add TF (optional but useful)
1. Click **"Add"**
2. **"By display type"** → **"TF"** → OK
3. This shows all your coordinate frames including `camera_optical_link`

---

### Step 7 — Save the config so you don't repeat this
```
File → Save Config As → save to your package as  
~/autonomous_ws/src/autonomous_drive/rviz/camera_view.rviz

