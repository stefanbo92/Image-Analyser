# Image-Analyser

Program for identifying and counting user specified objects in an image.

## Usage:
First rename the image to analyse to "img.png" and then run

```{r, engine='bash', count_lines}
python analyser.py
```

Specify the object you want to detect and count by selecting it with a bounding rectangel. The brogram will then show all of these objects and count them.
For now the object detection only works with a simple template matching. In the future a neural network should be implemented for more robust object detection.

OpenCV and Scipy are required for running the python script.


## Examples:

![qAAMg2](http://i.makeagif.com/media/12-29-2016/qAAMg2.gif)


![dANrFV](http://i.makeagif.com/media/12-29-2016/dANrFV.gif)
