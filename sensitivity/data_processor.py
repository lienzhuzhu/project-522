import csv
import os, sys
import argparse
import glob
import numpy as np
import openturns as ot
import openturns.viewer
import openturns.viewer as viewer
from math import factorial

# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--eventsfile', help='Input file with test events', type=str, required=True)
    parser.add_argument('-w', '--workloadsfile', help='Input file with test workloads', type=str, required=True)
    parser.add_argument('-D', '--directory', help='Specify the directory that contains run results (i.e., ~/prelim-root/2_events-1_trials-events_workloads_50ms-interval/results)', type=str, required=True)
    args = parser.parse_args()
    return args

# Populates the arrays that contain all events and all workloads
#
def process_input(events_input_file, workloads_input_file):

    all_events = []
    all_workloads = [] # stress-ng workloads from input. Type [string]. Example item: "--matrix-ops 100"

    with open(events_input_file) as events_file:
        for line in events_file:
            all_events.append(line.strip())

    with open(workloads_input_file) as workloads_file:
        for line in workloads_file:
            all_workloads.append(line.strip())

    return all_events, all_workloads

def get_csv_dirs(root_path):
    all_csvs = os.listdir(root_path)
    all_csvs = sorted(filter(os.path.isfile, glob.glob(root_path + '/*') ) )
    return all_csvs

def parse_results(all_csvs, all_events):
    all_input_results = {}
    all_output_results = []
    count_multiplexed = 0

    for events in all_events:
        all_input_results[events] = []
        
    for csv_result in all_csvs:
        with open(csv_result, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=('IT', 'C', 'U', 'E'))
            count_multiplexed = 0
            counting = 0
            recording = 0
            output_sum = 0
            current_events = ''
            recorded_events = []
            for x, row in enumerate(reader):
                if x == 0:
                    count_multiplexed = int(row['IT'][0])
                    continue
                if x < 2:
                    continue
                if row['IT'][0] == '-':
                    recording = 1
                    continue
                if recording == 1 and row['E'] is not None and counting != count_multiplexed:
                    output_sum += float(row['IT'])
                    current_events = row['E']
                    continue
                if recording == 1 and row['E'] is None and counting != count_multiplexed:
                    all_input_results[current_events].append(float(row['IT']))
                    recorded_events.append(current_events)
                    counting += 1
                    if counting == count_multiplexed:
                        all_output_results.append(output_sum)
                        counting = 0
                        recording = 0
                        output_sum = 0
                        current_events = ''
                        for events in all_events:
                            if events not in recorded_events:
                                all_input_results[events].append(0.0) # Filling missing value with 0 by default
                        recorded_events = []
                    else:
                        output_sum = 0
                    continue
                
    return all_input_results, all_output_results, count_multiplexed

def get_sobol_indice():
    return

def data_to_np_array(all_input_results, all_output_results, all_workloads, combinations):
    input_length = 0
                
    for keys in all_input_results:
        input_length = len(all_input_results[keys])
        # print(keys)
    
    input_np = np.array([])
    for i in range(input_length):
        temp_np = np.array([])
        for keys in all_input_results:
            temp_np = np.append(temp_np, all_input_results[keys][i])
            # print(all_input_results[keys][i])
            # print(type(all_input_results[keys][i]))
        # print(temp_np)
        if i == 0:
            input_np = temp_np
        else: 
            input_np = np.vstack((input_np, temp_np))
            
    output_np = np.zeros((len(all_output_results), combinations)) # Filling missing value with 0 by default
    
    workload_count = 0
    index_count = 0
    
    for i in range(len(all_output_results)):
        if workload_count < len(all_workloads):
            output_np[i][index_count] = all_output_results[i]
            # print(all_output_results[i])
            workload_count += 1
        if workload_count == len(all_workloads):
            workload_count = 0
            index_count += 1
        if index_count == combinations:
            index_count = 0
    return input_np, output_np

def main():
    args = parse_args()
    root_path = args.directory
    
    # Process Data from CSVs
    all_csvs = get_csv_dirs(root_path)

    all_events, all_workloads = process_input(args.eventsfile, args.workloadsfile)
    
    all_input_results, all_output_results, count_multiplexed = parse_results(all_csvs, all_events)
    
    combinations = (int) (factorial(len(all_events)) / (factorial(count_multiplexed) * factorial(len(all_events) - count_multiplexed)))
    
    input_np, output_np = data_to_np_array(all_input_results, all_output_results, all_workloads, combinations)
    
    # Sobol Sensitivity analysis start here
    # inputDistribution = ot.Normal(len(all_events))
    
    size = (int)(len(all_output_results) / (len(all_events) + 2))
    print(size)
    # sie = ot.SobolIndicesExperiment(inputDistribution, len(all_output_results))
    # inputDesign = sie.generate()
            
    outputDesign = ot.Sample(output_np)
    
    inputDesign = ot.Sample(input_np)
    
    inputDescription = ot.Description(len(all_events))
    textDescription = ot.Description(len(all_events))
    for i in range(len(all_events)):
        inputDescription[i] = all_events[i]
        textDescription[i] = 'bottom'
        
    # print(inputDescription)
    inputDesign.setDescription(inputDescription)
    
    print(inputDesign)
    print(outputDesign)

    sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(inputDesign, outputDesign, size)
    
    for i in range(combinations):
        print("Output #", i)
        first_order = sensitivityAnalysis.getFirstOrderIndices(i)
        total_order = sensitivityAnalysis.getTotalOrderIndices(i)
        print("    First order indices: ", first_order)
        print("    Total order indices: ", total_order)

    agg_first_order = sensitivityAnalysis.getAggregatedFirstOrderIndices()
    agg_total_order = sensitivityAnalysis.getAggregatedTotalOrderIndices()
    print("Agg. first order indices: ", agg_first_order)
    print("Agg. total order indices: ", agg_total_order)
    
    graph = sensitivityAnalysis.draw()
    
    text = graph.getDrawable(2)
    text.setTextPositions(textDescription)
    text.setTextSize(0.7)
    
    # print(text.getPattern())
    
    graph.setDrawable(text, 2)
    # print(graph.getDrawable(2).getDrawLabels())
    # print(graph.getDrawables())
    view = viewer.View(graph, legend_kw={'bbox_to_anchor':(0.86,1), 'loc':"upper left"})
    view.save('graph.png')
    # view.show()
    # view.close()
    
    # print(combinations)
    # np.set_printoptions(threshold=np.inf)
    # print(input_np)
    # print(output_np)
    
    # np.savetxt("input_np.csv", input_np,
    #           delimiter = ",")
    # np.savetxt("output_np.csv", output_np,
    #           delimiter = ",")
    
    # input_np.tofile('input_np.csv', sep = ',')
    # output_np.tofile('output_np.csv', sep = ',')
        
    # print(len(all_output_results))
    
    # print(all_input_results)
    # print(all_output_results)
                
            
                
if __name__ == "__main__":
    main()
