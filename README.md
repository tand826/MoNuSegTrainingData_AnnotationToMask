# MoNuSegTrainingData_AnnotationToMask
Script to make mask images of MoNuSegTrainingData

# Notion
- Output masks don't represents exactly the same coordinates as the annotation xml files because cv2.drawContours gets the contours coordinates as integer while the xml files have the coordinates with precision below the decimal point.

# Dataset
https://monuseg.grand-challenge.org/Data/

# Run the script
```python
python anno_to_mask.py [root directory of MoNuSegTrainingData]
```

Then the script saves masks in "MoNuSegTrainingData"/masks