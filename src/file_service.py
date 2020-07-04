class FileService():
    def generate_file(self, id):
        return open("particle_timeline_{}.txt".format(id), "w+")

    def append_particle_position(self, file, x, y):
        file.write("{0} {1}\n".format(x, y))
