class FileService():
    def generate_file(self, worker_id):
        return open("particle_timeline_data/particle_timeline_{}.txt".format(worker_id), "w+")

    def append_particle_position(self, file, x_pos, y_pos):
        file.write("{0} {1}\n".format(x_pos, y_pos))
