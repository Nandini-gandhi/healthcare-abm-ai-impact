# Architecture (Reference)

- **Framework:** Streamlit front-end; Mesa agents + model; RandomActivation schedule; DataCollector for metrics.
- **Controls:** sidebar slider for agents (1–500; default 150), metric multiselect, start/stop.
- **Run loop:** up to 500 steps with incremental plotting and a short sleep to animate.

```mermaid
graph TD
  UI[Streamlit UI] --> Controls[Sidebar Controls]
  Controls --> Model[HealthcareModel (Mesa)]
  Model --> Agents[HealthcareWorker Agents]
  Model --> Metrics[DataCollector → Metrics DataFrame]
  Metrics --> Charts[Matplotlib Line Chart]
```
