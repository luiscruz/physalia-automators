# On the Energy Footprint of Mobile Testing Frameworks

Project to compare UI Automated interaction frameworks.

**Submitted to the IEEE Transactions on Software Engineering**

### Requirements

- Android SDK installed
- UI automation frameworks:
  - [Android View Client](https://github.com/dtmilano/AndroidViewClient)
  - [Calabash Android](https://calaba.sh/)
- Monsoon Power Monitor
- Android Device with root permissions connected to the power monitor (we use Nexus 5X)

### Notes

Set screen brightness to 30.5\% (78/255):

```
adb shell settings put system screen_brightness 78
```
