from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/generate")
async def generate_graphs(filePath: str):
    df = pd.read_csv(filePath)  # Add Excel support later
    graphs = []

    # Initial Bar (categorical x, numeric y)
    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(include='object').columns
    if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
        x_col, y_col = categorical_cols[0], numeric_cols[0]
        frames = []
        for i in range(len(df) + 1):
            y_values = df[y_col][:i].tolist() + [0] * (len(df) - i)
            max_val = max(y_values) if max(y_values) > 0 else 1e-10
            colors = [f'rgb({int(255*(v/max_val))},{int(255*(1-v/max_val))},128)' if isinstance(v, (int, float)) else '#888888' for v in y_values]
            frames.append(go.Frame(data=[go.Bar(x=df[x_col], y=y_values, marker=dict(color=colors))], name=f'frame{i}'))
        fig_bar = go.Figure(data=[go.Bar(x=df[x_col], y=[0]*len(df), marker=dict(color=['#888888']*len(df)))], frames=frames)
        fig_bar.update_layout(title=f"{y_col} vs {x_col}", xaxis_title=x_col, yaxis_title=y_col, yaxis_range=[0, df[y_col].max() * 1.1])
        fig_bar.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 300}, "transition": {"duration": 200}, "fromcurrent": True, "mode": "immediate"}])])])
        graphs.append(fig_bar.to_html(full_html=False))

    # Initial Donut (categorical distribution)
    if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
        fig_donut = px.pie(df, names=categorical_cols[0], values=numeric_cols[0], hole=0.3, title="Donut Distribution")
        fig_donut.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 500}, "transition": {"duration": 300}, "fromcurrent": True, "mode": "immediate"}])])])
        graphs.append(fig_donut.to_html(full_html=False))

    return {"graphs": graphs}
