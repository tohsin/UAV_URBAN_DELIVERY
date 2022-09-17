# UAV_URBAN_DELIVERY
 A UAV project that impliments several algorithms to perform food delivery in Urban like cities , C University used as test environement

## Sensor Suite
- Mono Camera
- IMU
- Gyroscope
- GPS
- Accelerometer



## Todo
Main sub parts that need too be accomplished
- [ ] Sensor Fusion
- [ ] LSD slam Py
- [ ] Particle filter image scan matching
- [ ] Semantic Segementaion Loop Closure 
- [ ] Drone/ Flight Controller
- [ ] IOS Mobile Device Controller

## SetUp
#### Create Virtual environment
```
python3 -m venv venv
```

#### Add g2o-py binding
```
git clone https://github.com/uoip/g2opy.git
cd g2opy
mkdir build
cd build
cmake ..
make -j8
cd ..
python setup.py install
```

#### Other libtraries
```
pip install -r requirements.txt
```


