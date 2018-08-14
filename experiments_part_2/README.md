# Experiments part 2

Libraries have changed since the first round of experiments.
To avoid having conflicts with different library versions we decided to create a separate project for the following experiments:

- Collect energy usage data of Idle Execution of the Android app under measurement.
- Collect energy usage data of user interface interactions executed by humans.


First time:
```
python3 -m venv venv
source venv/bin/activate
pip install -e git+https://github.com/luiscruz/PyMonsoon@6b5a52fecf40d3a360a82e263d0ffe3cafbce62c#egg=monsoon
pip install -r requirements.txt
python idle_time.py
deactivate
```

After first time:
```
source venv/bin/activate
python idle_time.py
deactivate
```

Results will appear in `results_idle_time.csv`