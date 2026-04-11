import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq

# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Power BI AI Agent",
    page_icon="⚡",
    layout="wide"
)

# ── Groq Client ────────────────────────────────────────────────────────────
client = Groq(api_key="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")

# ── AI Helper Function ─────────────────────────────────────────────────────
def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# ── Smart Full Data Summarizer ─────────────────────────────────────────────
def prepare_data_summary(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols     = df.select_dtypes(include="object").columns.tolist()

    summary = f"""
=== DATASET OVERVIEW ===
Total Rows    : {df.shape[0]:,}
Total Columns : {df.shape[1]}
Column Names  : {df.columns.tolist()}

=== NUMERIC STATISTICS (from ALL {df.shape[0]:,} rows) ===
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
=== FULL DATA AGGREGATIONS ===
{df[numeric_cols].agg(["sum","mean","min","max","median","std"]).round(2).to_string()}
"""

    summary += f"""
=== SAMPLE ROWS (Top 5) ===
{df.head(5).to_string()}

=== SAMPLE ROWS (Bottom 5) ===
{df.tail(5).to_string()}
"""
    return summary

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;'>⚡ Power BI AI Developer Agent</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; font-size:18px;'>"
    "Your AI Assistant for <b>DAX · SQL · Visuals · Insights · Recommendations</b>"
    "</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ── Sidebar — Data Upload ──────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg",
    width=80
)
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Upload any CSV file", type=["csv"]
)

df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(
        f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns"
    )
    st.sidebar.info(f"📋 Columns: {', '.join(df.columns.tolist())}")
else:
    st.sidebar.info("No file uploaded. Using sample data.")
    df = pd.DataFrame({
        "Month":      ["Jan","Feb","Mar","Apr","May","Jun"],
        "Region":     ["North","South","East","West","North","East"],
        "Category":   ["Tech","Retail","Tech","Retail","Finance","Finance"],
        "Sales":      [50000,62000,47000,80000,55000,71000],
        "Profit":     [12000,15000,9000,22000,13000,18000],
        "Orders":     [120,145,98,200,130,165],
        "Customer":   ["Alice","Bob","Carol","Dave","Eve","Frank"]
    })

# ── Auto Detect Data Domain ────────────────────────────────────────────────
numeric_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols     = df.select_dtypes(include="object").columns.tolist()
all_cols     = df.columns.tolist()

with st.spinner("🤖 AI detecting dataset type..."):
    domain_prompt = f"""
Based only on these column names: {all_cols}
In one short sentence, what type of dataset is this?
Example: "This appears to be a Sales Performance dataset."
Give only the one sentence, nothing else.
"""
    detected_domain = ask_ai(domain_prompt)

st.success(f"🤖 AI Detected: {detected_domain}")

# ── KPI Metrics ────────────────────────────────────────────────────────────
st.subheader("📊 Dataset Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rows",    f"{df.shape[0]:,}")
col2.metric("Total Columns", f"{df.shape[1]}")

if len(numeric_cols) >= 1:
    col3.metric(
        f"Total {numeric_cols[0]}",
        f"{df[numeric_cols[0]].sum():,.0f}"
    )
if len(numeric_cols) >= 2:
    col4.metric(
        f"Total {numeric_cols[1]}",
        f"{df[numeric_cols[1]].sum():,.0f}"
    )

with st.expander("👁️ Preview Dataset"):
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔷 DAX Generator",
    "🗄️ SQL Generator",
    "📈 Auto Visualizations",
    "💡 Insights & Recommendations",
    "🤖 Ask Anything"
])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — DAX GENERATOR
# ══════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("🔷 DAX Measure Generator")
    st.markdown(
        "Describe what you want to calculate "
        "and get ready-to-use DAX code instantly."
    )

    col_a, col_b = st.columns([2, 1])

    with col_a:
        dax_input = st.text_area(
            "📝 Describe your DAX requirement:",
            placeholder=(
                "e.g. Calculate month-over-month sales growth %\n"
                "e.g. Rank customers by total revenue\n"
                "e.g. Calculate YTD profit\n"
                "e.g. Show % of total sales per region"
            ),
            height=150,
            key="dax_text"
        )
        table_name   = st.text_input(
            "Table Name in Power BI model:", value="Sales"
        )
        columns_info = st.text_input(
            "Available Column Names (comma separated):",
            value=", ".join(all_cols)
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
            "Distinct Customer Count"
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
3. How to add this measure in Power BI Desktop
4. 2 related bonus DAX measures the user might also need
5. Common mistakes to avoid with this measure

Format all DAX code clearly inside code blocks.
"""
            with st.spinner("🤔 Generating DAX measure..."):
                result = ask_ai(prompt)
            st.success("✅ DAX Measure Generated!")
            st.markdown(result)
        else:
            st.warning("Please describe your DAX requirement first.")

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — SQL GENERATOR
# ══════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("🗄️ SQL Query Generator")
    st.markdown(
        "Describe what data you need and get "
        "production-ready, optimized SQL instantly."
    )

    col_c, col_d = st.columns([2, 1])

    with col_c:
        sql_input = st.text_area(
            "📝 Describe your SQL requirement:",
            placeholder=(
                "e.g. Get top 10 customers by sales last month\n"
                "e.g. Monthly sales with month-over-month growth\n"
                "e.g. Find customers with no orders in 90 days\n"
                "e.g. Sales by region with running total"
            ),
            height=150,
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
            "Describe your table structure (optional):",
            placeholder=(
                "e.g. Table: Orders "
                "(OrderID, CustomerID, OrderDate, Sales, Profit)\n"
                "Table: Customers (CustomerID, Name, Region)"
            ),
            value=(
                f"Table has columns: {', '.join(all_cols)} "
                f"with {df.shape[0]:,} rows."
            ),
            height=100
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
            "No activity in 90 days"
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
            st.warning("Please describe your SQL requirement first.")

# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — AUTO VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("📈 Auto Visualization Engine")
    st.markdown(
        "Select your columns and chart type — "
        "AI also recommends the best visual and Power BI tips."
    )

    col_e, col_f = st.columns(2)

    with col_e:
        chart_type = st.selectbox(
            "Choose Chart Type:",
            [
                "Bar Chart",
                "Line Chart",
                "Pie Chart",
                "Scatter Plot",
                "Area Chart",
                "Box Plot",
                "Histogram",
                "Treemap",
                "Funnel Chart"
            ]
        )
        x_col = st.selectbox("X-Axis / Category:", all_cols)

    with col_f:
        y_col = st.selectbox(
            "Y-Axis / Value:",
            numeric_cols if numeric_cols else all_cols
        )
        color_col = st.selectbox(
            "Color By (optional):",
            ["None"] + cat_cols
        )

    chart_title = st.text_input(
        "Chart Title:",
        value=f"{chart_type} — {y_col} by {x_col}"
    )
    color_val = None if color_col == "None" else color_col

    if st.button("📊 Generate Chart", type="primary", key="gen_chart"):
        fig = None

        try:
            if chart_type == "Bar Chart":
                fig = px.bar(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark"
                )
            elif chart_type == "Line Chart":
                fig = px.line(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark", markers=True
                )
            elif chart_type == "Pie Chart":
                fig = px.pie(
                    df, names=x_col, values=y_col,
                    title=chart_title, template="plotly_dark"
                )
            elif chart_type == "Scatter Plot":
                fig = px.scatter(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark"
                )
            elif chart_type == "Area Chart":
                fig = px.area(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark"
                )
            elif chart_type == "Box Plot":
                fig = px.box(
                    df, x=x_col, y=y_col, color=color_val,
                    title=chart_title, template="plotly_dark"
                )
            elif chart_type == "Histogram":
                fig = px.histogram(
                    df, x=x_col,
                    title=chart_title, template="plotly_dark"
                )
            elif chart_type == "Treemap":
                fig = px.treemap(
                    df, path=[x_col], values=y_col, title=chart_title
                )
            elif chart_type == "Funnel Chart":
                fig = px.funnel(
                    df, x=y_col, y=x_col, title=chart_title
                )

            if fig:
                st.plotly_chart(fig, use_container_width=True)

                chart_prompt = f"""
As a Power BI expert, analyze this chart:
Chart Type : {chart_type}
X-Axis     : {x_col}
Y-Axis     : {y_col}
Data Sample: {df[[x_col, y_col]].head(10).to_string()}

Provide:
1. Key insight from this chart in 2-3 sentences
2. Is this the best chart type for this data? Suggest better if not
3. Exact steps to recreate this in Power BI Desktop
4. A DAX measure that would enhance this visual
5. Any formatting tips for Power BI
"""
                with st.spinner("🤔 AI analyzing your chart..."):
                    viz_insight = ask_ai(chart_prompt)
                st.info("🤖 **AI Chart Analysis & Power BI Tips:**")
                st.markdown(viz_insight)

        except Exception as e:
            st.error(f"Chart error: {str(e)}. Try different column selections.")

# ══════════════════════════════════════════════════════════════════════════
# TAB 4 — INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("💡 Auto Insights & Recommendations")
    st.markdown(
        "AI analyzes your **complete dataset** using smart summarization "
        "— not just top rows — for accurate, real insights."
    )

    st.info(
        f"📊 This analysis uses ALL **{df.shape[0]:,} rows** "
        f"of your data through statistical summarization."
    )

    if st.button(
        "🔍 Analyze Full Dataset Now", type="primary", key="analyze"
    ):
        with st.spinner(
            f"🤔 Processing all {df.shape[0]:,} rows..."
        ):
            full_summary = prepare_data_summary(df)

        prompt_insights = f"""
You are a senior Power BI consultant and data analyst with 10+ years experience.

The following is a COMPLETE statistical summary derived from ALL {df.shape[0]:,} rows
of the dataset. Use actual numbers and column names in your response.

{full_summary}

Provide a comprehensive analysis:

## 1. KEY INSIGHTS
- Find exactly 5 important patterns or trends from the FULL data
- Mention specific numbers (e.g. "Sales peaked at X in month Y")
- Highlight any anomalies, outliers or data quality issues

## 2. POWER BI DASHBOARD RECOMMENDATIONS
- Best 5 visuals to build for this specific dataset
- Which KPI cards should be on the first page
- Best slicers and filters to add
- Suggested dashboard layout

## 3. DAX MEASURES TO CREATE
- Write 5 essential DAX measures for this exact dataset
- Include complete DAX code for each measure
- Explain what each measure does

## 4. SQL QUERIES FOR DATA PREPARATION
- Write 3 useful SQL queries for this data
- Focus on data cleaning or aggregation needs

## 5. BUSINESS RECOMMENDATIONS
- 3 to 5 specific, actionable business decisions based on this data
- Be specific using actual column names and numbers from the summary

Use actual column names: {all_cols}
"""
        with st.spinner("🤔 AI generating full insights..."):
            insights = ask_ai(prompt_insights)

        st.success("✅ Full Dataset Analysis Complete!")
        st.markdown(insights)

        st.markdown("---")
        st.subheader("📊 Auto-Generated Quick Charts")

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
                    agg_df,
                    x=cat_cols[0],
                    y=numeric_cols[0],
                    title=f"Total {numeric_cols[0]} by {cat_cols[0]}",
                    template="plotly_dark",
                    color=cat_cols[0]
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col_h:
                if len(numeric_cols) >= 2:
                    fig2 = px.scatter(
                        df,
                        x=numeric_cols[0],
                        y=numeric_cols[1],
                        color=cat_cols[0] if cat_cols else None,
                        title=(
                            f"{numeric_cols[0]} vs {numeric_cols[1]}"
                        ),
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig2, use_container_width=True)

            if len(numeric_cols) >= 1 and len(cat_cols) >= 1:
                pie_df = (
                    df.groupby(cat_cols[0])[numeric_cols[0]]
                    .sum()
                    .reset_index()
                )
                fig3 = px.pie(
                    pie_df,
                    names=cat_cols[0],
                    values=numeric_cols[0],
                    title=f"{numeric_cols[0]} Distribution by {cat_cols[0]}",
                    template="plotly_dark"
                )
                st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 5 — ASK ANYTHING
# ══════════════════════════════════════════════════════════════════════════
with tab5:
    st.header("🤖 Ask Anything — Power BI Expert")
    st.markdown(
        "Ask any Power BI, DAX, SQL, data modeling "
        "or analytics question."
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
        st.markdown("**💡 Popular Questions — Click to Use:**")
        popular_qs = [
            "Best practices for data modeling",
            "How to use CALCULATE in DAX",
            "Difference between Direct Query and Import",
            "How to create a date table in DAX",
            "How to optimize slow reports",
            "Row-level security setup",
            "When to use measures vs columns",
            "How to use bookmarks in Power BI"
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

Provide a detailed, practical answer with:
1. Clear explanation in simple terms
2. DAX or SQL code examples inside code blocks where relevant
3. Step-by-step instructions if applicable
4. Pro tips and best practices
5. Common mistakes to avoid
6. Any useful Microsoft documentation reference to check
"""
            with st.spinner("🤔 Getting expert answer..."):
                free_answer = ask_ai(prompt_free)
            st.success("✅ Expert Answer:")
            st.markdown(free_answer)
        else:
            st.warning("Please type or select a question first.")

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>"
    "⚡ <b>Power BI AI Agent</b> | "
    "Built by <b>Kumar Gaurav Srivastava</b> | "
    "Data Analyst & Power BI Developer"
    "</p>",
    unsafe_allow_html=True
)
