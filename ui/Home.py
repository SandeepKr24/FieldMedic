import requests
import streamlit as st

API_URL = "http://api:3000"

st.set_page_config(
    page_title="FieldMedic",
    page_icon="🏥",
    layout="wide",
)

# -------------------------------------------------------
# CSS
# -------------------------------------------------------

st.markdown(
    """
<style>

.block-container{
    padding-top:1.4rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

h1,h2,h3{
    margin-top:0;
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-bottom:0;
}

.subtitle{
    text-align:center;
    color:#7a7a7a;
    font-size:18px;
    margin-top:-10px;
    margin-bottom:20px;
}

.card-title{
    font-size:24px;
    font-weight:600;
    margin-bottom:10px;
}

div[data-testid="stVerticalBlock"]{
    gap:0.65rem;
}

</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.markdown(
    '<div class="title">🏥 FieldMedic</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">AI-powered Clinical Decision Support System</div>',
    unsafe_allow_html=True,
)

left, right = st.columns(
    [2, 3],
    gap="large",
)

# =======================================================
# LEFT PANEL
# =======================================================

with left:

    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Patient Information</div>',
            unsafe_allow_html=True,
        )

        symptoms = st.text_area(
            "Symptoms",
            height=80,
            placeholder="Describe the patient's symptoms...",
        )

        st.markdown("#### Vital Signs")

        col1, col2 = st.columns(2)

        with col1:

            spo2 = st.number_input(
                "SpO₂ (%)",
                min_value=0,
                max_value=100,
                value=98,
            )

            heart_rate = st.number_input(
                "Heart Rate",
                min_value=0,
                max_value=250,
                value=72,
            )

            temperature = st.number_input(
                "Temperature (°C)",
                value=37.0,
                step=0.1,
            )

        with col2:

            blood_pressure = st.text_input(
                "Blood Pressure",
                placeholder="120/80",
            )

            respiratory_rate = st.number_input(
                "Respiratory Rate",
                min_value=0,
                max_value=80,
                value=16,
            )

        additional_info = st.text_area(
            "Additional Clinical Information",
            height=110,
            placeholder="""Examples:

Hb = 3
Weight = 65 kg
Height = 170 cm
Blood Glucose = 280
Known Allergy = Penicillin
""",
        )

        if st.button(
            "🚑 TRIAGE PATIENT",
            use_container_width=True,
            type="primary",
        ):

            vitals = {
                "spo2": spo2,
                "heart_rate": heart_rate,
                "temperature": temperature,
                "blood_pressure": blood_pressure,
                "respiratory_rate": respiratory_rate,
            }

            payload = {
                "symptoms": symptoms,
                "vitals": vitals,
                "additional_info": additional_info,
            }

            # try:

            #     with st.spinner("Analyzing patient..."):

            #         response = requests.post(
            #             f"{API_URL}/triage",
            #             json=payload,
            #             timeout=120,
            #         )

            #         response.raise_for_status()

            #         st.session_state.result = response.json()

            # except Exception as e:

            #     st.error(f"Error: {e}")

            try:

                with st.spinner("Analyzing patient..."):

                    response = requests.post(
                        f"{API_URL}/triage",
                        json=payload,
                        timeout=120,
                    )

                    if response.status_code != 200:

                        try:
                            error = response.json().get(
                                "detail",
                                "An unexpected error occurred.",
                            )
                        except Exception:
                            error = "An unexpected error occurred."

                        st.error(error)
                        st.stop()

                    st.session_state.result = response.json()

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. The AI model may be busy. Please try again."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the FieldMedic API. Please make sure the backend is running."
                )

            except Exception as e:

                st.error(f"Unexpected error: {e}")

# =======================================================
# RIGHT PANEL
# =======================================================

with right:

    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Triage Result</div>',
            unsafe_allow_html=True,
        )

        result = st.session_state.result

        if result is None:

            st.info(
                """
Enter the patient's symptoms and clinical information, then click **🚑 TRIAGE PATIENT** to generate a recommendation.
                """
            )

        else:

            triage = result.get("triage", "Unknown")
            confidence = result.get("confidence", 0.0)

            # -----------------------------------------
            # Priority
            # -----------------------------------------

            if triage.lower() == "emergency":
                st.error(f"🔴 **{triage}**")

            elif triage.lower() == "urgent":
                st.warning(f"🟠 **{triage}**")

            else:
                st.success(f"🟢 **{triage}**")

            st.progress(min(max(confidence, 0.0), 1.0))

            st.caption(f"Confidence: **{confidence:.0%}**")

            st.divider()

            # -----------------------------------------
            # Care Plan
            # -----------------------------------------

            st.subheader("Care Plan")

            st.write(
                result.get(
                    "care_plan",
                    "No care plan available.",
                )
            )

            st.divider()

            # -----------------------------------------
            # Summary
            # -----------------------------------------

            st.subheader("Clinical Summary")

            st.write(
                result.get(
                    "summary",
                    "No summary available.",
                )
            )

            st.divider()

            # -----------------------------------------
            # ICD-10
            # -----------------------------------------

            st.subheader("ICD-10 Codes")

            codes = result.get("icd10", [])

            if codes:

                for code in codes:
                    st.write(f"• {code}")

            else:

                st.write("No ICD-10 codes returned.")

            # -----------------------------------------
            # Supporting Evidence
            # -----------------------------------------

            evidence = result.get("evidence", [])

            if evidence:

                st.divider()

                with st.expander("Supporting Evidence"):

                    for i, chunk in enumerate(evidence, start=1):

                        st.markdown(f"**Evidence {i}**")

                        st.write(chunk)

                        if i != len(evidence):
                            st.divider()