log = pm4py.read_xes("data/IP-6/IP-6_init_log.xes")

    traces = []
    for trace in np.unique(log['case:concept:name']):
        filter = pm4py.filter_event_attribute_values(log, 'case:concept:name', {trace}, level='event')
        traces.append(filter['concept:name'].to_numpy())


    agent_1 = ['t2', 't3', 'b!_1', 't9', 'b!_2', 't10', 't23', 't24', 't25', 't26', 'd?_1', 't57', 'd?_2', 't31', 'a!', 't12', 't17', 't18', 't11', 't16', 't19', 't13', 't15', 't20', 't14', 't21', 't22', 'c?', 't32' ]
    agent_2 = ['q1', 'q3', 'a?', 'q7', 'q12', 'c!_1', 'q8', 'q13', 'c!_2', 'q15', 'q16', 'q2', 'q4', 'b?', 'q5', 'q9', 'q10', 'q6', 'q11', 'd!', 'q14', 'q17', 'q18', 'q19']

    matrix = np.full((len(agent_1), len(agent_2)), fill_value=2)

    for trace in traces:
        for i in range(len(trace) - 1):
            for j in range(i + 1, len(trace)):
                if trace[i] in agent_1 and trace[j] in agent_1:
                    continue
                if trace[i] in agent_2 and trace[j] in agent_2:
                    continue

                if trace[i] in agent_1:
                    row = agent_1.index(trace[i])
                    col = agent_2.index(trace[j])
                    if matrix[row, col] == 2:
                        matrix[row, col] = -1
                    if matrix[row, col] == -1 or matrix[row, col] == 0:
                        continue
                    if matrix[row, col] == 1:
                        matrix[row, col] = 0
                else:
                    row = agent_1.index(trace[j])
                    col = agent_2.index(trace[i])
                    if matrix[row, col] == 2:
                        matrix[row, col] = 1
                    if matrix[row, col] == 1 or matrix[row, col] == 0:
                        continue
                    if matrix[row, col] == -1:
                        matrix[row, col] = 0
    I = pd.Index(agent_1, name="rows")
    C = pd.Index(agent_2, name="columns")
    df = pd.DataFrame(data=matrix, index=I, columns=C)
    print(df)

    minimum = []

    for i in range(len(agent_1)):
        for j in range(len(agent_2)):
            try:
                if matrix[i, j] == -1 and matrix[i+1, j] != -1 and matrix[i, j-1] != -1:
                    minimum.append([agent_1[i], agent_2[j]])
                if matrix[i,j] == 1 and matrix[i-1, j] != 1 and matrix[i, j+1] != 1:
                    minimum.append([agent_2[j], agent_1[i]])
            except:
                continue
    print(minimum)
