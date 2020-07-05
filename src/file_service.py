import os

class FileService():
    def generate_file(self, worker_id):
        return open(os.path.join('src', 'particle_timeline_data', f'particle_timeline_{worker_id}.txt'), 'w+')

    def append_particle_data(self, file, history):
        for line in history:
            if isinstance(line, str):
                file.write(line)
            else:
                for particle in line:
                    file.write(
                        f"{particle.x} {particle.y} {particle.size} {particle.color}\n")
