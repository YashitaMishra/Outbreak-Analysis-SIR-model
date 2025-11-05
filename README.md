# Outbreak-Analysis-SIR-model
I used the SIR model to compare spread of the covid outbreak between vaccinated and unvaccinated populations. This model was created as a DIY project for the course BIO-3636-1 during Summer 2025 at Ashoka University.
Instructions for running Python Script:
Make sure that you have the modules pandas and matplotlib.pyplot. 
You can check this by running the commands:

import pandas
import matplotlib.pyplot 

If your terminal doesn’t display any error messages then run the code from the attached python script. 

If it shows an error message, run these lines in your terminal.

If pandas is not present use the following command:

pip install pandas

If matplotlib is not present, use the following command:

pip install matplotlib


Additional comments:
Source for dataset for covid — https://www.kaggle.com/datasets/sudalairajkumar/covid19-in-india?resource=download&select=covid_19_india.csv

The file output.png shows the plots that the code produces. For other values and rates of infections you can tweak the respective values and get plots accordingly. This model can be used for other datasets as well.

The code will be updated periodically and the newest version will be reflected under updatedsir.py. The original code will be attached along with the original output. The current updates to the original code are as follows:
There are no longer any guardrails to limit the number of days to 200. I have only used the date of the first vaccination rollout to seperate it into the groups of vaccinated and unvaccinated. Though this does cause an unevenness in the number of days (this is also printed using the commands : print(f"Unvaccinated data size: {len(unvaccinated_data)} days") print(f"Vaccinated data size: {len(vaccinated)} days")).
