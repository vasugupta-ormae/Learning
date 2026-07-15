import streamlit as st
import pandas as pd

st.title("Hello User, Welcome to Streamlit")
st.header("Scheduling App")
st.markdown("Imagine you have a assembly line, with 7 stages. we have a list of jobs. Each jobs has a prescribed task that needs to be done at a given stage. So job1 -> task1 on stage, task2 on stage 2, task 3 on stage 3, finished. Different jobs will have different number of tasks. One task on one stage. There will be no gaps in stages, so job1 cannot have tasks on stage 1,2 and 4. Once a task is done on a stage, job will move to next stage, and next job's task will begin at current stage. Given a sequence of jobs, find total time needed to complete all jobs")

n_stages = st.number_input("Enter number of stages", min_value=1, max_value=10, value=7)
n_jobs = st.number_input("Enter number of jobs", min_value=1, max_value=100, value=5)
processing_time_input = st.text_input("Enter time taken for each job at each stage (use ';' to separate stages, e.g. 5,3,8,2,10;2,6,7,4,9)")

display_data = st.checkbox("Display Data")

if display_data and processing_time_input:
        # Split into stages
        stages = processing_time_input.split(";")

        # Convert each stage into a list of integers
        stage_data = [list(map(int, stage.split(","))) for stage in stages]

        # Check that every stage has the same number of jobs
        num_jobs = len(stage_data[0])
        if not all(len(stage) == num_jobs for stage in stage_data):
            st.error("Each stage must have the same number of job processing times.")
        else:
            # Transpose so rows = Jobs and columns = Stages
            df = pd.DataFrame(
                list(zip(*stage_data)),
                index=[f"Job {i+1}" for i in range(num_jobs)],
                columns=[f"Stage {i+1}" for i in range(len(stage_data))]
            )

            st.subheader("Processing Time Matrix")
            st.dataframe(df, use_container_width=True)


def job_sequencing(n_stages, n_jobs, processing_time_input):
    # Convert the input string into a stage-by-stage list
    processing_time = [
        list(map(int, stage.split(',')))
        for stage in processing_time_input.split(';')
        if stage.strip()
    ]

    if not processing_time:
        return 0, []

    n_stages = len(processing_time)
    n_jobs = len(processing_time[0])

    completion = [[0] * n_jobs for _ in range(n_stages)]

    for i in range(n_stages):
        for j in range(n_jobs):
            if i == 0 and j == 0:
                completion[i][j] = processing_time[i][j]
            elif i == 0:
                completion[i][j] = completion[i][j - 1] + processing_time[i][j]
            elif j == 0:
                completion[i][j] = completion[i - 1][j] + processing_time[i][j]
            else:
                completion[i][j] = max(
                    completion[i - 1][j],
                    completion[i][j - 1]
                ) + processing_time[i][j]

    makespan = completion[-1][-1]

    return makespan, completion


if st.button("Calculate"):
    makespan, completion = job_sequencing(
        n_stages,
        n_jobs,
        processing_time_input
    )

    st.success(f"Total completion time: {makespan}")

    # Display completion time matrix
    completion_df = pd.DataFrame(
        list(zip(*completion)),      # transpose
        index=[f"Job {i+1}" for i in range(len(completion[0]))],
        columns=[f"Stage {i+1}" for i in range(len(completion))]
    )

    st.subheader("Completion Time Matrix")
    st.dataframe(completion_df, use_container_width=True)