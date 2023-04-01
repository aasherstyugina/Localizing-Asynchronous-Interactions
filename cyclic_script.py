log = pm4py.read_xes("data/IP-7/IP-7_init_log.xes")
    
    traces = []
    for trace in np.unique(log['case:concept:name']):
        filter = pm4py.filter_event_attribute_values(log, 'case:concept:name', {trace}, level='event')
        events = filter['concept:name'].to_numpy()
        traces.append(events)

    unique = ['a!_1', 'a!_2', 'a?_1', 'a?_2', 'b!_1', 'b!_2', 'b?_1', 'b?_2', 'q5', 'q6', 'q7', 'q8', 'q9', 't3', 't4', 't5', 't8', 't9']

    unique_a = ['a?_1', 'a?_2', 'b!_1', 'b!_2', 't3', 't4', 't5', 't8', 't9']
    unique_b = ['a!_1', 'a!_2', 'b?_1', 'b?_2', 'q5', 'q6', 'q7', 'q8', 'q9']

    mins = np.full((len(unique_a), len(unique_b)), fill_value=1000)
    maxs = np.full((len(unique_a), len(unique_b)), fill_value=-1000)
    for trace in traces:
        for i in range(len(unique_a)):
            for j in range(len(unique_b)):
                max_k = 0
                min_k = 0
                current = 0
                for t in trace:
                    if t == unique_a[i]:
                        current = current + 1
                    if t == unique_b[j]:
                        current = current - 1
                    max_k = np.max([current, max_k])
                    min_k = np.min([current, min_k])
                mins[i][j] = min(min_k, mins[i][j])
                maxs[i][j] = max(max_k, maxs[i][j])

    I = pd.Index(unique_a, name="rows")
    C = pd.Index(unique_b, name="columns")
    df_min = pd.DataFrame(data=mins, index=I, columns=C)
    print(df_min)
    I = pd.Index(unique_a, name="rows")
    C = pd.Index(unique_b, name="columns")
    df_max = pd.DataFrame(data=maxs, index=I, columns=C)
    print(df_max)
