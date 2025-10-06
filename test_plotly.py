import plotly.graph_objects as go

# Create a simple figure
fig = go.Figure()

# Test the problematic update_layout call
try:
    fig.update_layout(
        title="안축장 성장 차트",
        xaxis=dict(
            title="나이 (연)",
            titlefont=dict(size=12),
            tickfont=dict(size=10),
            showgrid=True,
            gridcolor='rgba(128,128,128,0.3)',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.5)',
            zerolinewidth=1,
            showline=True,
            linecolor='rgba(128,128,128,0.8)',
            linewidth=1,
            showticklabels=True,
            tickmode='linear',
            tick0=4,
            dtick=2
        ),
        yaxis=dict(
            title="안축장 (mm)",
            titlefont=dict(size=12),
            tickfont=dict(size=10),
            showgrid=True,
            gridcolor='rgba(128,128,128,0.3)',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='rgba(128,128,128,0.5)',
            zerolinewidth=1,
            showline=True,
            linecolor='rgba(128,128,128,0.8)',
            linewidth=1,
            showticklabels=True,
            tickmode='linear',
            dtick=1,
            fixedrange=False
        ),
        hovermode='closest',
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.98,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.3)",
            borderwidth=1,
            font=dict(size=10)
        ),
        margin=dict(l=60, r=60, t=80, b=60),
        width=None,
        height=600,
        dragmode='pan'
    )
    print("update_layout call successful!")
except Exception as e:
    print(f"Error in update_layout: {e}")
    print(f"Error type: {type(e)}")
