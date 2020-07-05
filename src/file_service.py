class FileService():
    def generate_file(self, worker_id):
        return open("src/particle_timeline_data/particle_timeline_{}.txt".format(worker_id), "w+")

    def append_particle_data(self, file, particles):
        for particle in particles:
            file.write(
                f"{particle.x} {particle.y} {particle.size} {particle.color}\n")
