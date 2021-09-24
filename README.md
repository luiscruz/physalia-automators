# On the Energy Footprint of Mobile Testing Frameworks

Project to compare UI Automated interaction frameworks.

**[Accepted in IEEE Transactions on Software Engineering](https://luiscruz.github.io/publications/2019-12-cruz-uiframeworks.html)**

### Requirements

- Android SDK installed
- UI automation frameworks:
  - [Android View Client](https://github.com/dtmilano/AndroidViewClient)
  - [Calabash Android](https://calaba.sh/)
- Monsoon Power Monitor
- Android Device with root permissions connected to the power monitor (we use Nexus 5X)

### Setup

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run

Make sure your device is connected to the Power Monitor.
After starting the scripts, the Power Monitor will power the device with 3.7V.
At this point, you will be asked to turn the device on.
The scripts will wait for the device to be ready and will start the experiments automatically.

```
source venv/bin/activate
python physalia_automators/cli.py
```

### Reports

Generate reports with the comparison between different frameworks and interactions.
```
source venv/bin/activate
python physalia_automators/reports.py -o <REPORTS_DIR>
```

### Notes

Set screen brightness to 30.5\% (78/255):

```
adb shell settings put system screen_brightness 78
```
