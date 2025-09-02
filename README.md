![Deployment Image](Deployment.png)

## 🛠️ Installation  
Make sure you have Python installed, then install dependencies:  

```bash
pip install torch torchvision opencv-python numpy
```

## 🚀 Run the Script  
Simply execute:  

```bash
python main.py
```

> 🎥 **Make sure to update the path to your input video inside the script!**  

## 🖼️ Sample Output  
The output video will display:  
🔹 **Detected vehicles** with a **yellow bounding box**  
🔹 **Speed overlay** in **bold yellow text**  
🔹 **Tracking of vehicles over time**  

## 📂 File Structure  
```
📁 Car_Speed_Detection_Using_YOLOv5
 ├── main.py  # The main script
 ├── detected_video.mp4  # Processed output video
 ├── README.md  # Project documentation
 ├── requirements.txt  # List of dependencies
```

## 📝 Notes  
-with enough data if it can train then that perform better on all image
- Adjust the `scale` variable for better speed estimation 🎯  
- The script tracks vehicles based on their movement over frames 🚥  
- Press **'Q'** to exit the video display window manually ❌  

## 🤝 Contribution  
Feel free to **fork** and improve the project! PRs are welcome. 🙌  

