import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Power BI AI Agent",
    page_icon="⚡",
    layout="wide"
)

# ── Custom CSS — Attractive UI ─────────────────────────────────
st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e0e0;
    }

    /* Hero Header */
    .hero-header {
        background: linear-gradient(90deg, #f7971e, #ffd200, #f7971e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        padding: 10px 0;
        letter-spacing: 2px;
    }

    .hero-sub {
        text-align: center;
        color: #b0b8d1;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }

    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #1e2a45, #243050);
        border: 1px solid #2e4070;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        margin: 6px 0;
    }

    .feature-card h4 {
        color: #ffd200;
        margin: 0 0 6px 0;
        font-size: 1rem;
    }

    .feature-card p {
        color: #9aaac8;
        margin: 0;
        font-size: 0.85rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        background: #1e2a45;
        color: #9aaac8;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #f7971e, #ffd200) !important;
        color: #0f0f1a !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #f7971e, #ffd200);
        color: #0f0f1a;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        transition: transform 0.2s;
    }

    .stButton > button:hover {
        transform: scale(1.03);
        background: linear-gradient(90deg, #ffd200, #f7971e);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1923, #1a2744);
        border-right: 1px solid #2e4070;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2a45, #243050);
        border: 1px solid #2e4070;
        border-radius: 10px;
        padding: 15px;
    }

    /* Text areas and inputs */
    .stTextArea textarea, .stTextInput input {
        background: #1e2a45 !important;
        color: #e0e0e0 !important;
        border: 1px solid #2e4070 !important;
        border-radius: 8px !important;
    }

    /* Success / Info boxes */
    .stSuccess, .stInfo {
        border-radius: 10px;
    }

    /* Divider */
    hr {
        border-color: #2e4070;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #6b7a99;
        font-size: 0.9rem;
        border-top: 1px solid #2e4070;
        margin-top: 30px;
    }

    .footer b {
        color: #ffd200;
    }
</style>
""", unsafe_allow_html=True)

# ── Groq Client ────────────────────────────────────────────────
client = Groq(api_key="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")

# ── AI Helper Function ─────────────────────────────────────────
def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# ── Data Summarizer ────────────────────────────────────────────
def prepare_data_summary(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols     = df.select_dtypes(include="object").columns.tolist()

    summary = f"""
=== DATASET OVERVIEW ===
Total Rows    : {df.shape[0]:,}
Total Columns : {df.shape[1]}
Column Names  : {df.columns.tolist()}

=== NUMERIC STATISTICS ===
{df[numeric_cols].describe().round(2).to_string() if numeric_cols else "No numeric columns"}

=== MISSING VALUES ===
{df.isnull().sum().to_string()}

=== CATEGORICAL COLUMNS — Top Values ===
"""
    for col in cat_cols[:6]:
        summary += f"\n{col} — Top 5 Values:\n"
        summary += df[col].value_counts().head(5).to_string()
        summary += "\n"

    if len(numeric_cols) >= 2:
        summary += f"""
=== CORRELATIONS ===
{df[numeric_cols].corr().round(2).to_string()}
"""
    if numeric_cols:
        summary += f"""
=== AGGREGATIONS ===
{df[numeric_cols].agg(["sum","mean","min","max","median","std"]).round(2).to_string()}
"""
    summary += f"""
=== SAMPLE ROWS (Top 5) ===
{df.head(5).to_string()}

=== SAMPLE ROWS (Bottom 5) ===
{df.tail(5).to_string()}
"""
    return summary

# ══════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(
    "<div class='hero-header'>⚡ Power BI AI Developer Agent</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div class='hero-sub'>Your AI Assistant for "
    "<b style='color:#ffd200'>DAX · SQL · Visuals · Insights · Recommendations</b>"
    " — No data upload required for DAX & SQL!</div>",
    unsafe_allow_html=True
)

# Feature highlights row
fc1, fc2, fc3, fc4, fc5 = st.columns(5)
with fc1:
    st.markdown("""<div class='feature-card'>
        <h4>🔷 DAX Generator</h4>
        <p>Write any DAX measure instantly</p>
    </div>""", unsafe_allow_html=True)
with fc2:
    st.markdown("""<div class='feature-card'>
        <h4>🗄️ SQL Generator</h4>
        <p>Production-ready SQL queries</p>
    </div>""", unsafe_allow_html=True)
with fc3:
    st.markdown("""<div class='feature-card'>
        <h4>📈 Auto Charts</h4>
        <p>Smart visualizations from data</p>
    </div>""", unsafe_allow_html=True)
with fc4:
    st.markdown("""<div class='feature-card'>
        <h4>💡 Insights</h4>
        <p>AI-powered data analysis</p>
    </div>""", unsafe_allow_html=True)
with fc5:
    st.markdown("""<div class='feature-card'>
        <h4>🤖 Ask Anything</h4>
        <p>Power BI expert on demand</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
st.sidebar.markdown(
    "<h2 style='color:#ffd200; text-align:center;'>⚡ Power BI AI Agent</h2>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='color:#9aaac8; text-align:center; font-size:0.85rem;'>"
    "Built by Kumar Gaurav Srivastava</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
st.sidebar.header("📂 Upload Your Dataset")
st.sidebar.markdown(
    "<p style='color:#9aaac8; font-size:0.85rem;'>"
    "Upload CSV for charts, insights & data analysis.<br>"
    "<b style='color:#ffd200;'>DAX and SQL tabs work without any upload!</b></p>",
    unsafe_allow_html=True
)
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

df = None
data_loaded = False

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    data_loaded = True
    st.sidebar.success(f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    st.sidebar.info(f"📋 Columns: {', '.join(df.columns.tolist())}")
else:
    st.sidebar.info("Using sample data for charts & insights.")
    df = pd.DataFrame({
        "Month":    ["Jan","Feb","Mar","Apr","May","Jun"],
        "Region":   ["North","South","East","West","North","East"],
        "Category": ["Tech","Retail","Tech","Retail","Finance","Finance"],
        "Sales":    [50000,62000,47000,80000,55000,71000],
        "Profit":   [12000,15000,9000,22000,13000,18000],
        "Orders":   [120,145,98,200,130,165],
        "Customer": ["Alice","Bob","Carol","Dave","Eve","Frank"]
    })

numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols     = df.select_dtypes(include="object").columns.tolist()
all_cols     = df.columns.tolist()

# ── Dataset Overview (only if data loaded) ─────────────────────
if data_loaded:
    st.subheader("📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows",    f"{df.shape[0]:,}")
    col2.metric("Total Columns", f"{df.shape[1]}")
    if len(numeric_cols) >= 1:
        col3.metric(f"Total {numeric_cols[0]}", f"{df[numeric_cols[0]].sum():,.0f}")
    if len(numeric_cols) >= 2:
        col4.metric(f"Total {numeric_cols[1]}", f"{df[numeric_cols[1]].sum():,.0f}")

    with st.expander("👁️ Preview Dataset"):
        st.dataframe(df, use_container_width=True)

    with st.spinner("🤖 AI detecting dataset type..."):
        domain_prompt = f"""
Based only on these column names: {all_cols}
In one short sentence, what type of dataset is this?
Example: "This appears to be a Sales Performance dataset."
Give only the one sentence, nothing else.
"""
        detected_domain = ask_ai(domain_prompt)
    st.success(f"🤖 AI Detected: {detected_domain}")
    st.markdown("---")
else:
    st.markdown(
        "<div style='background:linear-gradient(90deg,#1e2a45,#243050);"
        "border:1px solid #ffd200; border-radius:10px; padding:14px 20px;"
        "margin-bottom:20px;'>"
        "<b style='color:#ffd200;'>⚡ No data uploaded</b>"
        "<span style='color:#b0b8d1;'> — DAX Generator, SQL Generator and Ask Anything "
        "work fully without any data. Upload a CSV to unlock Charts and Insights.</span>"
        "</div>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔷 DAX Generator",
    "🗄️ SQL Generator",
    "📈 Auto Visualizations",
    "💡 Insights & Recommendations",
    "🤖 Ask Anything"
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — DAX GENERATOR (works without data)
# ══════════════════════════════════════════════════════════════
with tab1:
    st.header("🔷 DAX Measure Generator")
    st.markdown(
        "Describe your requirement in plain English. "
        "**No data upload needed** — works like ChatGPT for DAX."
    )

    col_a, col_b = st.columns([2, 1])

    with col_a:
        dax_input = st.text_area(
            "📝 Describe your DAX requirement:",
            placeholder=(
                "e.g. Calculate month-over-month sales growth %\n"
                "e.g. Rank customers by total revenue\n"
                "e.g. Calculate YTD profit\n"
                "e.g. Show % of total sales per region\n"
                "e.g. Create a rolling 3-month average of orders"
            ),
            height=160,
            key="dax_text"
        )
        table_name = st.text_input(
            "Table Name in Power BI model:",
            value="Sales",
            help="Type any table name — this will be used in the DAX formula"
        )
        columns_info = st.text_input(
            "Available Column Names (comma separated):",
            value=", ".join(all_cols),
            help="You can type your own column names if you haven't uploaded data"
        )

    with col_b:
        st.markdown("**💡 Quick Examples — Click to Use:**")
        dax_examples = [
            "YTD Sales",
            "Month-over-Month Growth %",
            "Rank by Revenue",
            "Running Total",
            "Same Period Last Year",
            "% of Total",
            "Rolling 3-Month Average",
            "Distinct Customer Count",
            "Profit Margin %",
            "Average Order Value"
        ]
        selected_dax = None
        for ex in dax_examples:
            if st.button(ex, key=f"dax_{ex}"):
                selected_dax = ex

    final_dax_input = selected_dax if selected_dax else dax_input

    if st.button("⚡ Generate DAX Measure", type="primary", key="gen_dax"):
        if final_dax_input:
            prompt = f"""
You are an expert Power BI DAX developer with 10+ years experience.

Table Name    : {table_name}
Columns       : {columns_info}
User Request  : {final_dax_input}

Generate:
1. Complete DAX measure with proper syntax in a code block
2. Step-by-step explanation of every function used
3. How to add this measure in Power BI Desktop (exact steps)
4. 2 related bonus DAX measures the user might also need
5. Common mistakes to avoid with this measure

Format all DAX code clearly inside code blocks.
"""
            with st.spinner("🤔 Generating DAX measure..."):
                result = ask_ai(prompt)
            st.success("✅ DAX Measure Generated!")
            st.markdown(result)
        else:
            st.warning("Please describe your DAX requirement or click a quick example.")

# ══════════════════════════════════════════════════════════════
# TAB 2 — SQL GENERATOR (works without data)
# ══════════════════════════════════════════════════════════════
with tab2:
    st.header("🗄️ SQL Query Generator")
    st.markdown(
        "Describe what data you need. "
        "**No data upload needed** — works like ChatGPT for SQL."
    )

    col_c, col_d = st.columns([2, 1])

    with col_c:
        sql_input = st.text_area(
            "📝 Describe your SQL requirement:",
            placeholder=(
                "e.g. Get top 10 customers by sales last month\n"
                "e.g. Monthly sales with month-over-month growth\n"
                "e.g. Find customers with no orders in 90 days\n"
                "e.g. Sales by region with running total\n"
                "e.g. Compare this year vs last year by month"
            ),
            height=160,
            key="sql_text"
        )
        db_type = st.selectbox(
            "Database / SQL Dialect:",
            [
                "SQL Server (T-SQL)",
                "MySQL",
                "PostgreSQL",
                "Oracle",
                "Snowflake",
                "BigQuery",
                "SQLite"
            ]
        )
        table_info_sql = st.text_area(
            "Describe your table structure (type your own or use uploaded data):",
            placeholder=(
                "e.g. Table: Orders (OrderID, CustomerID, OrderDate, Sales, Profit)\n"
                "Table: Customers (CustomerID, Name, Region, City)"
            ),
            value=(
                f"Table has columns: {', '.join(all_cols)} "
                f"with {df.shape[0]:,} rows."
            ),
            height=110
        )

    with col_d:
        st.markdown("**💡 Quick Examples — Click to Use:**")
        sql_examples = [
            "Top 10 by revenue",
            "Monthly trend",
            "Year-over-year comparison",
            "Customer segmentation",
            "Find duplicates",
            "Regional ranking",
            "Running total",
            "No activity in 90 days",
            "Sales by category",
            "Profit margin by region"
        ]
        selected_sql = None
        for ex in sql_examples:
            if st.button(ex, key=f"sql_{ex}"):
                selected_sql = ex

    final_sql_input = selected_sql if selected_sql else sql_input

    if st.button("⚡ Generate SQL Query", type="primary", key="gen_sql"):
        if final_sql_input:
            prompt = f"""
You are an expert SQL developer specializing in {db_type}.

Table Info     : {table_info_sql}
User Request   : {final_sql_input}
SQL Dialect    : {db_type}

Generate:
1. Complete, optimized SQL query in a code block
2. Step-by-step explanation of the query logic
3. Performance tips and indexing recommendations
4. Alternative approach if applicable
5. How this query can be used as a Power BI data source

Format SQL code clearly inside code blocks.
"""
            with st.spinner("🤔 Generating SQL query..."):
                result = ask_ai(prompt)
            st.success("✅ SQL Query Generated!")
            st.markdown(result)
        else:
            st.warning("Please describe your SQL requirement or click a quick example.")

# ══════════════════════════════════════════════════════════════
# TAB 3 — AUTO VISUALIZATIONS (improved charts)
# ══════════════════════════════════════════════════════════════
with tab3:
    st.header("📈 Auto Visualization Engine")

    if not data_loaded:
        st.warning(
            "📂 Upload a CSV file in the sidebar to use the visualization engine. "
            "Sample data is shown below for demo."
        )

    st.markdown(
        "Select columns and chart type — AI also gives Power BI tips for each chart."
    )

    col_e, col_f = st.columns(2)

    with col_e:
        chart_type = st.selectbox(
            "Choose Chart Type:",
            [
                "Bar Chart",
                "Grouped Bar Chart",
                "Line Chart",
                "Pie Chart",
                "Donut Chart",
                "Scatter Plot",
                "Area Chart",
                "Box Plot",
                "Histogram",
                "Treemap",
                "Funnel Chart",
                "Heatmap (Correlation)"
            ]
        )
        x_col = st.selectbox("X-Axis / Category:", all_cols)

    with col_f:
        y_col = st.selectbox(
            "Y-Axis / Value:",
            numeric_cols if numeric_cols else all_cols
        )
        color_col = st.selectbox(
            "Color / Group By (optional):",
            ["None"] + cat_cols
        )

    col_title, col_agg = st.columns(2)
    with col_title:
        chart_title = st.text_input(
            "Chart Title:",
            value=f"{chart_type} — {y_col} by {x_col}"
        )
    with col_agg:
        agg_method = st.selectbox(
            "Aggregation (for bar/line/area):",
            ["Sum", "Average", "Count", "Max", "Min"]
        )

    color_val = None if color_col == "None" else color_col

    if st.button("📊 Generate Chart", type="primary", key="gen_chart"):
        fig = None

        try:
            # Aggregate data smartly for categorical x-axis
            def get_agg_df(df, x, y, method):
                agg_map = {
                    "Sum": "sum", "Average": "mean",
                    "Count": "count", "Max": "max", "Min": "min"
                }
                return (
                    df.groupby(x)[y]
                    .agg(agg_map[method])
                    .reset_index()
                    .sort_values(y, ascending=False)
                )

            if chart_type == "Bar Chart":
                plot_df = get_agg_df(df, x_col, y_col, agg_method)
                fig = px.bar(
                    plot_df, x=x_col, y=y_col,
                    title=chart_title, template="plotly_dark",
                    color=x_col,
                    text=y_col,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                fig.update_layout(showlegend=False, uniformtext_minsize=10)

            elif chart_type == "Grouped Bar Chart":
                if color_val:
                    fig = px.bar(
                        df, x=x_col, y=y_col, color=color_val,
                        barmode="group",
                        title=chart_title, template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                else:
                    plot_df = get_agg_df(df, x_col, y_col, agg_method)
                    fig = px.bar(
                        plot_df, x=x_col, y=y_col,
                        title=chart_title, template="plotly_dark",
                        color=x_col,
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )

            elif chart_type == "Line Chart":
                fig = px.line(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark",
                    markers=True,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_traces(line=dict(width=3))

            elif chart_type == "Pie Chart":
                pie_df = get_agg_df(df, x_col, y_col, agg_method)
                fig = px.pie(
                    pie_df, names=x_col, values=y_col,
                    title=chart_title, template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")

            elif chart_type == "Donut Chart":
                pie_df = get_agg_df(df, x_col, y_col, agg_method)
                fig = px.pie(
                    pie_df, names=x_col, values=y_col,
                    title=chart_title, template="plotly_dark",
                    hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")

            elif chart_type == "Scatter Plot":
                fig = px.scatter(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark",
                    size_max=15,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

            elif chart_type == "Area Chart":
                fig = px.area(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

            elif chart_type == "Box Plot":
                fig = px.box(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

            elif chart_type == "Histogram":
                fig = px.histogram(
                    df, x=y_col, color=color_val,
                    title=chart_title, template="plotly_dark",
                    nbins=20,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

            elif chart_type == "Treemap":
                path_cols = [x_col] + ([color_col] if color_val else [])
                fig = px.treemap(
                    df, path=path_cols, values=y_col,
                    title=chart_title,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

            elif chart_type == "Funnel Chart":
                funnel_df = get_agg_df(df, x_col, y_col, agg_method)
                fig = px.funnel(
                    funnel_df, x=y_col, y=x_col,
                    title=chart_title,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )

            elif chart_type == "Heatmap (Correlation)":
                if len(numeric_cols) >= 2:
                    corr_df = df[numeric_cols].corr().round(2)
                    fig = px.imshow(
                        corr_df,
                        title="Correlation Heatmap",
                        template="plotly_dark",
                        color_continuous_scale="RdBu_r",
                        text_auto=True
                    )
                else:
                    st.error("Need at least 2 numeric columns for a heatmap.")

            if fig:
                fig.update_layout(
                    title_font_size=18,
                    title_font_color="#ffd200",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(15,15,26,0.8)",
                    font=dict(color="#e0e0e0"),
                    margin=dict(t=60, b=40, l=40, r=40)
                )
                st.plotly_chart(fig, use_container_width=True)

                # AI Chart Analysis
                chart_prompt = f"""
As a Power BI expert, analyze this chart:
Chart Type : {chart_type}
X-Axis     : {x_col}
Y-Axis     : {y_col}
Data Sample: {df[[x_col, y_col]].head(10).to_string()}

Provide:
1. Key insight from this chart in 2-3 sentences
2. Is this the best chart type? Suggest better if not
3. Exact steps to recreate this in Power BI Desktop
4. A DAX measure that would enhance this visual
5. Formatting tips for Power BI
"""
                with st.spinner("🤔 AI analyzing chart..."):
                    viz_insight = ask_ai(chart_prompt)
                st.info("🤖 **AI Chart Analysis & Power BI Tips:**")
                st.markdown(viz_insight)

        except Exception as e:
            st.error(f"Chart error: {str(e)} — Try a different column combination.")

# ══════════════════════════════════════════════════════════════
# TAB 4 — INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════
with tab4:
    st.header("💡 Auto Insights & Recommendations")

    if not data_loaded:
        st.warning("📂 Upload a CSV file in the sidebar to use this feature.")
        st.markdown(
            "This tab analyzes your uploaded dataset and provides:\n"
            "- Key business insights\n"
            "- Power BI dashboard recommendations\n"
            "- Auto-generated DAX measures\n"
            "- SQL queries for data prep\n"
            "- Business action recommendations"
        )
    else:
        st.markdown(
            "AI analyzes your **complete dataset** — not just top rows — "
            "for accurate, real insights."
        )
        st.info(
            f"📊 This analysis uses ALL **{df.shape[0]:,} rows** "
            f"through statistical summarization."
        )

        if st.button("🔍 Analyze Full Dataset Now", type="primary", key="analyze"):
            with st.spinner(f"🤔 Processing all {df.shape[0]:,} rows..."):
                full_summary = prepare_data_summary(df)

            prompt_insights = f"""
You are a senior Power BI consultant and data analyst with 10+ years experience.

Complete statistical summary from ALL {df.shape[0]:,} rows:

{full_summary}

Provide:

## 1. KEY INSIGHTS
- 5 important patterns with specific numbers
- Highlight anomalies or data quality issues

## 2. POWER BI DASHBOARD RECOMMENDATIONS
- Best 5 visuals for this dataset
- KPI cards for first page
- Best slicers and filters
- Suggested layout

## 3. DAX MEASURES TO CREATE
- 5 essential DAX measures with complete code
- Explanation of each

## 4. SQL QUERIES FOR DATA PREPARATION
- 3 useful SQL queries for this data

## 5. BUSINESS RECOMMENDATIONS
- 3-5 specific, actionable decisions from this data

Use actual column names: {all_cols}
"""
            with st.spinner("🤔 AI generating full insights..."):
                insights = ask_ai(prompt_insights)

            st.success("✅ Full Dataset Analysis Complete!")
            st.markdown(insights)
            st.markdown("---")
            st.subheader("📊 Auto-Generated Charts")

            if numeric_cols and cat_cols:
                col_g, col_h = st.columns(2)

                with col_g:
                    agg_df = (
                        df.groupby(cat_cols[0])[numeric_cols[0]]
                        .sum()
                        .reset_index()
                        .sort_values(numeric_cols[0], ascending=False)
                    )
                    fig1 = px.bar(
                        agg_df, x=cat_cols[0], y=numeric_cols[0],
                        title=f"Total {numeric_cols[0]} by {cat_cols[0]}",
                        template="plotly_dark", color=cat_cols[0],
                        text=numeric_cols[0],
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    fig1.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                    fig1.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        title_font_color="#ffd200"
                    )
                    st.plotly_chart(fig1, use_container_width=True)

                with col_h:
                    if len(numeric_cols) >= 2:
                        fig2 = px.scatter(
                            df, x=numeric_cols[0], y=numeric_cols[1],
                            color=cat_cols[0] if cat_cols else None,
                            title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                            template="plotly_dark",
                            color_discrete_sequence=px.colors.qualitative.Bold
                        )
                        fig2.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            title_font_color="#ffd200"
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                pie_df = (
                    df.groupby(cat_cols[0])[numeric_cols[0]]
                    .sum()
                    .reset_index()
                )
                fig3 = px.pie(
                    pie_df, names=cat_cols[0], values=numeric_cols[0],
                    title=f"{numeric_cols[0]} Distribution by {cat_cols[0]}",
                    template="plotly_dark", hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig3.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    title_font_color="#ffd200"
                )
                st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — ASK ANYTHING
# ══════════════════════════════════════════════════════════════
with tab5:
    st.header("🤖 Ask Anything — Power BI Expert")
    st.markdown(
        "Ask any Power BI, DAX, SQL, data modeling or analytics question. "
        "**Works exactly like ChatGPT — no data upload needed.**"
    )

    col_i, col_j = st.columns([2, 1])

    with col_i:
        free_question = st.text_area(
            "💬 Your Question:",
            placeholder=(
                "e.g. How do I create a dynamic title in Power BI?\n"
                "e.g. What is the difference between CALCULATE and FILTER?\n"
                "e.g. How to optimize a slow Power BI report?\n"
                "e.g. How to build a date table in DAX?\n"
                "e.g. Best practices for Power BI data modeling?"
            ),
            height=180
        )

    with col_j:
        st.markdown("**💡 Popular Questions — Click:**")
        popular_qs = [
            "Best practices for data modeling",
            "How to use CALCULATE in DAX",
            "Direct Query vs Import Mode",
            "How to create a date table in DAX",
            "How to optimize slow reports",
            "Row-level security setup",
            "Measures vs Calculated Columns",
            "How to use bookmarks in Power BI",
            "What is star schema",
            "How to handle many-to-many relationships"
        ]
        selected_q = None
        for q in popular_qs:
            if st.button(q, key=f"q_{q}"):
                selected_q = q

    final_question = selected_q if selected_q else free_question

    if st.button("🚀 Get Expert Answer", type="primary", key="free_ask"):
        if final_question:
            prompt_free = f"""
You are a senior Power BI expert with 10+ years of experience
in DAX, SQL, data modeling, report design and Power BI service.

Question: {final_question}

Provide:
1. Clear explanation in simple terms
2. DAX or SQL code examples in code blocks where relevant
3. Step-by-step instructions if applicable
4. Pro tips and best practices
5. Common mistakes to avoid
6. Useful Microsoft documentation reference
"""
            with st.spinner("🤔 Getting expert answer..."):
                free_answer = ask_ai(prompt_free)
            st.success("✅ Expert Answer:")
            st.markdown(free_answer)
        else:
            st.warning("Please type a question or click one from the list.")

# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div class='footer'>"
    "⚡ <b>Power BI AI Agent</b> | "
    "Built by <b>Kumar Gaurav Srivastava</b> | "
    "Data Analyst & Power BI Developer | "
    "Powered by <b>Groq AI + LLaMA 3.3</b>"
    "</div>",
    unsafe_allow_html=True
)
