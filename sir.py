import pandas as pd    #Since the data is in a csv file, pandas helps with accessing data better.
import matplotlib.pyplot as plt  #To plot the graphs for the different cases better.
data = pd.read_csv("covid_19_india.csv") #Accessing the data easily since it is stored in a variable making it easy to re-use.
print(data.columns) #-> done to check the names of columns
# Converting the 'Date' column to datetime format so that it can be sorted into vaccinated and unvaccinated groups.
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)   #dayfirst=True is used if the format is DD-MM-YYYY
unvaccinated_data = data[(data['Date'] <= "2020-08-17") & (data['State/UnionTerritory'] == 'Kerala')] #Gives the data for 200 days of populations that didn't have access to vaccines in the state of Kerala.
# The same thing is done for the vaccinated populations. 
vaccinated = data[(data['Date'] >= "2021-01-16") & (data['Date'] <= "2021-08-04") &(data['State/UnionTerritory'] == 'Kerala')]
N_Kerala = 35500000 #initial population of Kerala in 2020 
# Actual Data UNVACCINATED
accI = unvaccinated_data.iloc[0]['Confirmed'] #Initial value for infected number of persons pre-vaccination
accR = unvaccinated_data.iloc[0]['Cured']     #Initial value for recovered number of persons pre-vaccination
accD = unvaccinated_data.iloc[0] ['Deaths']   #Initial value for dead number of persons pre-vaccination
newS = N_Kerala #Initial population for the state of Kerala
unvaccI, unvaccR,unvaccS = [],  [], [] #Empty lists initialised for the values of S, I and R.
for i in range(len(unvaccinated_data)):
    newI = unvaccinated_data.iloc[i]['Confirmed']
    newR = unvaccinated_data.iloc[i]['Cured']
    newD = unvaccinated_data.iloc[i]['Deaths']
    accI = newI - unvaccinated_data.iloc[i-1]['Confirmed']
    accR = newR - unvaccinated_data.iloc[i-1]['Cured']
    accD = newD - unvaccinated_data.iloc[i-1] ['Deaths']
    newS -= (accI + accR + accD)
    unvaccI.append(accI)
    unvaccR.append(accR)
    unvaccS.append(newS)
''' The above block of code takes in the length of the unvaccinated data and iterates over it.
The values newI, newR, newD take in the values of the Confirmed, Cured and Dead of that iteration.
Using this value, I calculate the actual values of S, I and R by subtracting the previous values of Confirmed, Cured and Dead.
I do this since the values of S, I and R in the dataset are cumulative. So, they don't give the values of daily cases, recoveries and deaths.
I then update the susceptible population to the previous susceptible population - (those who were infected today + those who have recovered + the number of deaths).
I do this since those who have been infected develop some immunity, as well as those who have recovered. And the population reduces as certain individuals have died.
I then append the values of those actually infected, those who have recovered and update the population as well.
They are put into lists so that they can be plotted. '''
# Actual Data VACCINATED
accIV = vaccinated.iloc[0]['Confirmed'] #Initial value for infected number of persons post-vaccination
accRV = vaccinated.iloc[0]['Cured']     #Initial value for recovered number of persons post-vaccination
accDV = vaccinated.iloc[0] ['Deaths']   #Initial value for number of deaths post-vaccination
newSV = N_Kerala
vaccI,vaccR,vaccS = [],  [], []
for i in range(len(vaccinated)):
    newIV = vaccinated.iloc[i]['Confirmed']
    newRV = vaccinated.iloc[i]['Cured']
    newDV = vaccinated.iloc[i] ['Deaths']
    accIV = newIV - vaccinated.iloc[i-1]['Confirmed']
    accRV = newRV - vaccinated.iloc[i-1]['Cured']
    accDV = newDV - vaccinated.iloc[i-1] ['Deaths']
    newSV -= (accIV + accRV +accDV)
    vaccI.append(newIV)
    vaccR.append(newRV)
    vaccS.append(newSV)
'''The above code block works similarly to the unvaccinated code block but instead takes the values from the vaccinated group. '''
#Expected SIR graph for vaccinated group 
b = 0.7 #Rate of transmission, value taken from the newer strain of covid in the UK. Source: https://www.rnz.co.nz/news/world/433956/new-covid-19-variant-raises-transmission-r-number-by-up-to-0-7
g = 0.6235 #Assuming that each person is covid positive for an average of 14 days 
R0 = b/g #Rate of reproduction
print(f"Reproduction Number R0 vaccinated= {R0:.2f}")

# Initial values from first day of vaccinated data
I0 = vaccinated.iloc[0]['Confirmed']
R0_init = vaccinated.iloc[0]['Cured']
S0 = N_Kerala - I0 - R0_init

# Making sure that both the predicted and the actual values have the same scale for time.
days = len(vaccinated)
dates = vaccinated['Date'].values

# Simulating the SIR model using a function.
#Takes intial susceptible population, initial infected people, initial recovered population, the rate of transmission, duration of infection, the initial population and the number of days. 
def simulate_SIR(S0, I0, R0, beta, gamma, N, days):
    S = [S0]
    I = [I0]
    R = [R0]
    
    for _ in range(days):
        curr_S = S[-1]
        curr_I = I[-1]
        curr_R = R[-1]
        dI = beta * curr_S * curr_I / N - gamma * curr_I
        dR = gamma * curr_I
        dS = -beta * curr_S * curr_I / N
        
        next_S = curr_S + dS
        next_I = curr_I + dI
        next_R = curr_R + dR

        S.append(next_S)
        I.append(next_I)
        R.append(next_R)
    
    return S, I, R

exp_S, exp_I, exp_R = simulate_SIR(S0, I0, R0_init, b, g, N_Kerala, days)


#Expected SIR graph for unvaccinated group 
bu = 0.3
gu = 0.1
I0u = 1
R0u_init = unvaccinated_data.iloc[0]['Cured']
S0u = N_Kerala - I0u - R0u_init
print(f"Reproduction Number R0 (unvaccinated) = {R0:.2f}")
days_unvac = len(unvaccinated_data)

exp_S_unvac, exp_I_unvac, exp_R_unvac = simulate_SIR(S0u, I0u, R0u_init, bu, gu, N_Kerala, days_unvac)
#The values for the predicted SIR graph for vaccinated and unvaccinated graphs are fit into it.
#Here I make 4 subplots so that all four of the graphs can be compared easily, and adjust the size of the figure for better clarity.
#Source for figsize command : https://matplotlib.org/stable/gallery/subplots_axes_and_figures/figure_size_units.html
fig, ax = plt.subplots(2, 2, figsize=(14, 8))

# Actual SIR (Unvaccinated)
ax[0, 0].plot(unvaccinated_data['Date'], unvaccS, 'b--', label='S')
ax[0, 0].plot(unvaccinated_data['Date'], unvaccI, 'r-', label='I')
ax[0, 0].plot(unvaccinated_data['Date'], unvaccR, 'g-.', label='R')
ax[0, 0].set_title('Actual SIR (Unvaccinated)')
ax[0, 0].legend()

# Actual SIR (Vaccinated)
ax[0, 1].plot(vaccinated['Date'], vaccS, 'b--', label='S')
ax[0, 1].plot(vaccinated['Date'], vaccI, 'r-', label='I')
ax[0, 1].plot(vaccinated['Date'], vaccR, 'g-.', label='R')
ax[0, 1].set_title('Actual SIR (Vaccinated)')
ax[0, 1].legend()


# Expected SIR (Unvaccinated)
ax[1, 0].plot(range(days_unvac + 1), exp_S_unvac, 'b--', label='S')
ax[1, 0].plot(range(days_unvac + 1), exp_I_unvac, 'r-', label='I')
ax[1, 0].plot(range(days_unvac + 1), exp_R_unvac, 'g-.', label='R')
ax[1, 0].set_title('Expected SIR (Unvaccinated - SIR Model)')
ax[1, 0].legend()

# Expected SIR (Vaccinated)
# You can use different beta/gamma here for vaccinated scenario if needed
ax[1, 1].plot(range(days + 1), exp_S, 'b--', label='S')
ax[1, 1].plot(range(days + 1), exp_I, 'r-', label='I')
ax[1, 1].plot(range(days + 1), exp_R, 'g-.', label='R')
ax[1, 1].set_title('Expected SIR (Vaccinated - SIR Model)')
ax[1, 1].legend()
#After fitting all four of the graphs and giving them a legend we use matplotlib.pyplot to plot the graphs.
plt.show()