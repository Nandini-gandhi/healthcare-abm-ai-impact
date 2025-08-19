# AI Integration Impact on Healthcare Workforce — Agent-Based Model (Streamlit)

Interactive simulation of how **AI adoption** affects healthcare workforce dynamics (stress, satisfaction, efficiency, skills).  
**Live app:** https://nandini-mfss.streamlit.app/

> Tip: try all five metrics and different AI-adoption settings in the UI.

## Documentation & Demo
- **Live Demo:** Try the interactive simulation at [https://nandini-mfss.streamlit.app/](https://nandini-mfss.streamlit.app/)
- **Documentation:** For detailed explanation and research context, see [`docs/Healthcare_ABM_Documentation.pdf`](docs/Healthcare_ABM_Documentation.pdf)

## What's inside
- **Streamlit UI** with controls and charts (this repo includes `app.py`).
- **Five metrics** you can toggle: AI Adoption Rate, Workforce Average Skill Level, Workplace Average Efficiency, Workforce Average Stress Level, Average Job Satisfaction.
- **Agents & model** implemented with Mesa; random-activation schedule and a data collector for metrics.

## How the app works (at a glance)
- **Controls:**  
  • **Number of Agents** slider (1–500, default 150) in the sidebar.  
  • Select any of the **five metrics** to plot over time.  
  • **Start Simulation** / **Stop Simulation** buttons.
- **Run behavior:** up to **500 time steps** with a short delay so the chart animates.
- **Model:** `HealthcareWorker` and `HealthcareModel` track adoption, skill, efficiency, stress, and satisfaction.

## Papers & context
- For the complete research context and detailed analysis, please refer to the documentation in [`docs/Healthcare_ABM_Documentation.pdf`](docs/Healthcare_ABM_Documentation.pdf).

## License
MIT (see `LICENSE`).
