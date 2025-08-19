import streamlit as st
import numpy as np
import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import time
import pandas as pd
import matplotlib.pyplot as plt

# Define the logistic growth function for AI adoption rate
def logistic_growth(current_value, growth_rate, capacity):
    return current_value + growth_rate * current_value * (1 - current_value / capacity)

class HealthcareWorker(Agent):
    # Initialize attributes for each healthcare worker agents
    def __init__(self, unique_id, model, experience_years, initial_ai_adoption_rate):
        super().__init__(unique_id, model)
        scaling_factor = model.num_agents / 200  # scaling factor based on the number of agents
        self.tech_savviness = random.uniform(0.5 * scaling_factor, 1.5 * scaling_factor)
        self.experience_years = experience_years  + int(5 * scaling_factor)
        self.using_AI = False
        self.skill_level = min(1.0, self.experience_years / 25.0)
        self.efficiency = 0.5
        self.initial_ai_adoption_rate = initial_ai_adoption_rate
        self.training_delay = 0
        self.stress_level = 0.5 + model.ai_adoption_rate * (0.5 - self.tech_savviness) * scaling_factor
        self.job_satisfaction = 0.50 - model.ai_adoption_rate * (0.25 * self.tech_savviness) * scaling_factor
        self.resistance_to_change = random.uniform(0.1, 0.5)
        self.ai_efficacy = 1.0

    # Define the step function to simulate agent actions per time step
    def step(self):
        if not self.using_AI:
            adoption_chance = self.tech_savviness * self.model.ai_adoption_rate * (1 - self.resistance_to_change)
            self.using_AI = random.random() < adoption_chance

        if self.using_AI and self.training_delay <= 0:
            self.skill_level = min(self.skill_level + 0.02 * self.ai_efficacy * (1 - self.skill_level) + (initial_ai_adoption_rate/10), 1)
            self.efficiency = min(self.efficiency + 0.005 * self.ai_efficacy * (1 - self.efficiency) + (initial_ai_adoption_rate/10), 1)
            self.stress_level = min(max(self.stress_level - 0.005, 0.1)  + (initial_ai_adoption_rate/10), 0.1)
            self.job_satisfaction = min(self.job_satisfaction + 0.01 * (1 - self.job_satisfaction) + (initial_ai_adoption_rate/10), 1)


        else:
            self.training_delay -= 1 
            self.stress_level = min(self.stress_level + 0.005 + model.ai_adoption_rate * 0.5, 1)
            self.job_satisfaction = max(self.job_satisfaction - 0.02 - model.ai_adoption_rate * 0.75, 0.1)

class HealthcareModel(Model):
        # Initialize the model with a specified number of agents and initial AI adoption rate
    def __init__(self, num_agents, initial_ai_adoption_rate):
        self.num_agents = num_agents
        self.ai_adoption_rate = initial_ai_adoption_rate
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "AI Adoption Rate": lambda m: np.mean([a.using_AI for a in m.schedule.agents]),
                "Workforce Average Skill Level": lambda m: np.mean([a.skill_level for a in m.schedule.agents]),
                "Workplace Average Efficiency": lambda m: np.mean([a.efficiency for a in m.schedule.agents]),
                "Workforce Average Stress Level": lambda m: np.mean([a.stress_level for a in m.schedule.agents]),
                "Average Job Satisfaction": lambda m: np.mean([a.job_satisfaction for a in m.schedule.agents])
            }
        )
        # Calculate training delay based on initial adoption rate and number of agents
        training_delay_base = int(10 * initial_ai_adoption_rate * self.num_agents / 100)
        for i in range(self.num_agents):
            experience_years = random.randint(1, 20)
            agent = HealthcareWorker(i, self, experience_years, initial_ai_adoption_rate)
            agent.training_delay = training_delay_base
            self.schedule.add(agent)

    # Collect data and advance the model by one step
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Setup and control of the Streamlit interface
st.title('Healthcare AI Adoption Model')
st.write('Different metrics evolve as healthcare workers adopt AI technology. Watch to a minimum of 50 time units.')

st.sidebar.title('Simulation Control')
num_agents = st.sidebar.slider('Number of Agents', 1, 500, 150)
initial_ai_adoption_rate = 0.05

st.sidebar.write('Pick 1 or more metrics to monitor their evolution during the simulation:')
selected_metrics = st.sidebar.multiselect('Metrics', ['AI Adoption Rate', 'Workforce Average Skill Level', 'Workplace Average Efficiency', 'Workforce Average Stress Level', 'Average Job Satisfaction'], default=['AI Adoption Rate', 'Workplace Average Efficiency', 'Workforce Average Stress Level'])

plot_area = st.empty()
model = HealthcareModel(num_agents, initial_ai_adoption_rate)
data_frames = []

start_button = st.sidebar.button('Start Simulation')
stop_button = st.sidebar.button('Stop Simulation')

if start_button:
    for step in range(500):
        if stop_button:
            break
        model.step()
        results = model.datacollector.get_model_vars_dataframe()
        data_frames.append(results.tail(1))
        all_results = pd.concat(data_frames)

        fig, ax = plt.subplots()
        for metric in selected_metrics:
            ax.plot(all_results.index, all_results[metric], label=metric)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.set_xlabel('Time')
        ax.set_ylabel('Values')
        plot_area.pyplot(fig)
        time.sleep(0.9) 
