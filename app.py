import streamlit as st

def run_bankers_algorithm(processes, resources, max_resources, currently_allocated, max_need):
    allocated = [0] * resources
    for i in range(processes):
        for j in range(resources):
            allocated[j] += currently_allocated[i][j]

    available = [max_resources[i] - allocated[i] for i in range(resources)]

    st.write(f"### Total Allocated Resources: {allocated}")
    st.write(f"### Total Available Resources: {available}")

    running = [True] * processes
    count = processes
    log = []
    while count != 0:
        safe = False
        for i in range(processes):
            if running[i]:
                executing = True
                for j in range(resources):
                    if max_need[i][j] - currently_allocated[i][j] > available[j]:
                        executing = False
                        break
                if executing:
                    log.append(f"Process {i + 1} is executing.")
                    running[i] = False
                    count -= 1
                    safe = True
                    for j in range(resources):
                        available[j] += currently_allocated[i][j]
                    break
        if not safe:
            log.append("The processes are in an unsafe state.")
            break
        else:
            log.append(f"Process is in a safe state. Available resources: {available}")
    return log

st.title("Banker's Algorithm Simulator")

processes = st.number_input("Number of processes", min_value=1, step=1)
resources = st.number_input("Number of resources", min_value=1, step=1)

max_resources_input = st.text_input("Maximum resources (space-separated)", "10 5 7")
max_resources = list(map(int, max_resources_input.split()))

currently_allocated = []
st.write("### Allocated Resources for Each Process")
for i in range(processes):
    alloc_input = st.text_input(f"Process {i+1} Allocated", "0 0 0", key=f"alloc_{i}")
    currently_allocated.append(list(map(int, alloc_input.split())))

max_need = []
st.write("### Maximum Need for Each Process")
for i in range(processes):
    max_input = st.text_input(f"Process {i+1} Max Need", "0 0 0", key=f"max_{i}")
    max_need.append(list(map(int, max_input.split())))

if st.button("Run Banker's Algorithm"):
    log = run_bankers_algorithm(processes, resources, max_resources, currently_allocated, max_need)
    st.write("### Output")
    for line in log:
        st.write(line)
