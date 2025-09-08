import random

# --------- Problem Definition ---------
processing_times = [5, 2, 7, 3, 8, 4]
num_tasks = len(processing_times)
num_machines = 3

# --------- PSO Parameters ---------
num_particles = 10
max_iterations = 50
w = 0.5       # inertia weight
c1 = 1.5      # cognitive coefficient
c2 = 1.5      # social coefficient

# --------- Fitness Function ---------
def fitness(position):
    machine_times = [0] * num_machines
    for task_index, machine in enumerate(position):
        machine_times[machine] += processing_times[task_index]
    return max(machine_times)

# --------- Initialize particles ---------
def initialize_particles():
    particles, velocities, pbest_positions, pbest_scores = [], [], [], []
    for _ in range(num_particles):
        position = [random.randint(0, num_machines - 1) for _ in range(num_tasks)]
        velocity = [random.choice([-1, 0, 1]) for _ in range(num_tasks)]
        particles.append(position)
        velocities.append(velocity)
        pbest_positions.append(position[:])
        pbest_scores.append(fitness(position))
    return particles, velocities, pbest_positions, pbest_scores

# --------- Update velocity ---------
def update_velocity(velocity, position, pbest, gbest):
    new_velocity = []
    for i in range(num_tasks):
        r1, r2 = random.random(), random.random()
        inertia = w * velocity[i]
        cognitive = c1 * r1 * (pbest[i] - position[i])
        social = c2 * r2 * (gbest[i] - position[i])
        vel = inertia + cognitive + social

        if vel > 1:
            new_velocity.append(random.randint(1, num_machines-1))
        elif vel < -1:
            new_velocity.append(-random.randint(1, num_machines-1))
        else:
            new_velocity.append(int(round(vel)))
    return new_velocity

# --------- Update position ---------
def update_position(position, velocity):
    new_position = position[:]
    for i in range(num_tasks):
        new_val = position[i] + velocity[i]
        new_val = new_val % num_machines  # wrap around to keep valid machine index
        new_position[i] = new_val
    return new_position

# --------- Main PSO Loop ---------
particles, velocities, pbest_positions, pbest_scores = initialize_particles()
gbest_index = pbest_scores.index(min(pbest_scores))
gbest_position = pbest_positions[gbest_index][:]
gbest_score = pbest_scores[gbest_index]

print(f"Initial best makespan: {gbest_score}\n")

for iteration in range(max_iterations):
    print(f"--- Iteration {iteration+1} ---")
    for i in range(num_particles):
        score = fitness(particles[i])
        print(f"Particle {i+1}: Position {particles[i]}, Fitness {score}")

        # update personal best
        if score < pbest_scores[i]:
            pbest_scores[i] = score
            pbest_positions[i] = particles[i][:]

        # update global best
        if score < gbest_score:
            gbest_score = score
            gbest_position = particles[i][:]

    # update all particles
    for i in range(num_particles):
        velocities[i] = update_velocity(velocities[i], particles[i], pbest_positions[i], gbest_position)
        particles[i] = update_position(particles[i], velocities[i])

    print(f"Best makespan after iteration {iteration+1}: {gbest_score}\n")

# --------- Final Output ---------
print("\nFinal Best Makespan:", gbest_score)
print("Task assignment to machines:")
for machine in range(num_machines):
    tasks = [i for i in range(num_tasks) if gbest_position[i] == machine]
    total_time = sum(processing_times[i] for i in tasks)
    print(f"Machine {machine+1}: Tasks {tasks}, Total time {total_time}")


"""OUTPUT:
Initial best makespan: 11

--- Iteration 1 ---
Particle 1: Position [0, 0, 1, 2, 1, 2], Fitness 15
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [1, 2, 0, 2, 1, 1], Fitness 17
Particle 4: Position [2, 2, 2, 2, 2, 1], Fitness 25
Particle 5: Position [1, 1, 1, 2, 2, 0], Fitness 14
Particle 6: Position [1, 1, 2, 1, 1, 0], Fitness 18
Particle 7: Position [0, 1, 1, 0, 2, 2], Fitness 12
Particle 8: Position [0, 1, 2, 0, 0, 2], Fitness 16
Particle 9: Position [0, 0, 2, 0, 2, 2], Fitness 19
Particle 10: Position [1, 2, 0, 0, 2, 0], Fitness 14
Best makespan after iteration 1: 11

--- Iteration 2 ---
Particle 1: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 4: Position [0, 1, 0, 0, 2, 1], Fitness 15
Particle 5: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 6: Position [0, 1, 1, 0, 1, 0], Fitness 17
Particle 7: Position [0, 1, 1, 0, 2, 2], Fitness 12
Particle 8: Position [0, 1, 2, 0, 1, 2], Fitness 11
Particle 9: Position [0, 0, 2, 0, 2, 2], Fitness 19
Particle 10: Position [2, 1, 0, 0, 2, 0], Fitness 14
Best makespan after iteration 2: 11

--- Iteration 3 ---
Particle 1: Position [0, 0, 1, 2, 2, 2], Fitness 15
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [2, 0, 0, 2, 2, 1], Fitness 16
Particle 5: Position [0, 0, 1, 2, 2, 0], Fitness 11
Particle 6: Position [0, 1, 1, 0, 2, 2], Fitness 12
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 0], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 10: Position [0, 0, 1, 0, 2, 2], Fitness 12
Best makespan after iteration 3: 11

--- Iteration 4 ---
Particle 1: Position [0, 0, 1, 1, 2, 2], Fitness 12
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [1, 0, 1, 0, 2, 1], Fitness 16
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 1, 0], Fitness 14
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [2, 0, 1, 0, 2, 2], Fitness 17
Best makespan after iteration 4: 11

--- Iteration 5 ---
Particle 1: Position [0, 0, 1, 2, 2, 2], Fitness 15
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 1, 1], Fitness 12
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 5: 11

--- Iteration 6 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 2], Fitness 12
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 0, 0, 2, 2], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [2, 0, 1, 0, 2, 1], Fitness 13
Best makespan after iteration 6: 11

--- Iteration 7 ---
Particle 1: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 2, 1], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 7: 11

--- Iteration 8 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 2, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 1], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [2, 0, 1, 0, 2, 1], Fitness 13
Best makespan after iteration 8: 11

--- Iteration 9 ---
Particle 1: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 1, 2], Fitness 17
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 9: 11

--- Iteration 10 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 1, 2], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [2, 0, 1, 0, 2, 1], Fitness 13
Best makespan after iteration 10: 11

--- Iteration 11 ---
Particle 1: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 1, 2], Fitness 17
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [1, 0, 1, 0, 2, 1], Fitness 16
Best makespan after iteration 11: 11

--- Iteration 12 ---
Particle 1: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 12: 11

--- Iteration 13 ---
Particle 1: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 1, 1], Fitness 14
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 13: 11

--- Iteration 14 ---
Particle 1: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 1, 1], Fitness 21
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 14: 11

--- Iteration 15 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 15: 11

--- Iteration 16 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 2, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 1, 2], Fitness 17
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 16: 11

--- Iteration 17 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 1, 2], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 17: 11

--- Iteration 18 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 18: 11

--- Iteration 19 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 1, 1], Fitness 19
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 19: 11

--- Iteration 20 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 0, 2, 0], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 1, 2], Fitness 17
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 20: 11

--- Iteration 21 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 0, 2, 0], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 2], Fitness 19
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 21: 11

--- Iteration 22 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 2, 2, 2], Fitness 15
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 1, 1], Fitness 12
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 22: 11

--- Iteration 23 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 2, 0, 0, 1, 1], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 23: 11

--- Iteration 24 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 24: 11

--- Iteration 25 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 0, 0, 2, 0], Fitness 21
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 25: 11

--- Iteration 26 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 1, 1], Fitness 12
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 26: 11

--- Iteration 27 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 1, 2], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 27: 11

--- Iteration 28 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 2, 2], Fitness 12
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 28: 11

--- Iteration 29 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 29: 11

--- Iteration 30 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 1, 1], Fitness 14
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 30: 11

--- Iteration 31 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 1, 1], Fitness 19
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 31: 11

--- Iteration 32 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 0], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 32: 11

--- Iteration 33 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 2, 2, 2], Fitness 15
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 1], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 33: 11

--- Iteration 34 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 2, 2, 2], Fitness 15
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 1, 0], Fitness 12
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 34: 11

--- Iteration 35 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 1, 2], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 35: 11

--- Iteration 36 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 36: 11

--- Iteration 37 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 2, 0], Fitness 14
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 37: 11

--- Iteration 38 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 1], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 38: 11

--- Iteration 39 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 0], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 39: 11

--- Iteration 40 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 2, 2], Fitness 19
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 40: 11

--- Iteration 41 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 1, 0, 1, 0], Fitness 17
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 41: 11

--- Iteration 42 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 1, 2], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 42: 11

--- Iteration 43 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 0, 2], Fitness 16
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 43: 11

--- Iteration 44 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 2, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 1, 1], Fitness 14
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 44: 11

--- Iteration 45 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 0, 1], Fitness 18
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 45: 11

--- Iteration 46 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 2, 2, 2], Fitness 15
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 1, 0, 2, 2], Fitness 12
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 46: 11

--- Iteration 47 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 0, 2, 0], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 2, 1], Fitness 15
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 47: 11

--- Iteration 48 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 2, 1, 0, 2, 1], Fitness 11
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 2, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 2, 2], Fitness 19
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 48: 11

--- Iteration 49 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 5: Position [0, 0, 1, 1, 2, 0], Fitness 11
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 0, 2, 0, 1, 2], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 49: 11

--- Iteration 50 ---
Particle 1: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 2: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 3: Position [0, 1, 1, 0, 2, 1], Fitness 13
Particle 4: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 5: Position [0, 0, 1, 1, 2, 1], Fitness 14
Particle 6: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 7: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 8: Position [0, 1, 2, 0, 1, 2], Fitness 11
Particle 9: Position [0, 0, 1, 0, 2, 1], Fitness 11
Particle 10: Position [0, 0, 1, 0, 2, 1], Fitness 11
Best makespan after iteration 50: 11


Final Best Makespan: 11
Task assignment to machines:
Machine 1: Tasks [0, 1, 3], Total time 10
Machine 2: Tasks [2, 5], Total time 11
Machine 3: Tasks [4], Total time 8

=== Code Execution Successful ==="""
