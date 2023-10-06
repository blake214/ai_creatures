import population
import simulation 
import genome 
import creature 
import numpy as np

def to_csv_file(data, csv_file):
    csv_str = ""
    for record in data:
        start = True
        for data in record:
            if not start:
                csv_str = csv_str + ","
            start = False

            if type(data) != str:
                data = str(data)
            csv_str = csv_str + data
        csv_str = csv_str + '\n'

    with open(csv_file, 'a') as f:
        f.write(csv_str)


def testBasicGA(paramiters, csv_name):
    record_filename = "records/"+csv_name+"_"+str(1)+".csv"
    records = []

    pop = population.Population(pop_size=paramiters['population_size'], 
                                gene_count=3)
    sim = simulation.ThreadedSim(pool_size=5)
    current_fittest = 0
    new_fitter = False

    for iteration in range(paramiters['iterations']):
        sim.eval_population(pop, 2400)
        fits = [cr.get_distance_travelled() 
                for cr in pop.creatures]
        links = [len(cr.get_expanded_links()) 
                for cr in pop.creatures]
        
        if np.max(fits) > current_fittest:
            new_fitter = True
            current_fittest = np.max(fits)
        print(iteration, "fittest:", np.round(np.max(fits), 3), "mean:", np.round(np.mean(fits), 3))

        fit_map = population.Population.get_fitness_map(fits)
        new_creatures = []
        for i in range(len(pop.creatures)):
            p1_ind = population.Population.select_parent(fit_map)
            p2_ind = population.Population.select_parent(fit_map)
            p1 = pop.creatures[p1_ind]
            p2 = pop.creatures[p2_ind]
            # now we have the parents!

            best_creature = 0
            if p2.get_distance_travelled() > p1.get_distance_travelled():
                best_creature = 1

            dna = genome.Genome.crossover(p1.dna, p2.dna, best_creature, paramiters['crossover'])
            dna = genome.Genome.point_mutate(dna, rate=paramiters['point_mutate_rate'], amount=paramiters['point_mutate_amount'])
            dna = genome.Genome.shrink_mutate(dna, rate=paramiters['shrink_mutate_rate'])
            dna = genome.Genome.grow_mutate(dna, rate=paramiters['grow_mutate_rate'])
            cr = creature.Creature(1)
            cr.update_dna(dna)
            new_creatures.append(cr)
        # elitism
        max_fit = np.max(fits)
        for cr in pop.creatures:
            if cr.get_distance_travelled() == max_fit:
                new_cr = creature.Creature(1)
                new_cr.update_dna(cr.dna)
                new_creatures[0] = new_cr

                if not new_fitter:
                    break
                new_fitter = False
                filename2 = "csvs/elite_"+str(paramiters['version'])+"_"+str(iteration)+".csv"
                
                genome.Genome.to_csv(cr.dna, filename2)
                break

        records.append([
            str(paramiters['version']),
            np.round(np.max(fits), 3), # Fittest score
            np.round(np.mean(fits), 3), # Fittest avg
            iteration # Fittest Gene
        ])
        pop.creatures = new_creatures
    to_csv_file(records, record_filename)

for par in paramiters_array:
    x = 5
    while x:
        testBasicGA(par, "Geno_link_space_a")
        x = x -1